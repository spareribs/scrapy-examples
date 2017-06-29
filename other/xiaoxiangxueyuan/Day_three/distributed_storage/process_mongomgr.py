#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/6/28 17:24
# @Author  : Spareribs
# @File    : process_mongomgr.py
"""

from pymongo import MongoClient
from pymongo import errors
from datetime import datetime, timedelta


class MongoUrlManager:
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 27017

    def __init__(self, client=None, expires=timedelta(days=30)):
        """
        client: mongo database client
        expires: timedelta of amount of time before a cache entry is considered expired
        """
        # if a client object is not passed
        # then try connecting to mongodb at the default localhost port
        self.client = MongoClient(self.SERVER_IP, self.SERVER_PORT) if client is None else client
        # create collection to store cached webpages,
        # which is the equivalent of a table in a relational database
        self.db = self.client.cqc_process_crawl  # 指定一个爬虫数据库spider，类似于创建数据库

    def enqueueUrl(self, url, status, depth):
        """往数据库添加数据"""
        record = {
            'url': url,
            'depth': depth,
            'status': status,
            'queue_time': datetime.utcnow(),
            'done_time': datetime.utcnow(),
        }
        try:

            self.db.url.insert({"_id": url})  # 先插入_id
            self.db.url.update({"_id": url}, {'$set': record})  # 再根据_id更新数据
        except errors.DuplicateKeyError as err:  # 当数据库中已经存在URL的时候通过try except来捕获异常
            print "【INFO】：函数 enqueueUrl() {0} 已存在~~~~ {1}".format(url, err)

    def dequeueUrl(self):
        """取数据"""
        record = self.db.url.find_one_and_update(
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
        record = {'status': "done", 'done_time': datetime.utcnow()}
        self.db.url.update({'_id': url}, {'$set': record}, upsert=False)

    def clear(self):
        self.db.url.drop()


if __name__ == "__main__":
    """main函数部分是测试代码，用于当前脚本的测试，其他脚本导入时不执行"""
    test_mongomgr = MongoUrlManager()
    print "添加数据测试"
    test_mongomgr.enqueueUrl(url="http://cuiqingcai.com/", status='new', depth=0)
    print "取数据测试"
    print test_mongomgr.dequeueUrl()
    print "设置done状态测试"
    test_mongomgr.finishUrl(url="http://cuiqingcai.com/")
    test_mongomgr.clear()

