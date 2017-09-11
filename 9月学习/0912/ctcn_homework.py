# -*- coding: UTF-8 -*-

import requests
from lxml import etree
import csv
import MySQLdb

import Queue
import threading
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# from util.crawler import Header, Proxy  代理 请求头 我放在另个文件夹
# from database.db import Database
#
# con = Database.getConnection()   # 连接数据库
# cur = con.cursor()   # 游标对象

def get_news_url(start_url, result_queue):
    result = []
    while start_url.qsize():

        page_url = start_url.get() # 从队列中移除并返回这个数据
        try:
            # header = Header.get()
            # proxy = Proxy.get()
            response = requests.get(page_url)
        except Exception as e:
            print "抓取网页错误,错误为：%s" % e
            return None

        if response.status_code == 200:
            selector = etree.HTML(response.text)
            web_content = selector.xpath('//p[@class="tit"]')
            for news in web_content:
                item_result = {}
                item_result['href'] = news.xpath('a/@href')[0]
                item_result['title'] = news.xpath('a/text()')[0]
                item_result['date'] = news.xpath('span/text()')[0]
                result.append(item_result)
                # href = news.xpath('a/@href')[0]  这部分我存入数据库用，变成二维数组，字典格式的我竟然存不进去
                # title =news.xpath('a/text()')[0]
                # date =news.xpath('span/text()')[0]
                # web_news= [href,title,date]
                # result.append(web_news)
                # save_news_mysql(result)
            print result
            save_news_csv(result)
            save_file_csv(result)
            if len(result) > 0:
                result_queue.put(result)
                start_url.task_done()
        else:
            time.sleep(5)

def save_news_csv(list):
    with open('123456.csv','wb') as f:
        w = csv.writer(f)
        fieldnames = list[0].keys()
        w.writerow(fieldnames)

def save_file_csv(list):
    with open('123456.csv','wb') as f:
        w = csv.writer(f)
        for row in list:
            w.writerow(row.values())
            print ("写入成功！")

'''
有什么方法可以将[{}，{}，{}]这种形式的结构，插入到数据库中吗？
我是[[]，[]，[]]结构，一条一条的存的
'''
def save_news_mysql(result):

    con =MySQLdb.connect(host = '127.0.0.1',user = 'root',passwd = '123456',charset = 'utf8',port = 3306)
    cur = con.cursor() # 数据库都是游标来操作的
    sql = 'create database if not exists stcnnews default charset utf8'
    cur.execute(sql) #创建数据库，注意编码格式为utf8


    sql = 'create table if not exists news_zqsb'+"(id int auto_increment, href varchar(255), title varchar(255), \
    news_date varchar(255), primary key(ID))"

    cur.execute(sql) #

    for elem in result:
        sql = 'insert into news_zqsb(href,title,news_date) values(\'%s\',\'%s\',\'%s\')'\
         % tuple(elem)  # detail_news是一个二重数组list，我们需要将其转换成元组格式，插入到数据库中

    cur.execute(sql)
    print 'insert success!!!'   # 这里给个提示，每条数据是否插入成功

    con.commit()  #一定要有commit提交，不然数据库里没有数据
    cur.close()
    con.close()


def main():
    start_url = Queue.Queue()  # 存放url的队列
    result_queue = Queue.Queue()
    for i in range(1, 3):
        page_url = 'http://data.stcn.com/list/djsj_%s.shtml' % i
        start_url.put(page_url)  # 将值插入队列中
    # 构建线程
    thread_list = []
    for n in range(4):  # 创建4 个线程
        t_t = threading.Thread(target=get_news_url, args=(start_url, result_queue))  # 创建线程，调用get_news_url方法,args传入参数
        thread_list.append(t_t)
    for t in thread_list:
        t.start()

    # while result_queue.qsize(): # 返回队列的大小
    #     save_news_mysql('news_zqsb', result_queue.get())


if __name__ == "__main__":
    main()
