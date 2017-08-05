# -*- coding: UTF-8 -*-

import scrapy
from scrapy.selector import HtmlXPathSelector
from coach.items import CoachItem
from scrapy.http import Request
import re,json,urllib2,cookielib
from lxml import etree
import sys

class CoachSpider(scrapy.Spider):

    name = "coach"
    allowed_domains = ["coachaustralia.com"]
    start_urls = ["https://coachaustralia.com/product/flag-backpack-in-pebble-leather#C/57408LVX","https://coachaustralia.com/product/flag-backpack-in-pebble-leather#C/57408LWO"]
    domain_url = 'https://coachaustralia.com'
    def item_parse(self, response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.select('//*[@class="product-item"]//div[@class="picture"]//a//@href').extract()
        items = []
        for url in urls:
            full_url = self.domain_url+url
            item = CoachItem()
            item['sku'] = '1111'
            item['name'] = full_url
            items.append(item)
        return items

    # get product data
    def parse(self, response):
        items = []
        selector = etree.HTML(response.body)
        datahtml = selector.xpath("//*[@type='application/ld+json']//text()")[0]
        datahtml = datahtml.replace("\r\n","")
        datahtml = eval(datahtml)
        name = datahtml['name']
        description = datahtml['description']
        attributes = datahtml['offers']['offers']

        #sku  id
        skus = selector.xpath('//*[@class="article-code"]/div[@class="sku"]/span/text()')
        ids = selector.xpath('//*[@class="article-code"]/div[@class="sku"]/span/@id')
        multi = {}
        for index,item_sku in enumerate(skus):
            item_sku = (item_sku).replace(' style no. ','')
            id = (ids[index]).replace('sku-','')
            multi[item_sku] = id

        for item in attributes:
            sku = item['itemOffered']['sku']
            price = item['price']
            id = multi[sku]
            images = selector.xpath('//*[@class="picture-thumbs" and @data-productid="'+id+'"]/ul/li/a/@data-image')
            item = CoachItem()
            item['sku'] = str(sku).replace('/','_')
            item['name'] = name
            item['brand'] = 'Coach'
            item['price'] = price
            item['images'] = images
            item['description'] = description
            item['qty'] = 10
            item['short_description'] = name
            item['category_ids'] = 3
            item['weight'] = 1
            item['attribute_set'] = 'Default'
            item['type_id'] = 'simple'
            items.append(item)
        return items


    # get between str
    def GetMiddleStr(self,content,startStr,endStr):
        startIndex = content.index(startStr)
        if startIndex>=0:
            startIndex += len(startStr)
        endIndex = content.index(endStr)
        return content[startIndex:endIndex]
