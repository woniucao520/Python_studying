# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WorkjobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    zwyx = scrapy.Field() #月薪
    gzdd = scrapy.Field() #工作地点
    fbtime = scrapy.Field() #发布时间
    experence = scrapy.Field() # 经验
    totalnum = scrapy.Field() # 招聘人数
