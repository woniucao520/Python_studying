# -*- coding: utf-8 -*-
import re

import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import time
import xlwt,re

class CatchData(object):

    def __init__(self):
        self.rootURL = 'http://www.grandever-china.com/'


    def get_page_index(self):
        try:
            response = requests.get(self.rootURL)
            if response.status_code == 200:
                web_content = BeautifulSoup(response.text, 'lxml')
                soup = web_content.find_all('div', class_='dt')

                for item in soup:
                    index_html = item.find_all('a', class_='a')[0].get('href')  # 得到category-14-b0.html  八个系列的url
                    first_id = item.find_all('a', class_='a')[0].get('href').split('-')[1]  # 得到id 14
                    category_list =[self.rootURL + index_html]
                    # href = item.find_all('a', class_='a')[0].get('href').split('.')[0]  #  得到category-39-b0，拼接子页
                    # start_url = [self.rootURL + href + url for url in self.roothtml]
                    #print(start_url)
                    self.get_category_list(category_list)
        except ConnectionError:
            print('Error occurred')
            return None
    '''
    获取所有分类页面
    '''
    def get_category_list(self, category_list):
        for category_url in category_list:
            curr_category_list = []
            category_id = self.getBetweenStr(category_url,'category-','-b0')
            response = requests.get(category_url)
            if response.status_code == 200:
                 soup = BeautifulSoup(response.text, 'lxml')
                 last_page_html = soup.find(attrs={'class':'last'})  # http://www.grandever-china.com/category-14-b0.html
                 if last_page_html != None:
                    href_str = last_page_html.get('href')
                    max_page = self.getBetweenStr(href_str,'attr0-','-shop')
                    for i in range(1,int(max_page)+1):
                        curr_category_list.append(self.rootURL+'category-'+str(category_id)+'-b0-min0-max0-attr0-'+str(i)+'-shop_price-DESC.html')
                 else:
                    curr_category_list.append(category_url)
            self.get_detail_news(curr_category_list, category_id)
        pass
    '''
    循环分类页数据 获取产品url
    '''
    def get_detail_news(self, curr_category_list, category_id):
        for new_url in curr_category_list:
            try:
                response = requests.get(new_url)
                if response.status_code == 200:
                    web_content = BeautifulSoup(response.text, 'lxml')
                    soup =web_content.find_all('div', class_='goodsItem')
                    result = []
                    for item in soup:
                        last_url ='http://www.grandever-china.com/'+ item.a.get('href')
                        result.append(last_url)
                    self.get_detail_page(result)
                else:
                    return None
            except ConnectionError:
                print('Error occurred')
                return None

    '''
    获取产品页面信息
    '''
    def get_detail_page(self,result):
        for url in result:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    web_content = BeautifulSoup(response.text, 'lxml')
                    news = web_content.select('#goodsInfo')
                    #attributes
                    attributes = web_content.select(".ul2 > li > dd")
                    #price
                    price = attributes[0].select("#ECS_SHOPPRICE")[0].text
                    special_price = attributes[0].select(".market")[0].text
                    #sku
                    sku = attributes[1].contents[-1]
                    #type
                    type = ''
                    if attributes[3].a != None:
                        type = attributes[3].a.text
                    #weight
                    weight = attributes[4].contents[-1]
                    #create at
                    create_at = attributes[5].contents[-1]

                    tire_price = web_content.find(attrs={'bgcolor':'#aad6ff1'})
                    if tire_price != None:
                        print tire_price

                    id = self.getBetweenStr(url,'goods-','.html') # id
                    http_url = url  # http
                    title = web_content.find('div', class_='textInfo').h1.text #title



                    ### gallery 图片属性的获取与下载
                    gallery = []
                    images = web_content.findAll(attrs={'rel': 'zoom1'})
                    for child in images:
                        img_src =child.find('img').get('src')  # images/201703/thumb_img/672_thumb_P_1489015035980.jpg
                        img_id = img_src.split('/')[-1].split('_')[0]+'_1.jpg'
                        #img_ids 得到 672_1.jpg//672_2.jpg
                        img_ids = img_src.split('/')[-1].split('_')[0]+'_1.jpg'+'//'+img_src.split('/')[-1].split('_')[0]+'_2.jpg'
                        img_url = [self.rootURL + img_src ] # http://www.grandever-china.com/images/201703/thumb_img/672_thumb_P_1489015035218.jpg
                        for each in img_url:
                            try:
                                pic = requests.get(each, timeout=10)
                            except requests.exceptions.ConnectionError:
                                print '当前图片无法下载'
                                continue
                            fpath = 'pictures\\' + img_id
                            fp = open(fpath, 'wb')
                            fp.write(pic.content)
                            fp.close()

                    # 获取商品表格属性: 需要判断



            #         new_result = []
            #         for item in news:
            #             title = item.find('div', class_='textInfo').h1.text # 标题
            #             price = item.find('font', class_='shop').text # 售价
            #             numbers = item.find_all('li', class_='clearfix')[1].dd.contents[-1]  # 商品货号
            #             kucun = item.find_all('li', class_='clearfix')[2].dd.contents[-1]  #  库存
            #             try:
            #                 types = item.find_all('li', class_='clearfix')[3].dd.a.text  # 商品品牌
            #             except:
            #                 types = ''
            #             weight = item.find_all('li', class_='clearfix')[4].dd.contents[-1] # 重量
            #             trs = item.find_all('tr')  #
            #             if len(trs)==4:
            #                 price2 =trs[2].contents[-2].text
            #                 price3 =trs[3].contents[-2].text
            #             elif len(trs)==3:
            #                 price2  =trs[2].contents[-2].text
            #                 price3 = ''
            #             else:
            #                 price2 = ''
            #                 price3 = ''
            #
            #             price_all = price + '/' + price2  + '/' + price3  # 价格梯度 930/925/915
            #             new_result.append([title, numbers, kucun, types, weight, price_all])
            #             self.save_news_excel(new_result)
            # except ConnectionError:
            #     print('Error occurred')
            #     return None



    def save_news_excel(self,new_result,sheet_name = 'phone'):
        shares = xlwt.Workbook(encoding='utf-8')
        sheet = shares.add_sheet(sheet_name)
        sheet.write(0,0,'商品标题')
        sheet.write(0,1,'货号')
        sheet.write(0,2,'库存')
        sheet.write(0,3,'类型')
        sheet.write(0,4,'重量')
        sheet.write(0,5,'价格梯度')
        for i, item in enumerate(new_result):     # enumerate也可以遍历list
            sheet.write(i+1, 0, item[0])
            sheet.write(i+1, 1, item[1])
            sheet.write(i+1, 2, item[2])
            sheet.write(i+1, 3, item[3])
            sheet.write(i+1, 4, item[4])
            sheet.write(i+1, 5, item[5])
        shares.save('shares.xls')

    def getBetweenStr(self,html,start,end):
        pat = re.compile(start + '(.*?)' + end, re.S)
        str = pat.findall(html)
        if str:
            str = str[0]
        else:
            str = ''
        return str

if __name__ == '__main__':
    obj = CatchData()
    obj.get_category_list()

