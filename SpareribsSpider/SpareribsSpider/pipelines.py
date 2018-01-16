# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
from scrapy.pipelines.images import ImagesPipeline


class SpareribsspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        """当Spider关闭的时候，会顺便关闭文件"""
        self.file.close()


class ArticleImagesPipeline(ImagesPipeline):
    """
    # Two import def
    def get_media_requests(self, item, info):
    def item_completed(self, results, item, info):
    """

    def item_completed(self, results, item, info):
        for ok, value in results:
            iamge_file_path = value["path"]
        item["front_images_path"] = iamge_file_path
        return item
