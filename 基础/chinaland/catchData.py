# -*- coding: utf-8 -*-

import re
import time
import requests


class CatchData(object):
    
    def __init__(self):
        self.postURL = 'http://www.landchina.com/default.aspx?tabid=226&ComName=default'

    def getAllPagerData(self, pagerSum):
        """
        获得每个细节页的URL地址
        """

        for i in range(1, pagerSum + 1):
            if i % 50 == 0:
                time.sleep(300)  # 到50页的时候就休息5分钟
                
            pagerNum = str(i)

            data = {'top1_QuerySubmitPagerData': pagerNum}

            response = requests.post(self.postURL, data=data)
            print response.text
 
            # try:
            #     response = urllib2.urlopen(request, timeout=30)  # 超时30s
            #
            #     status = response.getcode()
            #
            #     print '页码为%s,状态为%s' % (i, status)
            #
            # except urllib2.HTTPError, e:
            #     print 'The server couldn\'t fulfill the request.'
            #     print 'Error code: ', e.code
            #     self.writePagerToFile(i, e.code)
            #     continue
            #
            # except urllib2.URLError, e:
            #     print 'We failed to reach a server.'
            #     print 'Reason: ', e.reason
            #     self.writePagerToFile(i, e.reason)
            #     continue
            #
            # # 获得网页信息
            info = response.info()
            if int(info['Content-Length']) < 50000:  # 一般正常的页面大小在13万左右，这里用5万做判断标准，低于5万的是错误页面
                print '<50000'
                self.writePagerToFile(i, '<5000')
                continue

            # 读取网页内容
            content = response.read()

            file = open('c:/maintest.html', 'w')
            file.write(content)
            file.close()

            match = re.findall(r'wmguid=b07b0664-79e7-4458-90ea-519c65045c6b&(.*?) target="_blank"', content)

            matchSum = len(match)

            if matchSum == 0:
                self.writePagerToFile(i, 'error:连接数为0，发生错误')
                print '连接数为0，发生错误'
                continue

            if matchSum != 30:
                self.writePagerToFile(i, 'error:连接数不够30个,匹配数为%s，可能发生错误' % matchSum)

            urlList = [self.rootURL + url for url in match]

            self.getPagerData(urlList)


    def getPagerData(self, urlList):
        """
        获得一个页面30个细节页面，分析后将数据存入本地
        :param urlList:
        :return:
        """
        '''
        name="FormView21$p1_f1_r1_c2_ctrl"></span>宗地标识：
        name="FormView21$p1_f1_r1_c4_ctrl">030505000415</span></td>宗地编号：
        
        '''
        pattern1 = r'name="FormView21$p1_f1_r1_c2_ctrl">(.*?)</span></td>'
        pattern2 = r'name="FormView21$p1_f1_r1_c4_ctrl">(.*?)</span></td>'
        
        '''
        name="FormView21$p1_f1_r2_c2_ctrl">柳州市屏山大道278号长虹世纪12栋5单元2-4室</span>宗地座落：
        
        '''
        pattern3 = r'name="FormView21$p1_f1_r2_c2_ctrl">(.*?)</span></td>'
        
        '''
                        所在行政区：
        name="FormView21$p1_f1_r11_c2_ctrl"></span>
        name="FormView21$p1_f1_r11_c4_ctrl">450200000</span>
        '''
        pattern4 = r'name="FormView21$p1_f1_r11_c2_ctrl">(.*?)</span></td>'
        pattern5 = r'name="FormView21$p1_f1_r11_c4_ctrl">(.*?)</span></td>'
        
        '''
        name="FormView21$p1_f1_r3_c2_ctrl">康百育</span>原土地使用权人
        name="FormView21$p1_f1_r3_c4_ctrl">迟占坤</span></td> 现土地使用权人
        '''
        pattern6 = r'name="FormView21$p1_f1_r3_c2_ctrl">(.*?)</span></td>'
        pattern7 = r'name="FormView21$p1_f1_r3_c4_ctrl">(.*?)</span></td>'
        
        '''
        name="FormView21$p1_f1_r4_c2_ctrl">0.0018</span>土地面积(公顷)：
        name="FormView21$p1_f1_r4_c4_ctrl">其他普通商品住房用地</span> 土地用途：
        '''
        pattern8 = r'name="FormView21$p1_f1_r4_c2_ctrl">(.*?)</span></td>'
        pattern9 = r'name="FormView21$p1_f1_r4_c4_ctrl">(.*?)</span></td>'
        
        '''
        name="FormView21$p1_f1_r5_c2_ctrl"> 出让</span> 土地使用权类型：
        name="FormView21$p1_f1_r5_c4_ctrl">66</span> 土地使用年限
        '''
        pattern10 = r'name="FormView21$p1_f1_r5_c2_ctrl">(.*?)</span></td>'
        pattern11 = r'name="FormView21$p1_f1_r5_c4_ctrl">(.*?)</span></td>'
        
        '''
        name="FormView21$p1_f1_r6_c2_ctrl"> 已开发</span> 土地利用状况
        name="FormView21$p1_f1_r6_c4_ctrl">三级</span> 土地级别：
        '''
        pattern12 = r'name="FormView21$p1_f1_r6_c2_ctrl">(.*?)</span></td>'
        pattern13 = r'name="FormView21$p1_f1_r6_c4_ctrl">(.*?)</span></td>'
        
        '''
        name="FormView21$p1_f1_r8_c2_ctrl">买卖</span>  转让方式：
        name="FormView21$p1_f1_r8_c4_ctrl">27.0000</span></td>  转让价格(万元)
        '''
        pattern14 = r'name="FormView21$p1_f1_r8_c2_ctrl">(.*?)</span></td>'
        pattern15 = r'name="FormView21$p1_f1_r8_c4_ctrl">(.*?)</span></td>'
        
        '''
                        成交时间
        name="FormView21$p1_f1_r7_c2_ctrl">2009-4-16 15:42:13</span>
        name="FormView21$p1_f1_r7_c3_ctrl"></span></td>
        name="FormView21$p1_f1_r7_c4_ctrl"></span></td>
        '''
        pattern16 = r'FormView21$p1_f1_r7_c2_ctrl">(.*?)</span></td>'
        pattern17 = r'FormView21$p1_f1_r7_c3_ctrl">(.*?)</span></td>'
        pattern18 = r'FormView21$p1_f1_r7_c4_ctrl">(.*?)</span></td>'
        
        time.sleep(2)
        
        pattern = r'FormView21$p1_f1_r[1-8]{1,2}_c[24]_ctrl">(.*?)</span>'
        
        getHeader = {'Host': 'www.landchina.com',
                     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                     'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                     'Accept-Encoding': 'gzip, deflate',
                     'Referer': 'http://www.landchina.com/default.aspx?tabid=264&ComName=default',
                     'Connection': 'keep-alive',
                     'Cache-Control': 'max-age=0'
                     }
        
        getHeader = urllib.urlencode(getHeader)
        
        for url in urlList:
            
            try:
                req = urllib2.Request(url, getHeader)
                response = urllib2.urlopen(req)  # 超时30s
             
                status = response.getcode()
             
                print '链接地址为%s,状态为%s' % (url, status)
             
            except urllib2.HTTPError, e:  
                print 'The server couldn\'t fulfill the request.'  
                print 'Error code: ', e.code  
                self.writeUrlToFile(url)
                continue
              
            except urllib2.URLError, e:  
                print 'We failed to reach a server.'  
                print 'Reason: ', e.reason  
                self.writeUrlToFile(url)
                continue
            
            # 获得网页信息
            info = response.info()
            
            if int(info['Content-Length']) < 15000:  # 一般正常的页面大小在5万左右，这里用1.5万做判断标准，低于5万的是错误页面
                self.writeUrlToFile(url)
                continue
            
            # 读取网页内容
            content = response.read()  
            self.writeUrlToFile(content)
            
            file = open('c:/urltest.html', 'w')
            file.write(content)
            file.close()
            
            match = re.findall(pattern, content)
            
            for i in match:
                print i
             
    def writePagerToFile(self, pagerNum, errorInfo):
        '''将未成功响应的页码写入到文件中'''
        fileName = open(r'pagerNum.txt', 'a')
        fileName.write(('%s,%s') % (pagerNum, errorInfo))
        fileName.close()
        
    def writeUrlToFile(self, url):
        '''将未抓取成功的页面的URL写入文件中'''
        fileName = open(r'urls.txt', 'a')
        fileName.write(url)
        fileName.close()


if __name__ == '__main__':
    
    obj = CatchData()
    obj.getAllPagerData(500)
