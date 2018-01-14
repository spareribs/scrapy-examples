#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/1 20:09
# @Author  : Aries
# @File    : get_lagou_job.py
# @Software: PyCharm

import json
import requests

url = "https://www.lagou.com/jobs/positionAjax.json"

querystring = {
    "city": "广州",
    "needAddtionalResult": "false",
    "isSchoolJob": "0"
}
headers = {
    'Referer': "https://www.lagou.com/jobs/list_爬虫?city=广州&cl=false&fromSearch=true&labelWords=&suginput=",
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
}

for page in range(1, 20):
    print "------------page:{0}".format(page)
    file_dict = {
        "first": (None, "true"),
        "pn": (None, "{0}".format(page)),
        "kd": (None, "爬虫")
    }
    response = requests.request("POST", url, files=file_dict, headers=headers, params=querystring)
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
    if len(response_body["content"]["positionResult"]["result"]) < 15:
        break
