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
    label_tags = ['爬虫', 'scrapy', 'selenium']

    rules = (
        Rule(LinkExtractor(allow=('\d+\.html$',)), callback='parse_all', follow=True),
        # Rule(LinkExtractor(allow=('\d+\.html$',)), callback='parse_pachong', follow=True),
        # Rule(LinkExtractor(allow=('\.html',)), callback='parse_all', follow=True),
    )

    # 将爬虫相关的数据存入数据库
    def parse_pachong(self, response):
        print_tag = False
        title_name = u""
        for tag in self.label_tags:
            title_name = response.xpath('//header/h1[1][@class="article-title"]/a/text()').extract()[0]
            if tag in title_name.lower().encode("utf-8"):
                print_tag = True
        if print_tag == True:
            self.count_all = self.count_all + 1
            self.url_all.append(response.url)
            item = CuiqingcaiItem()
            item['url'] = response.url
            item['title'] = title_name.encode("utf-8")
            return item

    # 将全站数据存入json文件
    def parse_all(self, response):
        title_name = None
        if response.xpath('//header/h1[1][@class="article-title"]/a/text()').extract()[0]:
            title_name = response.xpath('//header/h1[1][@class="article-title"]/a/text()').extract()[0]
        item = CuiqingcaiItem()
        item['url'] = response.url
        item['title'] = title_name
        return item
