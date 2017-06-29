#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/6/28 19:21
# @Author  : Spareribs
# @File    : process_cuiqinghua_crawl_mongo.py
# @Notice  : 宽度优先算法BSF实现的全站爬取的爬虫-多进程(mongo)
"""
import os
import urllib2
from lxml import etree
import httplib
import threading
import time
from process_mongomgr import MongoUrlManager

request_headers = {
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
}


def getPageContent(now_url, now_depth):
    print "【Download】正在下载网址 {0} 当前深度为 {1}".format(now_url, now_depth)
    max_depth = 2  # 爬取深度
    try:
        # 使用urllib库请求now_url地址，将页面通过read方法读取下来
        req = urllib2.Request(now_url, headers=request_headers)
        response = urllib2.urlopen(req)
        html_page = response.read()

        filename = now_url[7:].replace('/', '_')  # 处理URL信息，去掉"http://"，将/替换成_

        # 将获取到的页面写入到文件中
        fo = open("{0}{1}.html".format(dir_name, filename), 'wb+')
        fo.write(html_page)
        fo.close()

        # 【mongomgr.finishUrl】当完成下载的时候通过行级锁将当前的url的status设置为done
        mongomgr.finishUrl(now_url)

    # 处理各种异常情况
    except urllib2.HTTPError, Arguments:
        print "【Error】:HTTPError {0}\n".format(Arguments)
        return
    except httplib.BadStatusLine, Arguments:
        print "【Error】:BadStatusLine {0}\n".format(Arguments)
        return
    except IOError, Arguments:
        print "【Error】:IOError {0}\n".format(Arguments)
        return
    except Exception, Arguments:
        print "【Error】:Exception {0}\n".format(Arguments)
        return

    # 解析页面，获取当前页面中所有的URL
    try:
        html = etree.HTML(html_page.lower().decode('utf-8'))
        hrefs = html.xpath(u"//a")
        for href in hrefs:
            # 用于处理xpath抓取到的href，获取有用的
            try:
                if 'href' in href.attrib:
                    val = href.attrib['href']
                    if val.find('javascript:') != -1:  # 过滤掉类似"javascript:void(0)"
                        continue
                    if val.startswith('http://') is False:  # 给"/mdd/calendar/"做拼接
                        if val.startswith('/'):
                            val = 'http://cuiqingcai.com'.format(val)
                        else:
                            continue
                    if val[-1] == '/':  # 过滤掉末尾的/
                        val = val[0:-1]
                    if now_depth + 1 == max_depth:  # 如果深度与设定的最大深度相等，不加入数据库
                        break
                    else:
                        mongomgr.enqueueUrl(val, 'new', now_depth + 1)  # 【mongomgr.enqueueUrl】将url加入到数据库中

            except ValueError:
                continue
    except UnicodeDecodeError:  # 处理utf-8编码无法解析的异常情况
        pass


# 记录文件（存放下载的HTML页面）
dir_name = 'test_cuiqingcai/'
if not os.path.exists(dir_name):  # 检查用于存储网页文件夹是否存在，不存在则创建
    os.makedirs(dir_name)

# 实例化一个数据库操作对象（功能与queue类似），并指定指定最大的进程数
max_num_thread = 10
mongomgr = MongoUrlManager()

# 将首页面存入queue(数据库)
mongomgr.enqueueUrl("http://cuiqingcai.com/", 'new', 0)

start_time = time.time()  # 记录开始时间
is_root_page = True  # 标记首页
threads = []  # 创建进程池

CRAWL_DELAY = 0  # 设置超时，控制下载的速率，避免太过频繁访问目标网站,但目标网站没有这个限制

while True:
    curtask = mongomgr.dequeueUrl()  # 【mongomgr.dequeueUrl】将url加入到数据库中获取一个status为new的url
    if curtask is None:
        for t in threads:  # join方法，等待所有线程结束以后再继续执行【等待子进程结束，再退出主进程】
            t.join()
        break

    # looking for an empty thread from pool to crawl
    if is_root_page is True:  # 修改根目录URL的标记，并抓取首页，让数据库里面有初始数据
        getPageContent(curtask['url'], curtask['depth'])
        is_root_page = False
    else:
        while True:
            for t in threads:  # 处理掉异常而终止【非存活】的进程
                if not t.is_alive():
                    threads.remove(t)
            if len(threads) >= max_num_thread:  # 如果当前线程大于预设值，continue不执行后面的代码，继续循环，知道小于预设值
                # time.sleep(CRAWL_DELAY)
                continue  # len(threads) >= max_threads的判断左右
            try:  # 创建线程 加入线程池 并启动线程
                t = threading.Thread(target=getPageContent, name=None, args=(curtask['url'], curtask['depth']))
                threads.append(t)  # 将线程加入线程池中
                t.setDaemon(True)  # 设置 Ctrl-C 能退出thread的爬取【不等待子进程结束，直接退出主进程】
                t.start()  # 启动线程
                # time.sleep(CRAWL_DELAY)
                break
            except Exception:
                print "【Error】: 不能启动thread"

print '【End】 花费时间 {0:.2f} 秒'.format(time.time() - start_time)
