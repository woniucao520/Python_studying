# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Spider, Request
from zhihu.items import ZhihuItem


class ZhihutestSpider(scrapy.Spider):
    name = "zhihutest"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['http://www.zhihu.com/']
    user_url = 'https://www.zhihu.com/api/v4/members/{user_name}?include={include}'  #单个用户的url构造
    start_user = 'excited-vczh' #这里以 超级大V轮子哥为例
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
    # 用户关注列表的follower_url的链接构造
    follower_url = 'https://www.zhihu.com/api/v4/members/{follower_name}/followees?include={include}&offset={offset}&limit={limit}'
    follower_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):  # 拼接单个用户的url，关注页的url
        yield Request(self.follower_url.format(follower_name=self.start_user,include =self.follower_query,offset =0,limit =20),callback=self.follower_parse) #关注列表页的url
        yield Request(self.user_url.format(user_name=self.start_user,include =self.user_query),callback=self.user_parse) #单个用户的url

    def follower_parse(self,response):
        results = json.loads(response.text)
        if 'data' in results.keys(): # 关注列表，获取url_token
            for result in results['data']:
                url_token = result['url_token']
                yield Request(self.user_url.format(user_name=url_token, include=self.user_query), callback=self.user_parse)
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False: # 判断下一页
            next_page = results.get('paging').get('next')  # 获取下一页
            yield Request(next_page, callback=self.follower_parse)

    def user_parse(self, response):  # 获取单个页面的详细信息
        results = json.loads(response.text)
        item = ZhihuItem()

        for field in item.fields:
            if field in results.keys():
                item[field] = results.get(field)
                user_token = results.get('url_token')
        yield item
        yield Request(self.follower_url.format(follower_name=user_token, include=self.follower_query,offset =0,limit =20), callback=self.follower_parse)

