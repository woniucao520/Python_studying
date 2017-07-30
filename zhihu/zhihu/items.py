# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):

    answer_count = scrapy.Field()
    articles_count = scrapy.Field()
    headline = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    url_token = scrapy.Field()
    follower_count = scrapy.Field()

