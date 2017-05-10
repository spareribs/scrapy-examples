# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_id = scrapy.Field()
    position_name = scrapy.Field()
    work_year = scrapy.Field()
    education = scrapy.Field()
    position_id = scrapy.Field()
    salary = scrapy.Field()
    cmpany_full_name = scrapy.Field()
    pass
