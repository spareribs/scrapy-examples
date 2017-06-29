#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/6/28 17:25
# @Author  : Spareribs
# @File    : process_mongo_redismgr.py
"""

import time
import redis
import hashlib
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo import errors


class MongoRedisUrlManager:
    REDIS_SERVER_IP = "127.0.0.1"
    REDIS_SERVER_PORT = 6379
    MONGO_SERVER_IP = "127.0.0.1"
    MONGO_SERVER_PORT = 27017

    def __init__(self, client=None, expires=timedelta(days=30)):
        """
        client: mongo database client
        expires: timedelta of amount of time before a cache entry is considered expired
        """
        # *************
        #    mongo    *
        # *************
        # 如果实例化的时候没有传递client就使用本地的client
        self.client = MongoClient(self.MONGO_SERVER_IP, self.MONGO_SERVER_PORT) if client is None else client
        # 创建一个集合来缓存URL数据
        self.db = self.client.cqc_process_crawl
        #
        if self.db.cqc.count() is 0:
            self.db.cqc.create_index('status')

        # *************
        #    redis    *
        # *************
        self.redis_client = redis.StrictRedis(host=self.REDIS_SERVER_IP, port=self.REDIS_SERVER_PORT, db=0)

    def enqueueUrl(self, url, status, depth):
        """往数据库添加数据"""

        # *************
        #    redis    *
        # *************
        num = self.redis_client.get(url)
        if num is not None:
            self.redis_client.set(url, int(num) + 1)
            print "【info】：{0} 在Redis中已经存在~~~".format(url)
            return  # 如果redis中已经存在直接返回
        # 不存在则设置值并加入到mongo中
        self.redis_client.set(url, 1)

        # *************
        #    mongo    *
        # *************
        md5_tag = hashlib.md5(url).hexdigest()
        record = {
            'url': url,
            'status': status,
            'depth': depth,
            'queue_time': datetime.utcnow(),
            'done_time': datetime.utcnow(),
        }
        try:
            self.db.cqc.insert({'_id': md5_tag})
            self.db.cqc.update({"_id": md5_tag}, {'$set': record})
        except errors.DuplicateKeyError as err:  # 当数据库中已经存在URL的时候通过try except来捕获异常
            print "【INFO】：函数 enqueueUrl() {0} 已存在~~~~ {1}".format(url, err)

    def dequeueUrl(self):
        """取数据"""
        record = self.db.cqc.find_one_and_update(
            {'status': 'new'},  # 取出第一条new状态的数据
            {'$set': {'status': 'downloading'}},  # 将数据修改为downloading状态
            {'upsert': False, 'returnNewDocument': False}
        )
        # 存在返回数据，不存在返回None
        if record:
            return record
        else:
            return None

    def finishUrl(self, url):
        """设置done状态"""
        md5_tag = hashlib.md5(url).hexdigest()
        record = {'status': 'done', 'done_time': datetime.utcnow()}
        self.db.cqc.update({'_id': md5_tag}, {'$set': record}, upsert=False)

    def clear(self):
        self.db.cqc.drop()


if __name__ == "__main__":
    test_redismgr = MongoRedisUrlManager()
    print "添加数据测试"
    test_redismgr.enqueueUrl(url="http://cuiqingcai.com/", status='new', depth=0)
    time.sleep(10)
    print "取数据测试"
    print test_redismgr.dequeueUrl()
    time.sleep(15)
    print "设置done状态测试"
    test_redismgr.finishUrl(url="http://cuiqingcai.com/")
    time.sleep(15)
    print "清理数据库"
    test_redismgr.clear()
