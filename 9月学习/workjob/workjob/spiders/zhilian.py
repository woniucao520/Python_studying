# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from workjob.items import WorkjobItem
from scrapy.selector import Selector
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['jobs.zhaopin.com']
    start_urls = []
    keyword = 'java'
    place = '北京'
    page = 5

    def start_requests(self):
        for i in range(1, self.page+1):
            url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl={}&kw={}&sm=0&p={}'.format(self.place, self.keyword, str(i))
            yield Request(url, self.parse)

    def parse(self, response):
        # print response.body
        selector = Selector(response)
        web_content = selector.xpath('//div[@class="newlist_list_content"]/table')
        for news in web_content:  # 由于web_content有n个list，导致里面的url会循环n遍
            url = news.xpath('//td[@class="zwmc"]/div/a[1]/@href').extract()
        for new_url in url:
            new_url = new_url + 'l'
            # print new_url
            yield Request(new_url, self.get_web_content)

    def get_web_content(self, response):
        items = []
        selector = Selector(response)
        web_content = selector.xpath('//ul[@class="terminal-ul clearfix"]')
        print web_content
        for news in web_content:
            item = WorkjobItem()
            item['title'] = selector.xpath('//div[@class="fixed-inner-box"]/div/h1/text()')[0].extract()  # 职位名称

            item['company'] = selector.xpath('//div[@class="fixed-inner-box"]/div/h2/a/text()')[0].extract()

            item['zwyx'] = news.xpath('li[1]/strong/text()')[0].extract()

            # zwyx =zwyx.replace(u'元/月','')  # 职位月薪

            item['gzdd'] = news.xpath('li[2]/strong/a/text()')[0].extract() # 工作地点

            item['fbtime'] = news.xpath('li[3]/strong/span/text()')[0].extract()  # 发布时间

            item['experence'] = news.xpath('li[5]/strong/text()')[0].extract() # 工作经验

            item['totalnum'] = news.xpath('li[7]/strong/text()')[0].extract().replace('人', '')  # 招聘人数

            print (item['title'],item['company'],item['zwyx'],item['gzdd'],item['fbtime'],item['experence'],item['totalnum'])

            items.append(item)

        return items


