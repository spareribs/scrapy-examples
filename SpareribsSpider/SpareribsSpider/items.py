# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

# scrapy-plugins：将Items转化成djangoitem，ORM机制 方便对数据的操作
# https://github.com/scrapy-plugins/scrapy-djangoitem

import datetime
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class SpareribsspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value + "-spareribs"


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date


class JobBoleAticleItem(scrapy.Item):
    """
    使用MapCompose对数据进行预处理
    """
    title = scrapy.Field(
        input_processor=MapCompose(lambda x: x + "-jobbole", add_jobbole)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    tags = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
        output_processor=TakeFirst()
    )
    content = scrapy.Field()
    praise_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    comment_nums = scrapy.Field()
