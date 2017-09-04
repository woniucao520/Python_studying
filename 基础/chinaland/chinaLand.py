# -*- coding: utf-8 -*-

import requests
import urllib
import urllib2
import re
import time
from bs4 import BeautifulSoup


class ChinaLand(object):
    """
    post方式，传入data与headers参数
    """
    def __init__(self):
        self.url = 'http://www.landchina.com/default.aspx?tabid=226&ComName=default'
        self.rooturl = 'http://www.landchina.com/'
        self.hearders = {
            "Host": "www.landchina.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Referer": "http://www.landchina.com/default.aspx?tabid=226&ComName=default",
            "ContenType": "application/x-www-form-urlencoded",
            "Content-Length": "2954",
            "Connection": "keep-alive"
        }


    def  get_one_page(self,pagerSum):
        """
        解析获取网页的html源代码,
        获取页面的所有url
        :return:
        """
        for i in range(1, pagerSum + 1):
            if i % 20 == 0:
                time.sleep(120)

            pagerNum = str(i)
            # urlencode将dict对象转换成url的请求参数
            data = urllib.urlencode({
                "hidComName": "default",
                "TAB_QuerySubmitPagerData": pagerNum  # 原来是通过传输这个PagerData给服务器实现翻页功能的
            })

        try:
            req = urllib2.Request(self.url, data=data)
            response = urllib2.urlopen(req, timeout=30)
            html = response.read()
            # print html
            '''
            <td class="gridTdNumber">61.</td>
            <a href="DesktopModule/BizframeExtendMdl/workList/bulWorkView.aspx?
            wmguid=6506735a-142d-4bde-9674-121656045ed1&recorderguid=c70e9a41-29cd-42f7-837d-7891df6752c5&sitePath="
            '''
            match = re.findall('.*?<td class="queryCellBordy"><a href="(.*?)" target="_blank">', html)
            # match = re.compile('.*?<td class="gridTdNumber">(.*?)</td>.*?<a href="(.*?)" target="_blank">',re.S)
            # items = re.findall(match,html)
            # print items
            urlList = [self.rooturl + url for url in match]
            # print urlList
            self.detail_news(urlList)  # 刚开始没写这句，导致detail_news()解析不出结果

        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"中国土地网获取失败,错误原因",e.reason
                return None


    def detail_news(self,urlList):
        """
        采集每个详情页url_detail所提供的信息
        """
        for url_detail in urlList:
        #     # print url_detail
        #     try:
        #         response = requests.get(url_detail, headers=self.hearders)
        #     except Exception as e:
        #         print '抓取网页出现错误,错误为:%s' % e
        #         return None
        #
        # if response.status_code == 200:
        #     web_content = BeautifulSoup(response.text, 'lxml')  # 可能是我电脑的问题，感觉用beautifulsoup解析时速度很慢
        #     print web_content
        #     """
        #     print web_content得到的并不是我想要的网页源码，导致接下来卡了好久也没匹配到表格数据
        #     然后就参考你的代码，才用urllib2解析，得到的也不是符合需求的源码，（其实 你是对滴我后来验证了）
        #     从返回的结果里，并没有查找到
        #      name="FormView21$p1_f1_r7_c2_ctrl">2009-4-16 15:42:13</span>（这个格式的信息是真没找到）
        #     """
        #     news = web_content.find_all('table', class_='MsoNormalTable')
        #     print news
        # else:
        #     time.sleep(10)
        #     return None

            try:
                request = urllib2.Request(url_detail, headers=self.hearders)
                response = urllib2.urlopen(request,timeout=30)
                html_detail = response.read()
                pattern = re.compile('.*?<SPAN style="FONT-FAMILY: 宋体; mso-bidi-font-family: 宋体; mso-font-kerning: 0pt; mso-bidi-font-size: 10.5pt">(.*?)<SPAN lang=EN-US'
                                     + '.*?<SPAN lang=EN-US style="FONT-SIZE: 11pt">(.*?)<o:p></o:p></SPAN></SPAN></SPAN></P></TD>'
                                     +'.*?<SPAN lang=EN-US style="COLOR: black; FONT-FAMILY: 宋体; mso-bidi-font-family: 宋体; mso-font-kerning: 0pt; mso-bidi-font-size: 10.5pt">(.*?)<o:p></o:p>',re.S)
                items = re.findall(pattern, html_detail)
                # print items # 结果空，有时会出现长时间在运行，但又不报错的情况
                for item in items:
                    print item[0], item[1], item[2]  # 结果 空 空 空，参考你的代码也解决不了了，这边整整卡了周二周三两个晚上，捣鼓了好久，代码页也分析了

            except urllib2.URLError, e:
                if hasattr(e, "code"):
                    print e.code
                if hasattr(e, "reason"):
                    print e.reason

'''
<SPAN lang=EN-US style="COLOR: black; FONT-FAMILY: 宋体; mso-bidi-font-family: 宋体; mso-font-kerning: 0pt; mso-bidi-font-size: 10.5pt">5000<o:p></o:p></SPAN></SPAN></SPAN></P></TD><SPAN style="mso-bookmark: _Toc316220268"><SPAN style="mso-bookmark: _Toc286257541"></SPAN></SPAN>
<SPAN lang=EN-US style="COLOR: black; FONT-FAMILY: 宋体; mso-bidi-font-family: 宋体; mso-font-kerning: 0pt; mso-bidi-font-size: 10.5pt">2017-04<o:p></o:p></SPAN></SPAN></SPAN></P></TD><SPAN style="mso-bookmark: _Toc316220268"><SPAN style="mso-bookmark: _Toc286257541"></SPAN></SPAN>
<SPAN style="FONT-FAMILY: 宋体; mso-bidi-font-family: 宋体; mso-font-kerning: 0pt; mso-bidi-font-size: 10.5pt">宗地编号<SPAN lang=EN-US><o:p></o:p></SPAN></SPAN></SPAN></SPAN></P></TD>
<SPAN lang=EN-US style="FONT-SIZE: 11pt">2017001<o:p></o:p></SPAN></SPAN></SPAN></P></TD>
<SPAN lang=EN-US style="FONT-SIZE: 11pt; COLOR: black">71000<o:p></o:p></SPAN></SPAN></SPAN></P></TD>
<SPAN style="COLOR: black; FONT-FAMILY: 宋体; mso-bidi-font-family: 宋体; mso-font-kerning: 0pt; mso-bidi-font-size: 10.5pt">穆棱市共和乡<SPAN lang=EN-US><o:p></o:p></SPAN></SPAN></SPAN></SPAN></P></TD>
<SPAN lang=EN-US style="COLOR: black; FONT-FAMILY: 宋体; mso-bidi-font-family: 宋体; mso-font-kerning: 0pt; mso-bidi-font-size: 10.5pt">5000<o:p></o:p></SPAN></SPAN></SPAN></P></TD><SPAN style="mso-bookmark: _Toc316220268"><SPAN style="mso-bookmark: _Toc286257541"></SPAN></SPAN>
<SPAN lang=EN-US style="COLOR: black; FONT-FAMILY: 宋体; mso-bidi-font-family: 宋体; mso-font-kerning: 0pt; mso-bidi-font-size: 10.5pt">53400<o:p></o:p></SPAN></SPAN></SPAN></P></TD><SPAN style="mso-bookmark: _Toc316220268"><SPAN style="mso-bookmark: _Toc286257541"></SPAN></SPAN>

'''

if __name__ == '__main__':
    ChinaLand = ChinaLand()
    ChinaLand.get_one_page(2)

