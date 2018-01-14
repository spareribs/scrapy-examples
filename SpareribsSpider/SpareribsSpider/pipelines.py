# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline


class SpareribsspiderPipeline(object):
    def process_item(self, item, spider):
        return item


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
