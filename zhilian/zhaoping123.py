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
sys.setdefaultencoding("utf-8")

class ZhPinSpider(object):
    def __init__(self):
        self.place = '北京'
        self.kword = 'java'
        urlist = []
        for i in range(1,3):

            self.postUrl = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl={}&kw={}&sm=0&p={}'.format(self.place,self.kword,str(i) ) #构造 搜索的 url链接以及分页
            urlist.append(self.postUrl)
            self.headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}#postUrl是需要登陆后的网址，这里添加代理，不然返回502
        self.get_nexturlist(urlist)  # 添加到get_nexturlist,不然get_nexturlist获取不到数值
        # print urlist

    
    def get_nexturlist(self,urlist): # 获取“所有链接”
        detail_url = []
        for url in urlist:
            try:
                response = requests.get(url, headers =self.headers)  # 添加header,get()后面的参数也可以直接写成url
                print response
            except Exception as e:
                print '抓取网页出现错误,错误为:%s' % e
                return None
            if response.status_code == 200:
                response = requests.get(url,headers =self.headers)
                selector = etree.HTML(response.text)
                web_content =selector.xpath('//div[@class="newlist_list_content"]/table')

                for news in web_content:
                    url =news.xpath('//td[@class="zwmc"]/div/a[1]/@href')  # 得到url一部分的列表，http://jobs.zhaopin.com/197197314250211.html
                    par = news.xpath('//td[@class="zwmc"]/div/a[1]/@par') # 得到url的另一部分，ssidkey=y&ss=201&ff=03&sg=df302cd0ecfe420b89d61e98e6529b1c&so=1
                  #todu 如何将两个不同数组里的元素，拼接起来
                    # last_url =hstack((url,par))
                    # print last_url
                for url in url :
                    url = url + 'l'  # 得到 ：http://jobs.zhaopin.com/197197314250211.html，字符串的构造
                    detail_url.append(url)
                # print detail_url
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
                title = selector.xpath('//div[@class="fixed-inner-box"]/div/h1/text()')[0] #职位名称
                if len(selector.xpath('//div[@class="fixed-inner-box"]/div/h2/a/text()'))>0:  # 出现没有公司名的页面:需要盘大unyixia
                    company =selector.xpath('//div[@class="fixed-inner-box"]/div/h2/a/text()')[0]
                # print company

                for news in web_content:
                    zwyx = news.xpath('li[1]/strong/text()')[0]
                    zwyx =zwyx.replace(u'元/月','')  # 职位月薪
                    # print zwyx.encode('utf-8')
                    gzdd = news.xpath('li[2]/strong/a/text()')[0] # 工作地点
                    fbtime = news.xpath('li[3]/strong/span/text()')[0]  # 发布时间
                    experence = news.xpath('li[5]/strong/text()')[0]  # 工作经验
                    totalnum =  news.xpath('li[7]/strong/text()')[0] # 招聘人数
                    totalnum =totalnum.replace(u'人','') # 将中文字符替换掉
                    #print title,company,zwyx,gzdd,fbtime,experence,totalnum
                    detail =[title,company,zwyx,gzdd,fbtime,experence,totalnum]
                    # print detail

                # detail_news.append(detail)
                # print detail_news

                # self.save_excel(detail_news)
                # self.save_mysql(detail_news)
                # self.save_csv(detail_news) # 将二维数组的数据结构，利用csv文件的生成方式更加便捷


    def save_csv(self,detail_news):
        with open ('myjobt.csv','wb') as f:   # wb 的形式 ，就不会在生成的csv文件产生空行
            writer = csv.writer(f)
            writer.writerow(['title','company','zwyx','gzdd','fbtime','experence','totalnum']) #写入表头标题栏
            for row in detail_news: # 遍历detail里的数据，依次写入
                # print row
                writer.writerow(row)


    def save_excel(self,detail_news):
        shares = xlwt.Workbook(encoding='utf-8')
        sheet_name ='work'
        sheet = shares.add_sheet(sheet_name)
        sheet.write(0,0,'职位名称')  #  插入定义的 表标题
        sheet.write(0,1,'公司')
        sheet.write(0,2,'工作地点')
        sheet.write(0,3,'职位月薪')
        sheet.write(0,4,'发布时间')
        sheet.write(0,5,'工作经验')
        sheet.write(0,6,'招聘人数')
        for i, item in enumerate(detail_news):     # enumerate也可以遍历list
            sheet.write(i+1, 0, item[0]) # i+1 代表依次插入数据的行数，item[0]代表职位名称
            sheet.write(i+1, 1, item[1])  # item[1] 代表 公司
            sheet.write(i+1, 2, item[2])
            sheet.write(i+1, 3, item[3])
            sheet.write(i+1, 4, item[4])
            sheet.write(i+1, 5, item[5])
            sheet.write(i+1, 6, item[6])
            print (i+1,item[0])
        shares.save('shares.xls')


    def save_mysql(self,detail_news):
        # 先连接数据库
        conn =MySQLdb.connect(host = '127.0.0.1',user = 'root',passwd = '123456',charset = 'utf8',port = 3306)
        cur = conn.cursor()
        # cur.execute("drop database if exists new_database") # 如果new_database数据库存在则删除
        # cur.execute("create database new_database") #新创建一个数据库
        sql = 'create database if not exists new_database default charset utf8'
        cur.execute(sql)

        conn.select_db('new_database')

        sql = 'create table if not exists myresult'+"(id int auto_increment, title varchar(255), company varchar(255), \
        zwyx varchar(255),gzdd varchar(255), fbtime varchar(255), experence varchar(255), totalnum varchar(255), primary key(ID))"

        cur.execute(sql)

        for elem in detail_news:
            sql = 'insert into myresult(title,company,zwyx,gzdd,fbtime,experence,totalnum) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'\
             % tuple(elem)  #detail_news是一个二重数组list，我们需要将其转换成元组格式，插入到数据库中

        cur.execute(sql)

        print 'insert success!!!'   # 这里给个提示，每条数据是否插入成功

        conn.commit()
        cur.close()
        conn.close()


if __name__ == '__main__':
    object = ZhPinSpider()


