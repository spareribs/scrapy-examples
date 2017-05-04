#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/5/2 20:24
# @Author  : Spareribs
# @File    : test_lagou.py
"""
import json
import requests
from bs4 import BeautifulSoup

url = "https://www.lagou.com/jobs/list_python"
querystring = {"city": "广州", "cl": "false", "fromSearch": "true", "labelWords": "", "suginput": ""}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
    'cookie': "user_trace_token=20170502200739-07d687303c1e44fa9c7f0259097266d6;",
}
response = requests.request("GET", url, headers=headers, params=querystring)
soup = BeautifulSoup(response.text, "lxml")
pages = soup.find_all("a", id="tab_pos")[0].find("span").get_text()

url = "https://www.lagou.com/jobs/positionAjax.json"
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
    'cookie': "user_trace_token=20170502200739-07d687303c1e44fa9c7f0259097266d6;"
}
for page in range(1, (int(pages) / 15 + 2)):
    querystring = {"city": "广州", "needAddtionalResult": "false", "kd": "python", "pn": "{0}".format(page)}
    response = requests.request("GET", url, headers=headers, params=querystring)
    response_body = json.loads(response.text)
    for compony in response_body["content"]["positionResult"]["result"]:
        print "*" * 40
        print "公司编号" + str(compony["companyId"])
        print compony["positionName"]
        print compony["workYear"]
        print compony["education"]
        print compony["positionId"]
        print compony["salary"]
        print compony["companyFullName"]
