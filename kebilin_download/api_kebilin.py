# -*- coding: utf-8 -*-
import urllib2
from odoo import models, fields
from odoo.osv import osv
from datetime import datetime, timedelta
import hashlib
import json
import tempfile
import zipfile
import os
from openpyxl import Workbook
import requests
from lxml import etree


class ApiKebilin(osv.osv):

    _name = 'api.kebilin'

    api_url = 'http://api.kebilin.com'
    user_code = 'test'
    password = 'nh123467'
    secret_key = '4122e029f305f66dfb62849fe97f83abc7c46be1'
    SourceDealerShop = '25'
    SourcePlatform = ''

    def commonPost(self, method, data):
        head = {}
        url = self.api_url
        userid = self.SourceDealerShop or ''
        secert = self.secret_key or ''
        timestamp = datetime.strftime(datetime.now() + timedelta(hours=8), '%Y-%m-%d %H:%M:%S')

        md5_str = userid + secert + timestamp

        md5_encode = hashlib.md5()
        md5_encode.update(md5_str)
        sign = md5_encode.hexdigest()

        head['userid'] = userid
        head['timestamp'] = timestamp
        head['sign'] = sign
        head['f'] = method
        data['head'] = head

        data = json.dumps(data)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        res = response.read()
        return res

    #获取产品信息
    def getProductInfo(self, serial, page_size=100):
        method = 'get_goods_list'
        data = {
            'body': {
                'serial': serial,
                'page_size': page_size,
            }
        }
        res = self.commonPost(method, data)
        return res

    # 创建主文件夹
    def create_main_folder(self):
        mkfile_time = datetime.strftime(datetime.now() + timedelta(hours=8), '%Y%m%d%H%M%S')
        mkfile_time = 'kbl'+mkfile_time

        # 创建临时文件夹
        t = tempfile.mkdtemp()   # 创建临时目录
        mypath = t + '/' + mkfile_time

        if not os.path.exists(mypath):
            os.makedirs(mypath)
        return mypath

    # 创建Excel
    def create_excel_file(self, res, mypath):
        result = res['root']['body']
        # 实例化一个Workbook()对象(即excel文件)
        wbk = Workbook()
        ws = wbk.active

        header_list = ['vendor_code', 'gallery', 'description', 'weight', 'type_id', 'color', 'image',
                       'product_sync_type', 'price', 'special_price', 'qty', 'short_description', 'size',
                       'sku', 'name', 'brand', 'categories', 'attribute_set', 'country', 'warehouse', 'barcode']
        # 添加标题行
        ws.append(header_list)

        # 循环插入明细行
        for r in result:
            images = 'images' in r.keys() and r['images'] or ''
            content = 'content' in r.keys() and r['content'] or ''
            price = 'price' in r.keys() and r['price'] or 0
            name = 'goods_name' in r.keys() and r['goods_name'] or ''
            barcode = 'barcode' in r.keys() and r['barcode'] or ''
            country = 'madein' in r.keys() and r['madein'] or ''
            if country == u'台湾' or country == u'香港':
                country = u'中国' + country

            sku = 'sn' in r.keys() and 'kbl' + r['sn'].lower() or ''
            # 获取重量
            skus = 'skus' in r.keys() and  r['skus'] or ''

            if skus and ('sku' in skus.keys()) and skus['sku']:
                weight = skus['sku']['weight'] or 0.5
                qty = skus['sku']['stock'] or 0
                qty = qty > 10 and qty - 10 or 0
            else:
                weight = 0.5
                qty = 0

            vendor_code = 9000
            type_id = 'simple'
            product_sync_type = u'售卖且不需要同步'
            warehouse = u'青岛1号仓'
            default_image = sku + '_8001.jpg'

            gallery = ''
            description = ''

            # 主图
            for image in range(0, len(images)):
                if gallery:
                    gallery += '||'

                gallery += sku + '_800' + str(image + 1) + '.jpg'

            content_list = content.split('<img')
            # 详细内容
            for con in range(1, len(content_list)-1):
                content_add = '<img src="{{media url="wysiwyg/product/k/b/' + sku + '/' + sku + '_' + str(con).zfill(2) + '.jpg"}}" alt="' + name + '" />'
                description += content_add

            rows = []
            rows.append(vendor_code)

            rows.append(gallery)
            rows.append(description)
            rows.append(weight)
            rows.append(type_id)
            rows.append('')

            rows.append(default_image)
            rows.append(product_sync_type)
            rows.append(price)
            rows.append('')
            rows.append(qty)

            rows.append('')
            rows.append('')
            rows.append(sku)
            rows.append(name)
            rows.append('')

            rows.append('')
            rows.append('')
            rows.append(country)
            rows.append(warehouse)
            rows.append(barcode)

            ws.append(rows)

        # 保存Excel。
        wbk.save(mypath + '/kebilin_products.xlsx')

    def download_image(self, res, mkfile_time):
        for d in res['root']['body']:
            if 'images' in d.keys() and d['images']:
                image = d['images']
            else:
                continue

            if 'content' in d.keys() and d['content']:
                description = d['content']
            else:
                continue

            if 'sn' in d.keys() and d['sn'] and d['sn'] != None:
                new_sku = 'kbl'+ d['sn'].lower()
            else:
                continue

            des_tree = etree.HTML(description)
            des_list = des_tree.xpath('//img/@src')

            i = 1
            #  下载产品详细图
            for list in des_list:
                list = ''.join(list) # 转换成str
                if 'top.jpg' in list:  # 判断字符串里是否含有‘top’,主要是去除出第一张图片
                    continue

                images_name = new_sku + '_' + str(i).zfill(2) + '.jpg'
                i += 1

                fpath = mkfile_time + os.sep + new_sku
                if not os.path.exists(fpath):
                    os.makedirs(fpath)  # makedirs 创建多级目录文件夹，mkdir创建一个文件夹

                try:
                    r2 = requests.get(list, timeout=0.1)
                except requests.exceptions.ConnectTimeout:
                    NETWORK_STATUS = False
                    continue
                except requests.exceptions.Timeout:
                    REQUEST_TIMEOUT = True
                    continue
                with open(fpath + '/' + images_name, "wb") as f:
                    f.write(r2.content)

                #print '产品详细图' + str(i).zfill(2)

            i = 1
            #  下载产品主图
            for url in image:
                url_images = url.values()
                url_images = ''.join(url_images)
                pack_name = new_sku + '-gallery'
                images_name = new_sku + "_800" + str(i) + ".jpg"
                i += 1

                fpath = mkfile_time + '/' + pack_name  # 指定放在D 盘 目录下
                if not os.path.exists(fpath):  # 以 sku命名 的 大的 文件夹
                    os.makedirs(fpath)  # makedirs 创建多级目录文件夹，mkdir创建一个文件夹

                try:
                    r2 = requests.get(url_images)
                except requests.exceptions.ConnectTimeout:
                    NETWORK_STATUS = False
                    continue
                except requests.exceptions.Timeout:
                    REQUEST_TIMEOUT = True
                    continue
                with open(fpath + '/' + images_name, "wb") as f:
                    f.write(r2.content)

                #print '产品主图' + str(i).zfill(2)

        return True

    def file_pack(self, mypath):  # 下载文件打包
        zip_filename = mypath + '.zip'
        mypath = mypath + os.sep

        z = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(mypath):
            arcname = dirpath.replace(mypath, '')
            arcname = arcname and arcname + os.sep or ''

            for filename in filenames:
                z.write(os.path.join(dirpath, filename), arcname + filename)

        z.close()
        return zip_filename