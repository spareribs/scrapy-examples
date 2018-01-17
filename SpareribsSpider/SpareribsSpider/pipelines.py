# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter


class SpareribsspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        """当Spider关闭的时候，会顺便关闭文件"""
        self.file.close()


class JsonExporterPipleline(object):
    # 调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def spider_close(self, spider):
        """当Spider关闭的时候，会顺便关闭文件"""
        self.exporter.finish_exporting()
        self.file.close()


class MysqlPipeline(object):
    """
    采用同步的机制 实现插入数据到mysql
    """

    def __init__(self):
        """"""
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        """注意数据库的名字和插入的值（特别是not null的情况）"""
        insert_sql = """
            insert into article(title, url, create_date, fav_nums)
            VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))
        self.conn.commit()


class MysqlTwistedPipline(object):
    """
    Twisted异步 实现插入数据到mysql
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """获取settings文件的内容"""
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        """使用twisted将mysql插入变成异步执行"""
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 使用addErrback函数对query进行异常处理
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        """处理异步插入的异常"""
        print (failure)

    def do_insert(self, cursor, item):
        """
        执行具体的插入
        根据不同的item 构建不同的sql语句并插入到mysql中
        其他都是固定逻辑，主要是do_insert函数逻辑不同而已
        """
        insert_sql = """
                    insert into article(title, url, create_date, fav_nums)
                    VALUES (%s, %s, %s, %s)
                """
        cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))


class ArticleImagesPipeline(ImagesPipeline):
    """
    # Two import def
    def get_media_requests(self, item, info):
    def item_completed(self, results, item, info):
    """

    def item_completed(self, results, item, info):
        for ok, value in results:
            iamge_file_path = value["path"]
        item["front_images_path"] = iamge_file_path
        return item
