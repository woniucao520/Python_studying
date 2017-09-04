# -*- coding: utf-8 -*-
import re
import requests
import time
from bs4 import BeautifulSoup
import json

url = 'https://s.taobao.com/search?q=%E8%9B%8B%E7%B3%95&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20170731&ie=utf8'
response = requests.get(url)
soup = BeautifulSoup(response.text,'lxml')
news_pattern = re.compile(r'{"pageName":"mainsrp",.*?false}}', re.S|re.M|re.I)
web_content = re.search(news_pattern, response.text)
result = web_content.group()  # 获得json格式
pagejson = json.loads(result) # 将str转换成dic

print type(pagejson)
for price in pagejson['mods']['itemlist']['data']['auctions']:
    news = price['view_price']
    print news





