# -*- coding: UTF-8 -*-
import scrapy
from Pixabay.items import PixabayItem
from scrapy.http import Request
from scrapy.selector import Selector

class MyImages(scrapy.Spider):
    name = "downimages"
    allowed_domains = ["pixabay.com"]
    start_urls = []


    def start_requests(self):  # 这里重写了start_urls的方法
        for i in range(1,3):
            url = 'https://pixabay.com/zh/editors_choice/?media_type=photo&pagi=' + str(i)
            yield Request(url, self.parse)

    def parse(self, response):
        selector = Selector(response)
        web_content = selector.xpath('//*[@id="content"]/div/div/div/div/a/img/@data-lazy').extract()

        items = []
        for news in web_content:
            name_url = news.split('/', -1)[-1]
            name = name_url.replace(name_url.split("-", -1)[-1], "")[:-1]
            sku_url = name_url.replace("__340.jpg", "")
            sku_url = sku_url.replace("__340.png", "")
            sku = sku_url.replace(name+"-", "")

            item = PixabayItem()
            item['sku'] = sku
            item['name'] = name
            item['image'] = sku+"_1.jpg"
            item['gallery'] = sku+"_1.jpg"
            item['image_url'] = news
            item['qty'] = 999
            item['links'] = 'file:0.png,sort_order:,title:'+name+',sample:,is_shareable:config,number_of_downloads:0'
            item['description'] = '<p><img src="{{media url="wysiwyg/material/'+sku[0]+'/'+sku[1]+'/'+sku+'/' + sku+"_1.jpg" +'"}}" alt="" /></p>'

            items.append(item)
        return items

