# -*- coding: utf-8 -*-
import requests
import re
import time
from bs4 import BeautifulSoup
import json
import csv
import MySQLdb
import os



class TaoProduct(object):
    def __init__(self):
        self.kword = '蛋糕'
        self.headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        self.postURL = 'https://s.taobao.com/search?q='+self.kword
        urlist = []
        for i in range(2):
            self.url = self.postURL + '&s=' + str(44*i)
            urlist.append(self.url)
        print urlist
        self.get_product(urlist)
        self.save_images(urlist)


    def get_product(self,urlist):
        news_content = []
        for url in urlist:
            try:
                response = requests.get(url,headers =self.headers)
            except Exception as e:
                print '抓取网页出现错误,错误为:%s' % e
                return None
            if response.status_code ==200:
                response = requests.get(url)
                # soup = BeautifulSoup(response.text,'lxml')
                news_pattern = re.compile(r'{"pageName":"mainsrp",.*?false}}', re.S|re.M|re.I)
                web_content = re.search(news_pattern, response.text)
                result = web_content.group()  # 获得json格式
                pagejson = json.loads(result) # 将str转换成dic
                for news in pagejson['mods']['itemlist']['data']['auctions']: # 包含的信息在auctions内
                    view_price = news['view_price']  # 价格
                    view_sales = news['view_sales'] # 销量
                    item_loc = news['item_loc']  #
                    raw_title = news['raw_title']

                    web_news = [view_price,view_sales,item_loc,raw_title]
                    news_content.append(web_news)
                    # print news_content
            #         self.save_mysql(news_content) # 存入mysql数据库
            # self.save_to_csv(news_content)  #存入cav


    def save_to_csv(self,news_content):
        filename = "result.csv"
        with open(filename, "wb") as f:
            csvWriter = csv.writer(f)
            for data in news_content:
                csvWriter.writerow(data)
            f.close

    def save_images(self,urlist):  # 图片的下载
        for url in urlist:
            response = requests.get(url,headers =self.headers)
            news_pattern = re.compile(r'{"pageName":"mainsrp",.*?false}}', re.S|re.M|re.I)
            web_content = re.search(news_pattern, response.text)
            result = web_content.group()  # 获得json格式
            pagejson = json.loads(result) # 将str转换成dic
            for price in pagejson['mods']['itemlist']['data']['auctions']:
                pic_url = price['pic_url']
                imageurl = 'http:'+ str(pic_url)
                user_id = price['user_id']
                if not os.path.exists("images"):
                    os.mkdir("images")
                r2 = requests.get(imageurl)
                with open("images/" + user_id + '.jpg', "wb") as f:
                    f.write(r2.content)

    def save_mysql(self,news_content):
        # 先连接数据库
        conn =MySQLdb.connect(host = '127.0.0.1',user = 'root',passwd = '123456',charset = 'utf8',port = 3306)
        cur = conn.cursor() # 数据库都是游标来操作的
        sql = 'create database if not exists taobao_database default charset utf8'
        cur.execute(sql) #创建数据库，注意编码格式为utf8

        conn.select_db('taobao_database') # 创建表 taobao_database

        sql = 'create table if not exists product'+"(id int auto_increment, price varchar(255), sales varchar(255), \
        item_loc varchar(255),title varchar(255), primary key(ID))"

        cur.execute(sql) # 创建表结构 这部分代码以后直接在mysql里创建就可以了

        for elem in news_content:
            sql = 'insert into product(price,sales,item_loc,title) values(\'%s\',\'%s\',\'%s\',\'%s\')'\
             % tuple(elem)  #detail_news是一个二重数组list，我们需要将其转换成元组格式，插入到数据库中

        cur.execute(sql)
        print 'insert success!!!'   # 这里给个提示，每条数据是否插入成功

        conn.commit()  #一定要有commit提交，不然数据库里没有数据
        cur.close()
        conn.close()

if __name__ == '__main__':
    object = TaoProduct()

