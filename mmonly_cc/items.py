# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MmonlyCcItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    source_url = scrapy.Field()
    category = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()
