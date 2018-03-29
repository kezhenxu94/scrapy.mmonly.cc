# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class MmonlyCcPipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        return [Request(x, meta={
            'item': item
        }) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        super_file_path = super(MyImagesPipeline, self).file_path(request, response, info)

        if 'item' not in request.meta:
            return super_file_path

        item = request.meta['item']

        if 'title' not in item:
            return super_file_path

        if 'category' not in item:
            return super_file_path

        title = item['title']
        category = item['category']

        return '%s/%s/%s' % (category, title, super_file_path.replace('full/', ''))
