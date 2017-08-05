# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

'''定义要抓取的列'''
class KaolaItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    sku = scrapy.Field()
    name = scrapy.Field()
    type_id = scrapy.Field()
    attribute_set = scrapy.Field()
    category_ids = scrapy.Field()
    short_description = scrapy.Field()
    description = scrapy.Field()
    qty = scrapy.Field()
    price = scrapy.Field()
    special_price = scrapy.Field()
    tax_class_id = scrapy.Field()
    weight = scrapy.Field()
    image = scrapy.Field()
    gallery = scrapy.Field()
    country = scrapy.Field()
    brand = scrapy.Field()
    vendor_code = scrapy.Field()
    warehouse = scrapy.Field()
    product_sync_type = scrapy.Field()
    warehouse_city = scrapy.Field()
    warehouse_alias = scrapy.Field()
    custom1 = scrapy.Field()
    custom2 = scrapy.Field()
    custom3 = scrapy.Field()
    pass
