#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/1 20:09
# @Author  : Aries
# @File    : get_qcwy_job.py
# @Software: PyCharm

import sys
import time
import datetime
import requests
from bs4 import BeautifulSoup
from urllib import quote

reload(sys)
sys.setdefaultencoding('utf-8')

agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
headers = {'user-agent': agent, }


def keywork_urlencode(keyword):
    return quote(quote(keyword))


def search_job(url, headers):
    response = requests.request("GET", url, headers=headers)
    # 需要对response返回的内容进行解码
    gbk_to_unicode = response.content.decode("gbk")
    soup = BeautifulSoup(gbk_to_unicode, "lxml")
    return soup


def get_all_jobs(soup):
    # print soup
    for tag_p in soup.find_all("p", "t1"):
        # 将获取到的岗位和详细URL输出
        print tag_p.find("a").get_text().replace(' ', ''), tag_p.find("a").get("href")
    return int(len(soup.find_all("p", "t1")))


def main(keywork):
    print "Start~~~"
    for page in range(1, 20):
        print "------------page:{0}".format(page)
        url = "http://search.51job.com/list/030200,000000,0000,00,9,99,{0},2,{1}.html".format(keywork_urlencode(keywork), page)
        soup = search_job(url, headers)
        if get_all_jobs(soup) < 50:
            print get_all_jobs(soup)
            break
    print "End~~~"


if __name__ == "__main__":
    main("爬虫")
