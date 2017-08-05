# -*- coding: utf-8 -*-
import re
import os
import requests
from bs4 import BeautifulSoup
import json
import csv
import time
from requests.exceptions import ConnectionError
from lxml import etree
import sys
# http://www.kaola.com/product/1449381.html

reload(sys)
sys.setdefaultencoding("utf-8")

class KaolaSpider(object):
    def __init__(self):
        self.rootURL = \
    ['http://www.kaola.com/search.html?key=%25E8%25BF%2590%25E5%258A%25A8%25E6%2589%258B%25E7%258E%25AF&isSelfProduct=true&pageNo={}'.format(str(i)) for i in range(1, 2)]


    def get_list_url(self):
        for url in self.rootURL:
            try:
                response = requests.get(url)
                selector = etree.HTML(response.text)
                content = selector.xpath('//p[@class ="goodsinfo clearfix"]/a/@href')
                news_url = ['http://www.kaola.com/'+ url for url in content]
                self.get_detail_news(news_url)
                self.get_save_images(news_url)
            except ConnectionError:
                print('Error occurred')
                return None

    def get_detail_news(self, news_url):
        for url in news_url:
            try:
                response = requests.get(url)
            except Exception as e:
                print '抓取网页出现错误，错误为：%s' % e
                return None
            if response.status_code == 200:
                response = requests.get(url)
                news_pattern = re.compile(r'{"actualCurrentPrice".*?}, //', re.S|re.M|re.I)
                result = re.search(news_pattern, response.text)
                a = result.group()
                b = a.replace(', //', '')

                pageJson = json.loads(b)  # 将str解析成dic，解析json格式,解出来是一个字典
                '''
                解析json里面的数据
                第一部分：简单的基本商品信息
                '''
                skuList = pageJson['skuList']
                for skuData in skuList:  # 基本商品信息的提取
                    data = pageJson['warehouseNameAlias']  # 自营国内仓
                    goodsId = pageJson['skuList'][0]['goodsId']   # goodsid
                    propertyValues1 = pageJson['goodsPropertyList'][0]['propertyValues'][0]['propertyValueId']
                    title = pageJson['title']
                    brandName = pageJson['brandName']
                    originCountryName = pageJson['originCountryName']
                    warehouseCityShow = pageJson['warehouseCityShow']
                    marketPrice = skuData['marketPrice']
                    actualCurrentPrice = skuData['actualCurrentPrice']
                    store = skuData['store']
                    # print marketPrice, actualCurrentPrice, store
                '''
                第二部分：多属性商品信息的提取
                '''
        else:
            time.sleep(10)
            return None

    def get_save_images(self,news_url):
        '''
        第一部分：获取产品大图
        第二部分：获取信息描述图
        '''
        for url in news_url:
            try:
                response = requests.get(url)
            except Exception as e:
                print '抓取网页出现错误，错误为：%s' % e
                return None
            if response.status_code == 200:
                response = requests.get(url)
                news_pattern = re.compile(r'{"actualCurrentPrice".*?}, //', re.S|re.M|re.I)
                result = re.search(news_pattern, response.text)
                a = result.group()
                b = a.replace(', //', '')
                pageJson = json.loads(b)  # 将str解析成dic，解析json格式,解出来是一个字典
                img_all = pageJson['goodsImageList']
                product_pic = []
                for product_img in img_all:
                    need_img = product_img['imageUrl']
                    product_pic.append(need_img)




    def save_news_csv(self):
        pass

if __name__ == '__main__':
    object = KaolaSpider()
    object.get_list_url()




