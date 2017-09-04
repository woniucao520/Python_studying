# encoding:utf-8
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from KLcao.items import KlcaoItem
import json ,re


class KaolaSpider(BaseSpider):
    name = "kaola"
    allowed_domains= ["www.kaola.com"]
    start_urls = ["https://www.kaola.com/search.html?zn=top&key=%25E6%2589%258B%25E7%258E%25AF&searchRefer=searchbutton&timestamp=1504444431838"]

    def parse(self, response):
        web_content = HtmlXPathSelector(response)
        href = web_content.xpath('//p[@class="goodsinfo clearfix"]/a/@href').extract()
        for href in href:
            urls = 'http://www.kaola.com'+ href

            yield Request(urls, callback=self.getProductData)

    def getProductData(self, response):
        alldata_item = []
        pattern = re.compile(' {"actualCurrentPrice":(.*?)"}, //',re.S)
        items = re.search(pattern,response.body)
        result = items.group().replace(', //','')
        pageJson = json.loads(result)#将str解析成dic，解析json格式,解出来是一个字典
        id = pageJson['goodsId']
        sku = 'whg' + str(id)
        name = pageJson['title']
        country = pageJson['originCountryName']
        warehouseNameAlias = pageJson['warehouseNameAlias']  # 国内自营仓
        price = pageJson['actualCurrentPrice']
        img_description = pageJson['detail'] # 产品详细图
        # 解析多属性
        # product_attributes = {}
        # if 'skuGoodsPropertyList' in pageJson:
        #     for attr in pageJson['skuGoodsPropertyList']:
        #         attr_name = attr['propertyNameCn']
        #         options = attr['propertyValues']
        #         for option in options:
        #             tmp_option = {}
        #             option_id = option['propertyValueId']
        #             option_value = option['propertyValue']
        #             color_image = option['imageUrl']
        #             tmp_option['option_attr'] = attr_name
        #             tmp_option['option_value'] = option_value
        #             tmp_option['option_image'] = color_image
        #             product_attributes[option_id] = tmp_option
        # print product_attributes
        # 主图图片的下载
        gallery_all = pageJson['goodsImageList']
        gallery = []
        for img in gallery_all:
            gallery.append(img['imageUrl'])
        alldata_item.append({"sku":sku,"name":name,"country":country,"warehouseNameAlias":warehouseNameAlias,"price":price,"img_description":img_description,"gallery":gallery})
        return  alldata_item

    def my_items(self,response):
        productData = self.getProductData(response)
        items = []
        for data in productData:
            item=KlcaoItem()
            item['sku']=data['sku']
            item['name'] = data['name']
            item['country'] = data['country']
            item['warehouseNameAlias'] = data['warehouseNameAlias']
            item['img_description'] = data['img_description']
            item['price'] = data['price']
            item['gallery'] = data['gallery']

        return  items










