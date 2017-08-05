# -*- coding: UTF-8 -*-

import scrapy
from scrapy.selector import HtmlXPathSelector
from jd.items import JdItem
from scrapy.http import Request
import re,json,urllib2,cookielib
from lxml import etree
import sys,MySQLdb


class JdSpider(scrapy.Spider):

    name = "jd"
    allowed_domains = ["list.jd.com","item.jd.com","p.3.cn","jd.com"]
    start_urls = []
    base_url = ''
    url_id = ''

    # Mysql database
    MYSQL_HOST = '127.0.0.1'
    MYSQL_DBNAME = 'magento_db'
    MYSQL_USER = 'root'
    MYSQL_PASSWD = ''
    MYSQL_PORT = 3306

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
        conn = self.getDB()
        cur = conn.cursor()
        cur.execute("SELECT * FROM scrapy_record WHERE status = 'pending' LIMIT 1")
        row = cur.fetchone()
        if row != None:
            self.base_url = row[1]
            self.url_id = row[0]
        self.closeDB(conn)
        print()
        # set cookie
        # filename = 'cookie.txt'
        # cj = cookielib.MozillaCookieJar(filename)
        # cookie_support = urllib2.HTTPCookieProcessor(cj)
        # opener = urllib2.build_opener(cookie_support)
        # urllib2.install_opener(opener)
        mainPage = urllib2.urlopen(self.base_url)
        # cj.save()

        selector = etree.HTML(mainPage.read())
        page_size = int(selector.xpath('//*[@class="p-skip"]/em/b/text()')[0])
        page = 1
        page_size = 1
        while (page <= page_size):
            self.start_urls.append(self.base_url+'&page='+str(page))
            page = page+1
        pass

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.select('//*[@id="plist"]//li//div[@class="p-img"]//a//@href').extract()
        # product page
        for url in urls:
            full_url = 'http:'+url
            yield Request(full_url, callback=self.checkChild)
            break
        pass

    #check child
    def checkChild(self,response):
        children = ''
        attribute_list = eval(self.getBetweenContent(response.body,' colorSize: ',']')[0]+']')
        for attribute in attribute_list:
            children = 1
            child_sku = attribute['skuId']
            child_url = "http://item.jd.com/"+str(child_sku)+".html"
            yield Request(child_url, callback=self.item_parse)
        if children == '':
            self.item_parse(response)
        pass

    # format product data
    def item_parse(self, response):
        productData = self.getProductData(response)
        items = []
        for data in productData:
            item = JdItem()
            item['sku'] = data['sku']
            item['name'] = data['name']
            item['brand'] = data['brand']
            item['price'] = data['price']
            item['images'] = data['images']
            item['description'] = data['description']
            item['qty'] = data['qty']
            item['color'] = data['color']
            item['size'] = data['size']
            item['short_description'] = data['name']
            item['category_ids'] = 10
            item['weight'] = 1
            item['tax_class_id'] = 0
            item['attribute_set'] = 'Default'
            item['type_id'] = 'simple'
            items.append(item)
        return items

    # get product data
    def getProductData(self, response):
        ProductInfo = []
        selector = etree.HTML(response.body)
        url = response.url
        sku = self.getBetweenContent(url,'http://item.jd.com/','.html')

        sku = sku[0]
        name = str(selector.xpath('//*[@class="sku-name"]/text()'))
        brand = str(selector.xpath('//*[@id="parameter-brand"]/li/@title'))
        priceData = eval(urllib2.urlopen('http://p.3.cn/prices/mgets?pduid=14878171290871999775066&skuIds=J_'+sku).read())
        price = priceData[0]['p']
        imgData = urllib2.urlopen('http://item.jd.com/bigimage.aspx?id='+sku).read()
        images = self.getBetweenContent(imgData,'newOutputAllImages.data=',';')
        description_url = str('http:'+self.getBetweenContent(response.body,"desc: '","',")[0])
        description = urllib2.urlopen(description_url).read()
        qty_url = 'http://c0.3.cn/stock?skuId='+sku+'&area=1_72_4137_0&venderId=619902&cat=11729,11730,6908&buyNum=1&choseSuitSkuIds=&extraParam={%22originid%22:%221%22}'
        qty = int(self.getBetweenContent(urllib2.urlopen(qty_url).read(),'"StockState":',',')[0])
        if qty == 33:
            qty = 10
        else:
            qty = 0

        color_key = '颜色'.decode('utf-8').encode('gbk')
        size_key = '尺码'.decode('utf-8').encode('gbk')
        color = ''
        size = ''
        attribute_list = eval(self.getBetweenContent(response.body,' colorSize: ',']')[0]+']')
        for attribute in attribute_list:
            if sku == str(attribute['skuId']):
                for key in attribute.keys():
                    if key == color_key:
                        color = attribute[key].decode('gbk').encode('utf-8')
                    elif key == size_key:
                        size = str(attribute[key])
                    pass

        ProductInfo.append({"sku": sku,'name':name,'brand':brand,'price':price,'images':images,'description':description,'qty':qty,'size':size,'color':color})
        return ProductInfo

    # get between str
    def getBetweenContent(self, pagehtml, start, end):
        pat = re.compile(start + '(.*?)' + end, re.S)
        content = pat.findall(pagehtml)
        return content

    # link mysql
    def getDB(self):
        host = self.MYSQL_HOST
        user = self.MYSQL_USER
        password = self.MYSQL_PASSWD
        dbname = self.MYSQL_DBNAME
        db = MySQLdb.connect(host,user,password,dbname)
        return db

    #close datase
    def closeDB(self,db):
        db.close()
        pass

