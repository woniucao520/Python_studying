# encoding:utf-8
import requests
from lxml import etree
import csv

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_all_url():
    urls=[]
    for i in range(1, 3):
        page_url = 'http://data.stcn.com/list/djsj_%s.shtml' % i
        urls.append(page_url)
    return urls


def parse_url(url):
    result = []
    if requests.get(url,headers=headers).status_code == 200:
        response=requests.get(url,headers=headers)
        selector = etree.HTML(response.text)
        web_content = selector.xpath('//p[@class="tit"]')
        for news in web_content:
            item_result = {}
            item_result['href'] = news.xpath('a/@href')[0]
            item_result['title'] = news.xpath('a/text()')[0]
            item_result['date'] = news.xpath('span/text()')[0]
            result.append(item_result)
    print(result)
    return result

def save_news_csv(result):
    for row in result:
        w.writerow(row.values())
        print ("写入成功！")

def get_fieldnames(urls):
    for url in urls:
        result = parse_url(url)
        fieldnames = result[0].keys()
    return fieldnames

if __name__ == '__main__':
    headers={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    urls=get_all_url()
    fieldnames=get_fieldnames(urls)
    with open('result.csv', 'wb') as f:
        w = csv.writer(f)
        w.writerow(fieldnames)
        for url in urls:
            result=parse_url(url)
            # if len(result) > 0:
            save_news_csv(result)



