# -*- coding: utf-8 -*-
import re
from mongodb import *   # mongdb的包需要导入
import requests
import time
from bs4 import BeautifulSoup
import json
from selenium.common.exceptions import TimeoutException
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]




url = 'https://s.taobao.com/search?q=%E8%9B%8B%E7%B3%95&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20170731&ie=utf8'
response = requests.get(url)
soup = BeautifulSoup(response.text,'lxml')
news_pattern = re.compile(r'{"pageName":"mainsrp",.*?false}}', re.S|re.M|re.I)
web_content = re.search(news_pattern, response.text)
result = web_content.group()  # 获得json格式
pagejson = json.loads(result) # 将str转换成dic
news_content = []
for price in pagejson['mods']['itemlist']['data']['auctions']:
    view_price = price['view_price']
    view_sales = price['view_sales']
    item_loc = price['item_loc']
    raw_title = price['raw_title']
    news = [view_price,view_sales,item_loc,raw_title]
    news_content.append(news)
print news_content

fpath = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
browser = webdriver.Chrome(fpath)
wait = WebDriverWait(browser, 10)


def search():
    url = 'https://www.taobao.com'
    browser.get(url)
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))).send_keys(u'蛋糕')
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))).click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        return total.text
        get_product()
    except TimeoutException:
        return search()  # 重新请求


def next_page(pagenum):
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
        input.clear()
        input.send_keys(pagenum)  # 执行翻页

        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit")))
        submit.click()  # 确定按钮的提交
      #  判断当前点击的页码数，是否在 totalpage 的页数当中
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(pagenum)))   # 这一步不要不行嘛
        get_product()
    except TimeoutException:
        next_page(pagenum)


def get_product():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))   # 这一步可以不要
    html = browser.page_source
    selector = etree.HTML(html)
    web_content = selector.xpath('//div[@class="ctx-box J_MouseEneterLeave J_IconMoreNew"]')
    for news in web_content:
        product = {
            'price' : news.xpath('div[@class="row row-1 g-clearfix"]/div[@class="price g_price g_price-highlight"]/strong/text()')[0] , # 返回的是数组形式
            'deal_cnt' :news.xpath('div[@class="row row-1 g-clearfix"]/div[@class="deal-cnt"]/text()')[0],
            'location':news.xpath('div[@class="row row-3 g-clearfix"]/div[@class="location"]/text()')[0],
            'shop': news.xpath('div[@class="row row-3 g-clearfix"]/div[@class="shop"]/a/span[2]/text()')[0]
        }
        print product
        save_to_monggodb(product)


def save_to_monggodb(product):
    try:
        if db[MONGO_TABLE].insert(product):
            print('存储到MONGODB成功', product)
    except Exception:
        print('存储到MONGODB失败', product)


def main():
    total = search()
    total = int(re.compile('(\d+)').search(total).group(1))  # 这一步不是很懂 获取100
    for i in range(2, total+1):
        next_page(i)


if __name__ == '__main__':
    main()


