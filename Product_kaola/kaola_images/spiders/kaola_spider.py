# -*- coding: UTF-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from kaola.items import KaolaItem
from scrapy.http import Request
import json


class KaolaSpider(BaseSpider):

    name = "kaola"
    allowed_domains = ["kaola.com"]
    start_urls = ['http://www.kaola.com/category/2620/2622.html'] #demo url 不应定好使

    base_url = ''
    page_size = 1

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.xpath('//*[@class="titlewrap"]/a[1]/@href').extract()
        # product page
        for url in urls:
            full_url = 'http://www.kaola.com/recentlyViewAjax.html?id=' + url
            yield Request(full_url, callback=self.item_parse)

    def parse(self, response):
        productData = self.getProductData(response)
        items = []
        for data in productData:
            item = KaolaItem()
            item['id'] = data['id']
            item['sku'] = data['sku']
            item['name'] = data['name']
            item['country'] = data['country']
            item['brand'] = data['brand']
            item['price'] = data['price']
            item['special_price'] = data['special_price']
            item['qty'] = data['qty']
            item['tax_class_id'] = data['taxRate']
            item['short_description'] =data['short_description']
            item['description'] = data['description']
            item['image'] = data['image']
            item['gallery'] = data['gallery']
            item['type_id'] = 'simple'
            item['weight']  = '1'
            item['product_sync_type'] = '售卖且不需要同步'
            item['warehouse'] = '青岛1号仓'
            item['vendor_code'] = '4000'
            items.append(item)
        return items

    def getProductData(self,response):
        pageJson = json.loads(response.body)
        alldata_item = []
        pageData = pageJson['list'][0]
        skuList = pageData['skuList'][0]
        id = skuList['goodsId']
        name = pageData['title']
        sku = 'whg'+str(id)
        country = pageData['originCountryName']
        brand = pageData['brandName']
        price = skuList['marketPrice']*1.2
        special_price = skuList['actualCurrentPrice']*1.2
        qty = skuList['store']
        tax_class_id = skuList['taxRate']
        short_description = pageData['shortTitle']
        description = pageData['detail']
        image = pageData['imageUrl']
        gallery = pageData['imageUrlList']

        if (tax_class_id == "0.1"):
            tax = "2"
        elif (tax_class_id == "0.2"):
            tax = "4"
        elif (tax_class_id == "0.5"):
            tax = "5"
        elif (tax_class_id == "0.119"):
            tax = "6"
        elif (tax_class_id == "0.091"):
            tax = "7"
        elif (tax_class_id == "0.47"):
            tax = "8"
        elif (tax_class_id == "0.32375"):
            tax = "9"
        else:
            tax = "0"
        description = description.replace("\r\n","")
        description = description.replace("\n","")
        alldata_item.append(
            {"id": id, "name":name,"sku":sku,"country":country,"qty": qty, "price": str(price), "special_price": str(special_price),"brand":brand,
             "taxRate": tax,"short_description":short_description,"description":description,"image":image,"gallery":gallery})
        return alldata_item