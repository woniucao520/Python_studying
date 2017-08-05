# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    sku = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    type_id = scrapy.Field()
    price = scrapy.Field()
    images = scrapy.Field()
    image = scrapy.Field()
    gallery = scrapy.Field()
    description = scrapy.Field()
    qty = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()
    weight = scrapy.Field()
    tax_class_id = scrapy.Field()
    short_description = scrapy.Field()
    attribute_set = scrapy.Field()
    category_ids = scrapy.Field()
    pass
