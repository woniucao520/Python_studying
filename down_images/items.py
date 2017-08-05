# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TupianItem(scrapy.Item):
    # define the fields for your item here like:
    sku = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    qty = scrapy.Field()
    attribute_set = scrapy.Field()
    category_ids = scrapy.Field()
    tax_class_id = scrapy.Field()
    images = scrapy.Field()
    type = scrapy.Field()
    weight = scrapy.Field()
    links = scrapy.Field()
    image_url = scrapy.Field()
    pass
