# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request


class MmonlySpider(scrapy.Spider):
    name = 'mmonly.cc'

    categories = ['bjnmn', 'ctmn', 'hgmn', 'mnmx', 'nymn', 'qcmn', 'swmn', 'wgmv', 'xgmn']

    def start_requests(self):
        for category in self.categories:
            yield Request(url='http://mmonly.cc/mmtp/%s/' % (category), callback=self.parse_category_list)

    def parse_category_list(self, response):
        list_item_tags = response.css('div.item_list > div.item div.ABox a')
        for list_item_tag in list_item_tags:
            list_items_src = list_item_tag.css('::attr(href)').extract_first()
            if not list_items_src:
                continue
            list_items_src = response.urljoin(list_items_src)
            yield Request(url=list_items_src, callback=self.parse_category_list_item)

        pagination_tags = response.css('div#pageNum a')
        for pagination_tag in pagination_tags:
            page_src = pagination_tag.css('::attr(href)').extract_first()
            if not page_src:
                continue
            page_src = response.urljoin(page_src)
            yield Request(url=page_src, callback=self.parse_category_list)

    def parse_category_list_item(self, response):
        image_tags = response.css('div#big-pic img')
        for image_tag in image_tags:
            image_src = image_tag.css('::attr(src)').extract_first()
            image_title = image_tag.css('::attr(alt)').extract_first()
            source_url = response.url
            if not image_src or not image_title:
                continue
            yield {
                'image_urls': [image_src],
                'image_title': image_title,
                'source_url': source_url
            }

        pagination_tags = response.css('div.pages > ul > li > a')
        for pagination_tag in pagination_tags:
            page_src = pagination_tag.css('::attr(href)').extract_first()
            if not page_src:
                continue
            page_src = response.urljoin(page_src)
            yield Request(url=page_src, callback=self.parse_category_list_item)
