# coding=utf-8

import re
import requests
from bs4 import BeautifulSoup

from mylog import MyLog as mylog
from save2excel import SaveBallDate

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class DoubleColorBallItem(object):
    data = None  # 开奖日期
    order = None  # 期号
    # red1 = None  # 红球
    # red2 = None
    # red3 = None
    # red4 = None
    # red5 = None
    # red6 = None
    # blue = None  # 蓝球
    num = None  # 中奖号码
    money = None  # 彩池金额
    firstPrize = None  # 一等奖中奖人数
    secondPrize = None  # 二等奖中奖人数


class GetDoubleBallNumber(object):

    def __init__(self):
        self.urls = []
        self.log = mylog()
        self.getUrls()
        self.items = self.spider(self.urls)
        self.pipelines(self.items)
        SaveBallDate(self.items)

    def getUrls(self):
        URL = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html'
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'lxml')
        tag = soup.find_all('p',attrs={'class':'pg'})[0]
        pagenum = tag.strong.get_text()
        for i in range(1, 5):
            url = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list_%s.html' % str(i)
            self.urls.append(url)
            # self.log.info(u'添加URL:%s到URLS\r\n'% url)

    def getResponseContent(self, url):
        '''
        单独用一个函数返回页面的返回值，为后期 方便加proxy和headers
        '''
        try:
            response = requests.get(url)
            #response = requests.get(page_url, headers=header, proxis=proxy)
        except Exception as e:
            print '抓取网页出现错误,错误为:%s' % e
            self.log.error(u'Python返回URL:%s 数据失败 \r\n' % url)
        # else:
        #     self.log.info(u'Python返回URL:%s 数据成功 \r\n'% url)

    def spider(self, urls):
        items = []
        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text,'lxml')
            tags = soup.find_all('tr',attrs={})
            for tag in tags:
                if tag.find('em'):
                    item =DoubleColorBallItem()
                    tagTd = tag.find_all('td')
                    item.data = tagTd[0].get_text()
                    item.order =tagTd[1].get_text()
                    tagEm = tagTd[2].find_all('em')
                    red1 = tagEm[0].get_text()
                    red2 = tagEm[1].get_text()
                    red3 = tagEm[2].get_text()
                    red4 = tagEm[3].get_text()
                    red5 = tagEm[4].get_text()
                    red6 = tagEm[5].get_text()
                    blue = tagEm[6].get_text()
                    item.num = red1 + red2 +red3 +red4 +red5 +red6 +blue
                    item.money = tagTd[3].find('strong').get_text()
                    item.firstPrize = tagTd[4].find('strong').get_text()
                    item.secondPrize = tagTd[5].find('strong').get_text()
                    items.append(item)
                    # self.log.info(u'获取日期为:%s的数据成功' % (item.data))
        print items
        return items

    def pipelines(self, items):
        fileName = u'双色球.txt'
        with open(fileName, 'w') as fp :
            for item in items:
                print item
                fp.write('%s %s \t  %s \t %s \t %s  %s \n'%\
                ( item.data, item.order,item.num,item.money,item.firstPrize,item.secondPrize))


if __name__ == '__main__':
    object = GetDoubleBallNumber()