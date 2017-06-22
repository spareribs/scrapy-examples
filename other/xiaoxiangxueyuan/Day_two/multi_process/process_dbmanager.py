#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/6/21 20:01
# @Author  : Spareribs
# @File    : process_dbmanager.py
# @Notice  : 一个用于处理数据库的类
"""

import mysql.connector  # Windows pip install mysql-connector==2.1.6 2017.06.21测试可用
from mysql.connector import pooling
import hashlib
from mysql.connector import errorcode


class CrawlDatabaseManager(object):
    # 定义全局变量
    DB_USER = "root"
    DB_PASSWORD = "root"
    DB_PORT = "3306"
    DB_NAME = "cqc_process_crwal"
    SERVER_IP = "127.0.0.1"
    TABLES_NAME = "urls"  # 在TABLES创建的命令中也有定义

    # 创建数据表的SQL命令，存入到一个TABLES的字典当中
    TABLES = {'urls': (
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
        ") ENGINE=InnoDB"
    )}

    def __init__(self, max_num_thread=5):
        """初始化：包括创建数据库和数据表"""

        # 尝试连接数据库，如果连接不成功直接退出进程
        try:
            print "【Info】：尝试连接数据库 '{0}:{1}' ".format(self.SERVER_IP, self.DB_PORT)
            cnx = mysql.connector.connect(host=self.SERVER_IP, user=self.DB_USER, password=self.DB_PASSWORD)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print "【Error】: 用户名/密码错误~~~ {0}".format(err.msg)
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print "【Error】: 数据库不存在~~~ {0}".format(err.msg)
            else:
                print "【Error】：尝试连接数据库失败，请查看下进程（IP -> 端口 -> 服务）~~~ {0}".format(err.msg)
            exit(1)

        # 设置一个操作的游标
        cursor = cnx.cursor()

        # 如果数据库不存在的情况下，创建数据库
        try:
            cnx.database = self.DB_NAME  # 定义游标的数据库的名字
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(cursor)  # 创建数据库
                cnx.database = self.DB_NAME  # 定义游标的数据库的名字
                self.create_tables(cursor)  # 创建数据表
            else:
                print "【Error】：{0}".format(err)
                exit(1)
        finally:
            cursor.close()
            cnx.close()

        DBCONFIG = dict(database=self.DB_NAME, user=self.DB_USER, host=self.SERVER_IP, password=self.DB_PASSWORD)
        self.cnxpool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypoola", pool_size=max_num_thread, **DBCONFIG)

    def create_database(self, cursor):
        """创建数据库"""
        try:  # 执行创建数据表的命令
            print "【Info】：数据库[ {0} ]不存在，正在创建数据库...".format(self.DB_NAME)
            cursor.execute("CREATE DATABASE {0} DEFAULT CHARACTER SET 'utf8'".format(self.DB_NAME))
        except mysql.connector.Error as err:
            print "【Error】：创建数据库[ {1} ]失败{0}".format(err, self.DB_NAME)
            exit(1)

    def create_tables(self, cursor):
        """创建数据表"""
        for name, ddl in self.TABLES.iteritems():
            try:
                cursor.execute(ddl)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print '【Error】：创建表失败，表[ {0} ]已经存在~~~'.format(self.TABLES_NAME)
                else:
                    print '【Error】：创建表失败~~~ {0}'.format(err.msg)
            else:
                print '【Info】：表[ {0} ]不存在，正在创建数据表...'.format(self.TABLES_NAME)

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
            print 'enqueueUrl() ' + err.msg
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


if __name__ == "__main__":
    print "初始化开始"
    testdbmanaget = CrawlDatabaseManager()
    print "初始化完成"
    print "测试插入数据"
    # testdbmanaget.enqueueUrl("http://cuiqingcai.com/", 0)
    # print "测试读取数据"
