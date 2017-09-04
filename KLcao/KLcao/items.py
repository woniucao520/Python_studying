# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KlcaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    sku = scrapy.Field()
    name = scrapy.Field()
    country = scrapy.Field()
    price = scrapy.Field()
    warehouseNameAlias = scrapy.Field()
    gallery = scrapy.Field()
    img_description = scrapy.Field()

    pass
