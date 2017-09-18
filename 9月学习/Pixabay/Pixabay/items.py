# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PixabayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sku = scrapy.Field()
    name = scrapy.Field()
    image = scrapy.Field()
    gallery = scrapy.Field()
    qty = scrapy.Field()
    links = scrapy.Field()
    image_url = scrapy.Field()
    description = scrapy.Field()

