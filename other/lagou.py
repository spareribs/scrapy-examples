#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/5/2 20:24
# @Author  : Spareribs
# @File    : test_lagou.py
"""


import requests
import json

url = "https://www.lagou.com/jobs/positionAjax.json"

querystring = {"city":"广州","needAddtionalResult":"false","kd":"python","pn":"1"}

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
    'cookie': "user_trace_token=20170502200739-07d687303c1e44fa9c7f0259097266d6;"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
print json.dumps(response.text)