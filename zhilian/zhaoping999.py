# -*- coding: utf-8 -*-
import MySQLdb
import time
from lxml import etree
from bs4 import BeautifulSoup
from numpy import hstack
import requests
import xlwt
import csv
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


class ZhPinSpider(object):
    def __init__(self):
        self.place = '北京'
        self.kword = 'java'
        # urlist = []  # 如果在循环体的外面，那么self，在for里面的话，数据就逐条加入，
        # self在for循环体外面的话，就获取到最后一条结果集的记录，通过遍历，也能得到每条数据
        urlist = []
        for i in range(1,3):
            # 如果 []在循环体里面，self.get也在循环体里，一个一个的获取url，不会重复


            self.postUrl = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl={}&kw={}&sm=0&p={}'.format(self.place,self.kword,str(i) ) #构造 搜索的 url链接以及分页
            urlist.append(self.postUrl)
            self.headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}#postUrl是需要登陆后的网址，这里添加代理，不然返回502
            # print urlist  # 获取到的是每条每条的数据
        self.get_nexturlist(urlist)  # 添加到get_nexturlist,不然get_nexturlist获取不到数值
        # print urlist

    
    def get_nexturlist(self,urlist): # 获取“所有链接”
        detail_url = [ ]  # 如果detail_url 在for循环体的里面，那么每次只能获取60条数据
        for url in urlist:
            try:
                response = requests.get(url ,headers =self.headers)  # 添加header,get()后面的参数也可以直接写成url

            except Exception as e:
                print '抓取网页出现错误,错误为:%s' % e
                return None
            if response.status_code == 200:
                response = requests.get(url,headers =self.headers)
                selector = etree.HTML(response.text)
                web_content =selector.xpath('//div[@class="newlist_list_content"]/table')


                for news in web_content:  # 由于web_content有n个list，导致里面的url会循环n遍

                    url =news.xpath('//td[@class="zwmc"]/div/a[1]/@href') # 得到url一部分的列表，http://jobs.zhaopin.com/197197314250211.html

                for new_url in url:
                    new_url = new_url + 'l'
                    detail_url.append(new_url)  # 如果append在循环体的外面，那只会获取得到一条数据
                    # detail如果在循环体内 将获取得到所有数据new_url
                # print detail_url # 在循环体外，获取所有数据的最后一条（这条数据，要包含原来获取的数据）
                self.get_web_content(detail_url)

            else:
                time.sleep(5)


    def get_web_content(self,detail_url): # 单个招聘信息的详情
        detail_news = []
        for url in detail_url:
            print url
            try:
                response = requests.get(url ,headers =self.headers)  # 添加header,get()后面的参数也可以直接写成url
            except Exception as e:
                print '抓取网页出现错误,错误为:%s' % e
                return None
            if response.status_code == 200:

                response = requests.get(url,headers =self.headers,)
                selector = etree.HTML(response.text)

                web_content =selector.xpath('//ul[@class="terminal-ul clearfix"]')


                for news in web_content:
                    detail ={}
                    detail['title'] = selector.xpath('//div[@class="fixed-inner-box"]/div/h1/text()')[0] #职位名称

                    detail['company'] =selector.xpath('//div[@class="fixed-inner-box"]/div/h2/a/text()')[0]

                    detail['zwyx'] = news.xpath('li[1]/strong/text()')[0]

                    # zwyx =zwyx.replace(u'元/月','')  # 职位月薪

                    detail['gzdd'] = news.xpath('li[2]/strong/a/text()')[0] # 工作地点


                    detail['fbtime'] = news.xpath('li[3]/strong/span/text()')[0]  # 发布时间

                    detail['experence'] = news.xpath('li[5]/strong/text()')[0]  # 工作经验


                    detail['totalnum'] =  news.xpath('li[7]/strong/text()')[0].replace('人','') # 招聘人数
                    # print totalnum
                    # totalnum =totalnum.replace(u'人','')
                    print detail



                # print detail
                detail_news.append(detail)
                print detail_news
                self.save_csv(detail_news)
                self.save_mysql(detail_news)

    # self.save_mysql(detail_news) # 存入数据库




    def save_csv(self,detail_news):
        with open ('myjobt.csv','wb') as f:
            writer = csv.writer(f)
            fieldnames =detail_news[0].keys()  #将key作为表头标题填入
            writer.writerow(fieldnames)
            for row in detail_news:
                writer.writerow(row.values())  #将value作为内容，依次进行填充
        # def save_csv(self,detail_news):
    #     with open ('myjobt.csv','wb') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(['title','company','zwyx','gzdd','fbtime','experence','totalnum'])
    #         for row in detail_news:
    #             writer.writerow(row)


# todo如何将嵌入到列标里的字典，写入excel

    def save_mysql(self,detail):
        # 先连接数据库
        conn =MySQLdb.connect(host = '127.0.0.1',user = 'root',passwd = '',charset = 'utf8',port = 3306)
        cur = conn.cursor()
        # cur.execute("drop database if exists new_database") # 如果new_database数据库存在则删除
        # cur.execute("create database new_database") #新创建一个数据库
        sql = 'create database if not exists new_database default charset utf8'
        cur.execute(sql)

        conn.select_db('new_database')

        sql = 'create table if not exists myresult'+"(id int auto_increment, title varchar(255), company varchar(255), \
        zwyz varchar(255),gzdd varchar(255), fbtime varchar(255), experence varchar(255), totalnum varchar(255), primary key(ID))"

        cur.execute(sql)

        sql = 'insert into myresult(title,company,zwyz,gzdd,fbtime,experence,totalnum) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
         % (detail[0][0],detail[0][1],detail[0][2],detail[0][3],detail[0][4],detail[0][5],detail[0][6])

        print (sql)
        cur.execute(sql)
        print 'insert success!!!'
        conn.commit()
        cur.close()
        conn.close()

if __name__ == '__main__':
    object = ZhPinSpider()


