# -*- coding: utf-8 -*-
import re
import requests
import time
from bs4 import BeautifulSoup
import json

class CatchData(object):
    def __init__(self):
        '''
        http://maoyan.com/board/4?offset=10
        http://maoyan.com/board/4?offset=20
        '''
        self.rooturl = ["http://maoyan.com/board/4?offset={}".format(str(i)) for i in range(0, 20, 10)]

    def get_page_index(self):

        for url in self.rooturl:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    web_content = BeautifulSoup(response.text, 'lxml')
                    news_content = web_content.find_all('div', class_='board-item-content')
                    for item in news_content:
                        result = []
                        title = item.div.p.string
                        actor = item.select('.star')[0].string.strip()[3:]
                        time = item.select('.releasetime')[0].string
                        grade = item.select('.integer')[0].string + item.select('.fraction')[0].string
                        result.append([title, actor, time, grade])
						# result= ",".join(result)
                        self.write_to_file(result)
                else:
                # 休息10秒
                    time.sleep(10)
                    return None
            except Exception as e:
                print '抓取网页出现错误,错误为:%s' % e
                return None

    def write_to_file(self,result):
        with open('myfilms.txt','a') as f:  # myfilms里没有结果，好尴尬
            f.write(str(result) + '\n')
            f.close

if __name__ == '__main__':

    obj = CatchData()
    obj.get_page_index()







