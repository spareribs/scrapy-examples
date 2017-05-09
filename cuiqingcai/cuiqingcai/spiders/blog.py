#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/5/9 16:41
# @Author  : Spareribs
# @File    : blog.py
"""

# CrawlSpider与Rule配合使用可以起到历遍全站的作用、Request干啥的我就不解释了
from scrapy.spiders import CrawlSpider, Rule, Request
# 配合Rule进行URL规则匹配
from scrapy.linkextractors import LinkExtractor
# Scrapy中用作登录使用的一个包
from scrapy import FormRequest

from cuiqingcai.items import CuiqingcaiItem


class myspider(CrawlSpider):
    name = 'cqc'
    allowed_domains = ['cuiqingcai.com']
    count_all = 0
    url_all = []
    start_urls = ['http://cuiqingcai.com']
    label_tags = ['爬虫', 'scrapy', 'selenium', 'selenium']

    rules = (
        Rule(LinkExtractor(allow=('\d+\.html$',)), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=('\.html',)), callback='parse_print', follow=True),
    )

    def parse_item(self, response):
        print_tag = False
        title_name = u""
        for tag in self.label_tags:
            title_name = response.xpath('//header/h1[1][@class="article-title"]/a/text()').extract()[0]
            if tag in title_name.lower().encode("utf-8"):
                print_tag = True
        if print_tag == True:
            self.count_all = self.count_all + 1
            self.url_all.append(response.url)
            # print response.url
            # print title
            with open("url.txt", "a+") as f:
                f.write("{0} {1}\n".format(response.url, title_name.encode("utf-8")))
            f.close()
            # print self.count_all
            # item = CuiqingcaiItem()
            # item['url'] = response.url
            # item['title'] = response.xpath('//header/h1[1][@class="article-title"]/a/text()').extract()[0]
            # return item

    def parse_print(self, response):
        # print(response.url)
        with open("url_all.txt", "a+") as f:
            f.write("{0}\n".format(response.url))
        f.close()
        # print self.url_all
        # print self.count_all

