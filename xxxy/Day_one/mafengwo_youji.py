#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/6/12 19:22
# @Author  : Spareribs
# @File    : mafengwo_youji.py
# @Notice  : 这是一个有针对性（特定内容）的全站爬虫


www.mafengwo.cn网站分析
1. 所有的游记都位于www.mafengwo.cn/mdd【按照城市进行分类】
2. 城市首页：http://www.mafengwo.cn/travel-scenic-spot/mafengwo/10065.html【10065城市编码不一样】
3. 游记分页格式：http://www.mafengwo.cn/yj/10065/1-0-01.html【10065城市编码不一样；1-0-01页码不一样】
4. 游记的页面：http://www.mafengwo.cn/i/6950645.html【6950645游记的编号不一样】
"""

import time
import urllib2
import httplib
import re
from pybloom import BloomFilter
import os

# 定义请求的头部
request_headers = {
    'host': "www.mafengwo.cn",
    'connection': "keep-alive",
    'cache-control': "no-cache",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6"
}

city_home_pages = []  # 记录城市编码和城市的名字
city_ids = []  # 城市编码

dirname = 'mafengwo_notes/'
if not os.path.exists(dirname):  # 检查用于存储网页文件夹是否存在，不存在则创建
    os.makedirs(dirname)

# 创建 BloomFilter 对象
download_bf = BloomFilter(1024 * 1024 * 16, 0.01)


def download_city_notes(city_id, name):
    for notes_count in range(1, 999):

        url = "http://www.mafengwo.cn/yj/{0}/1-0-{1}.html".format(city_id, notes_count)
        if url in download_bf:
            continue
        print "【Get】当前正在获取 {0} 页面".format(url)
        download_bf.add(url)
        req = urllib2.Request(url, headers=request_headers)
        response = urllib2.urlopen(req)
        htmlcontent = response.read()

        city_notes = re.findall('href="/i/\d{7}.html', htmlcontent)
        if len(city_notes) == 0:  # 如果导航页错误，该页的游记数为0，则意味着 1-0-xxx.html 已经遍历完，结束这个城市
            return
        for city_note in city_notes:
            time.sleep(2)  # 降低爬取速度，防止被墙
            try:
                city_url = 'http://www.mafengwo.cn{0}'.format(city_note[6:])
                print "【Download】当前正在下载 {0} 页面".format(city_url)
                if city_url in download_bf:
                    print "【Skip】已经爬取 {0} 跳过".format(city_url)
                    continue
                print "【Download】当前正在下载 {0} 页面".format(city_url)
                req = urllib2.Request(city_url, headers=request_headers)
                response = urllib2.urlopen(req)
                html = response.read()
                filename = city_url[7:].replace('/', '_')
                fo = open("%s%s" % (dirname, filename), 'wb+')
                fo.write(html)
                fo.close()
                download_bf.add(city_url)
            except Exception, Arguments:
                print "【Error】:{0}\n".format(Arguments)
                continue


try:
    # 下载http://www.mafengwo.cn/mdd/页面获取所有城市的编号和连接
    req = urllib2.Request('http://www.mafengwo.cn/mdd/', headers=request_headers)
    response = urllib2.urlopen(req)
    htmlcontent = response.read()  # 得到一个str格式的html文件

    # 利用正则表达式，找出所有的城市主页
    city_home_pages = re.findall('/travel-scenic-spot/mafengwo/(\d{5}).html" target="_blank">(.*?)<', htmlcontent)

    # 通过循环，依次下载每个城市下的所有游记
    for city in city_home_pages:
        city_ids.append(city[0])
        download_city_notes(city[0], city[1])

# 异常处理
except urllib2.HTTPError, Arguments:
    print "【Error】:{0}\n".format(Arguments)
except httplib.BadStatusLine:
    print "【Error】:{0}\n".format('BadStatusLine')
except Exception, Arguments:
    print "【Error】:{0}\n".format(Arguments)
