# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from mmonly_cc.items import MmonlyCcItem

import re
import datetime


class MmonlySpider(CrawlSpider):
    name = 'mmonly'
    allowed_domains = ['mmonly.cc']
    start_urls = ['http://mmonly.cc/mmtp/']
    rules = [
        Rule(link_extractor=LinkExtractor(allow='.*/mmtp/.*/\d+(_\d+)?\.html'), callback='parse_item'),
        Rule(link_extractor=LinkExtractor(allow='.*/mmtp/.*/(list_\d+_\d+\.html)?'))
    ]

    def parse_item(self, response):
        title_tags = response.css('div.imgtitle h1')

        if not title_tags:
            return

        title_tag = title_tags[0]
        title = title_tag.css('::text').extract_first()
        title = re.sub('\(\d+/\d+\)$', '', title)

        image_tags = response.css('#big-pic img')

        if not image_tags:
            return

        image_tag = image_tags[0]

        image_url = image_tag.css('::attr(src)').extract_first()
        image_url = response.urljoin(image_url)

        matcher = re.match(ur'.*/mmtp/(?P<category>\w+)/.*', response.url)
        category = matcher.group('category') if matcher else ''

        mmonly_cc_item = MmonlyCcItem(
            title=title,
            image_urls=[image_url],
            source_url=response.url,
            category=category,
            updated_at=datetime.datetime.now()
        )

        yield mmonly_cc_item
