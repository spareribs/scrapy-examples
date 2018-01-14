#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/1 20:09
# @Author  : Aries
# @File    : get_bosszp_job.py
# @Software: PyCharm

import re
import sys
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
headers = {
    'user-agent': agent
}

url = "https://www.zhipin.com/c101280100/h_101280100/"
for page in range(1, 20):
    querystring = {
        "query": "爬虫",
        "page": "{0}".format(page),
        "ka": "page-{0}".format(page)
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    # print response.text
    soup = BeautifulSoup(response.text, "lxml")
    tag_pachong = 15
    for tag_div in soup.find_all("div", "job-primary"):
        print tag_div.find("h3").get_text()
        print "https://www.zhipin.com/" + str(tag_div.find("h3").find("a").get("href"))
        if 1:
            tag_pachong -= 1
    if tag_pachong == 0:
        break
