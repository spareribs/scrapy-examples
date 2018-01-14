# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpareribsspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobBoleAticaleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_objtct_id = scrapy.Field()
    tags = scrapy.Field()
    front_images_url = scrapy.Field()
    front_images_path = scrapy.Field()
    create_date = scrapy.Field()
    content = scrapy.Field()
    prasise_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    commonts_nums = scrapy.Field()
