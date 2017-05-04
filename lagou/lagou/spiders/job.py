#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/5/3 13:52
# @Author  : Spareribs
# @File    : job.py
"""
import scrapy
import json
from scrapy.http import Request


class JobSpider(scrapy.Spider):
    name = "job"
    allow_domains = ['lagou.com']
    headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.01", }
    cookies = {"user_trace_token": "20170502200739-07d687303c1e44fa9c7f0259097266d6", }
    work_tag = "python"

    def start_requests(self):
        base_url = "https://www.lagou.com/jobs/list_{0}?" \
                   "city=%E5%B9%BF%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput=".format(self.work_tag)

        yield Request(base_url, headers=self.headers, cookies=self.cookies, callback=self.parse_getpages)

    def parse_getpages(self, response):
        pages = response.xpath("//*[@id='tab_pos']/span/text()").extract()[0]

        for page in range(1, (int(pages) / 15 + 2)):
            base_url = "https://www.lagou.com/jobs/positionAjax.json?" \
                       "city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false&kd={0}&pn={1}".format(self.work_tag, page)
            yield Request(base_url, headers=self.headers, cookies=self.cookies)

    def parse(self, response):
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
