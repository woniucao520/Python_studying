# -*- coding: UTF-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from kaola.items import KaolaItem
from scrapy.http import Request
import json ,re


class KaolaSpider(BaseSpider):

    name = "kaola" # spider name
    allowed_domains = ["kaola.com"] # domain
    start_urls = ["http://www.kaola.com/product/1501901.html"] # start url 要采集的网页地址

    # base_url = 'http://www.kaola.com/search.html?key=%25E8%25BF%2590%25E5%258A%25A8%25E6%2589%258B%25E7%258E%25AF&isSelfProduct=true&pageNo='
    # page_size = 2

    def __init__(self):
        # for page in range(1,self.page_size+1):
        #     self.start_urls.append(self.base_url+str(page)) # 把所有的目录页面写入的 start_urls
        pass

    ''' 解析目录页面数据 '''
    def myparse(self, response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.xpath('//*[@class="titlewrap"]/a[1]/@href').extract() # 解析目录页面单个商品的url

        # product page
        for url in urls:
            full_url = 'http://www.kaola.com/' + url
            yield Request(full_url, callback=self.item_parse) # 爬取商品页面 回调到 item_parse

    ''' 写入ITEM  '''
    def parse(self, response):
        productData = self.getProductData(response) # 获取单个商品页面的信息
        items = []
        for data in productData:
            if data['country'] == u'中国':
                continue
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
            item['short_description'] =data['name']
            item['description'] = data['description']
            item['image'] = data['image']
            item['gallery'] = data['gallery']
            item['type_id'] = 'simple'
            item['weight'] = '1'
            item['product_sync_type'] = '售卖且不需要同步'
            item['warehouse'] = '青岛1号仓'
            item['vendor_code'] = '4000'
            item['warehouse_city'] = data['warehouse_city']
            item['warehouse_alias'] = data['warehouse_alias']
            if data['custom_arr']:
                for key in data['custom_arr']:
                    item[key] = data['custom_arr'][key]
            items.append(item)
        return items

    ''' 解析单个商品的页面数据 '''
    def getProductData(self,response):
        bodyHtml = response.body
        jsonData = self.getBetweenContent(bodyHtml,'goods: ',', \/\/商品信息') # 通过页面中的json 获取商品数据
        pageJson = json.loads(''.join(jsonData))
        skuList = pageJson['skuList']

        ''' 产品属性信息  '''
        product_attributes = {}
        if pageJson.has_key('skuGoodsPropertyList'):
            for attr in pageJson['skuGoodsPropertyList']:
                attr_name = attr['propertyNameCn']
                options = attr['propertyValues']
                for option in options:
                    tmp_option = {}
                    option_id = option['propertyValueId']
                    option_value = option['propertyValue']
                    color_image = option['imageUrl']
                    tmp_option['option_attr'] = attr_name
                    tmp_option['option_value'] = option_value
                    tmp_option['option_image'] = color_image
                    product_attributes[option_id] = tmp_option

        ''' sku信息  '''
        alldata_item = []
        for skuData in skuList:
            custom_arr = {}
            id = pageJson['goodsId']
            name = pageJson['title']
            country = pageJson['originCountryName']
            brand = pageJson['brandName']
            warehouse_city = pageJson['warehouseCityShow']
            warehouse_alias = pageJson['warehouseNameAlias']
            description = pageJson['detail']
            price = skuData['marketPrice']
            special_price = skuData['actualCurrentPrice']
            tax_class_id = skuData['taxRate']
            qty = skuData['store']
            image = pageJson['imageUrl']

            gallery_all = pageJson['goodsImageList']
            gallery = []
            for img in gallery_all:
                gallery.append(img['imageUrl'])

            sku = 'whg'+str(id)
            if skuData.has_key('skuPropertyValueId4View'):
                sku = sku+str(skuData['skuPropertyValueId4View'])
                options = skuData['skuPropertyValueIdList']
                i = 1
                for option in options:
                    custom_arr["custom"+str(i)] = product_attributes[option]['option_value']
                    if product_attributes[option]['option_image']:
                        image = product_attributes[option]['option_image']
                    i = i+1
            pass

            ''' 24th tax '''
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
            alldata_item.append(
                {"id": id, "name":name,"sku":sku,"country":country,"qty": qty, "price": str(price), "special_price": str(special_price),"brand":brand,
                 "taxRate": tax,"short_description":'',"description":description,"image":image,"gallery":gallery,"warehouse_city":warehouse_city,"warehouse_alias":warehouse_alias,'custom_arr':custom_arr})
        return alldata_item

    ''' 截取字符串部分数据 '''
    def getBetweenContent(self, pagehtml, start, end):
        pat = re.compile(start + '(.*?)' + end, re.S)
        content = pat.findall(pagehtml)
        return content