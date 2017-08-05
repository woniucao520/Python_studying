# -*- coding: UTF-8 -*-

import scrapy
from scrapy.selector import HtmlXPathSelector
from tupian.items import TupianItem
from scrapy.http import Request
import json,requests,os,re
import logging

class TupianSpider(scrapy.Spider):

    name = "tupian"
    allowed_domains = ["pixabay.com","cdn.pixabay.com"]
    start_urls = []
    base_url = 'https://pixabay.com/zh/editors_choice/?media_type=photo&pagi='
    page_size = 1
    def __init__(self):
        logger = logging.getLogger('scrapy.spidermiddlewares.httperror')
        logger.setLevel(logging.ERROR)
        for i in range(self.page_size):
            self.start_urls.append(self.base_url+str(i))
        pass

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        urls = hxs.xpath('//*[@id="content"]/div/div/div/div/a/img/@data-lazy').extract()
        # product page
        items = []
        for url in urls:
            name_url = url.split('/',-1)[-1]
            name = name_url.replace(name_url.split("-",-1)[-1],"")[:-1]
            sku_url = name_url.replace("__340.jpg","")
            sku_url = sku_url.replace("__340.png","")
            sku = sku_url.replace(name+"-","")
            item = TupianItem()
            item['sku'] = sku
            item['name'] = name
            item['images'] = sku+"_1.jpg"
            item['weight'] = '0.1'
            item['type'] = 'downloadable'
            item['qty'] = 999
            item['tax_class_id'] = '0'
            item['category_ids'] = ''
            item['attribute_set'] = 'Default'
            item['price'] = ''
            item['image_url'] = url
            item['links'] = 'file:0.png,sort_order:,title:'+name+',sample:,is_shareable:config,number_of_downloads:0'
            items.append(item)
        return items



