#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/6/21 20:01
# @Author  : Spareribs
# @File    : process_dbmanager.py
"""

import mysql.connector  # Windows pip install mysql-connector==2.1.6 2017.06.21测试可用
import hashlib
from mysql.connector import errorcode


class CrawlDatabaseManager:
    DB_NAME = 'mfw_pro_crawl'

    SERVER_IP = 'localhost'

    TABLES = {}
    # 创建数据表的SQL命令
    TABLES['urls'] = (
        "CREATE TABLE `urls` ("
        "  `index` int(11) NOT NULL AUTO_INCREMENT,"  # 队列的索引
        "  `url` varchar(512) NOT NULL,"
        "  `md5` varchar(16) NOT NULL,"
        "  `status` varchar(11) NOT NULL DEFAULT 'new',"  # {new,downloading,finish} 三种状态
        "  `depth` int(11) NOT NULL,"
        "  `queue_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,"  # update或者insert的时候更新时间
        "  `done_time` timestamp NOT NULL DEFAULT 0 ON UPDATE CURRENT_TIMESTAMP,"  # update的时候更新时间
        "  PRIMARY KEY (`index`),"
        "  UNIQUE KEY `md5` (`md5`)"
        ") ENGINE=InnoDB")

    def __init__(self, max_num_thread):
        """初始化：包括创建数据库和数据表"""
        try:
            cnx = mysql.connector.connect(host=self.SERVER_IP, user='root')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print "Database does not exist"
            else:
                print 'Create Error ' + err.msg
            exit(1)

        cursor = cnx.cursor()

        # use database, create it if not exist
        try:
            cnx.database = self.DB_NAME
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                # 创建数据库和数据表
                self.create_database(cursor)
                cnx.database = self.DB_NAME
                self.create_tables(cursor)
            else:
                print err
                exit(1)
        finally:
            cursor.close()
            cnx.close()

        dbconfig = {
            "database": self.DB_NAME,
            "user": "root",
            "host": self.SERVER_IP,
        }
        self.cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool",
                                                                   pool_size=max_num_thread,
                                                                   **dbconfig)

    # create databse
    def create_database(self, cursor):
        """创建数据库"""
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.DB_NAME))
        except mysql.connector.Error as err:
            print "Failed creating database: {}".format(err)
            exit(1)

    def create_tables(self, cursor):
        """创建数据表"""
        for name, ddl in self.TABLES.iteritems():
            try:
                cursor.execute(ddl)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print 'create tables error ALREADY EXISTS'
                else:
                    print 'create tables error ' + err.msg
            else:
                print 'Tables created'

    def enqueueUrl(self, url, depth):
        """将url加入到数据库中"""
        con = self.cnxpool.get_connection()
        cursor = con.cursor()
        try:
            add_url = ("INSERT INTO urls (url, md5, depth) VALUES (%s, %s, %s)")
            data_url = (url, hashlib.md5(url).hexdigest(), depth)
            cursor.execute(add_url, data_url)
            # 将操作提交到数据库【提交事务】
            con.commit()
        except mysql.connector.Error as err:
            # print 'enqueueUrl() ' + err.msg
            return
        finally:
            cursor.close()
            con.close()

    def dequeueUrl(self):
        """将url加入到数据库中获取一个status为new的url"""
        con = self.cnxpool.get_connection()
        cursor = con.cursor(dictionary=True)
        try:
            # 使用 select * for update 方法加入读锁并读取
            query = (
                "SELECT `index`, `url`, `depth` FROM urls WHERE status='new' ORDER BY `index` ASC LIMIT 1 FOR UPDATE")
            cursor.execute(query)
            if cursor.rowcount is 0:
                return None
            row = cursor.fetchone()
            update_query = ("UPDATE urls SET `status`='downloading' WHERE `index`=%d") % (row['index'])
            cursor.execute(update_query)
            con.commit()
            return row
        except mysql.connector.Error as err:
            # print 'dequeueUrl() ' + err.msg
            return None
        finally:
            cursor.close()
            con.close()

    def finishUrl(self, index):
        """当完成下载的时候通过行级锁将当前的url的status设置为done"""
        con = self.cnxpool.get_connection()
        cursor = con.cursor()
        try:
            # 更新问done的时候，系统会自动刷新数据库时间time.strftime('%Y-%m-%d %H:%M:%S')
            update_query = ("UPDATE urls SET `status`='done' WHERE `index`=%d") % (index)
            cursor.execute(update_query)
            con.commit()
        except mysql.connector.Error as err:
            # print 'finishUrl() ' + err.msg
            return
        finally:
            cursor.close()
            con.close()
