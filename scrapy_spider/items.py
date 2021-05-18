# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docorg/en/latest/topics/itemshtml

from scrapy import Item, Field


class SpiderItem(Item):
    author = Field()
    content = Field()
    release_time = Field()
    title = Field()
    plate = Field()
    source = Field()
    url = Field()
    tags = Field()
    hash_id = Field()
