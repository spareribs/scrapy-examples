# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql
from scrapy.conf import settings


def dbHandle():
    conn = pymysql.connect(
        host=settings['MYSQL_HOST'],
        db=settings['MYSQL_DBNAME'],
        user=settings['MYSQL_USER'],
        passwd=settings['MYSQL_PASSWD'],
        charset='utf8',
        use_unicode=False
    )
    return conn


class CuiqingcaiPipeline(object):
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        sql = 'insert into cqc.blog(title,url) values (%s,%s)'

        try:
            cursor.execute(sql, (item['title'], item['url']))
            dbObject.commit()
        except Exception, e:
            print e
        return item
        # print item


class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('cqcall.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
