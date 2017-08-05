# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests,os

class TupianPipeline(object):
    def process_item(self, item, spider):
        sku = item['sku']
        url = item['image_url']
        img_url = url.replace("_340","1280")
        # 1280
        file_path = 'images/1280/'+sku+"_1.jpg"
        with open(file_path, 'wb') as handle:
                response = requests.get(img_url, stream=True)
                for block in response.iter_content(4096):
                    handle.write(block)

        #img 340
        file_path = 'images/img-340/'+sku+"_1.jpg"
        with open(file_path, 'wb') as handle:
            response = requests.get(url, stream=True)
            for block in response.iter_content(4096):
                handle.write(block)

         #sku 340
        file_path = 'images/sku-340/'+sku+'/'
        if os.path.isdir(file_path) == False:
            os.mkdir(file_path)
        file_path = 'images/sku-340/'+sku+'/'+sku+"_1.jpg"
        with open(file_path, 'wb') as handle:
            response = requests.get(url, stream=True)
            for block in response.iter_content(4096):
                handle.write(block)
        return item
