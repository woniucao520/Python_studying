# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import settings, requests, os
from lxml import etree

class KaolaPipeline(object):
     def process_item(self, item, spider):
        dir_path = settings.IMAGES_STORE
        description = []
        id = item['id']
        sku = item['sku']
        description = item['description']
        gallery_images = []

        '''下载主图 并且改名字'''
        image_name = sku + "_800" + ".jpg"
        file_path = '%s/%s' % (dir_path+'product', image_name)
        image_url = item['image']
        with open(file_path, 'wb') as handle:
                response = requests.get(image_url, stream=True)
                for block in response.iter_content(2048):
                    handle.write(block)
        item['image'] = ''.join(image_name)

        '''下载多图 并且改名字'''
        i = 0
        for gallery_image in item['gallery']:
            if i == 0:
                i = int(i) + 1
                continue;
            image_name = sku + "_800" +str(i)+ ".jpg"
            file_path = '%s/%s' % (dir_path+'product', image_name)
            with open(file_path, 'wb') as handle:
                response = requests.get(gallery_image, stream=True)
                for block in response.iter_content(2048):
                    handle.write(block)
            i = int(i) + 1
            gallery_images.append(image_name)

        '''下载产品表述图 并且改名字'''
        des_tree = etree.HTML(description)
        des_list = des_tree.xpath('//img/@src')
        i = 1
        des_text = []
        for des_url in des_list:
            des_url = des_url.replace('http:','')
            des_url = "http:"+des_url
            if i <10:
                i = "0"+str(i)
            image_name = str(sku)+"_" + str(i) + ".jpg"
            product_name = item['name']

            file_path = dir_path+'description/'+sku
            if os.path.isdir(file_path) == False:
                os.mkdir(file_path)
            file_path = '%s/%s' % (file_path, image_name)
            full_path = '<img src="{{media url="wysiwyg/product/w/g/'+sku+'/' + image_name + '"}}" onerror=\'this.style.display="none"\' alt="' + product_name + '">'

            with open(file_path, 'wb') as handle:
                response = requests.get(des_url, stream=True)
                for block in response.iter_content(2048):
                    handle.write(block)
                des_text.append(full_path)
            i = int(i) + 1
        item['description'] = ''.join(des_text)
        item['gallery'] = '||'.join(gallery_images)
        return item
