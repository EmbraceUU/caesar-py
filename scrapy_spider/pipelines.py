# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy_spider.items import SpiderItem
import logging

logger = logging.getLogger(__name__)


class SpiderPipeline(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process_item(self, item, spider):
        if isinstance(item, SpiderItem):
            print(item.values())
        return item

    def close_spider(self, spider):
        pass
