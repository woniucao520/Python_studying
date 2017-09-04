# -*- coding: utf-8 -*-
import settings, requests, os
from lxml import etree
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class KlcaoPipeline(object):
    def process_item(self, item, spider):

        sku = item['sku']
        gallery_image = item['gallery']
        description = item['img_description']

        dir_path = settings.IMAGES_STORE
        # 下载产品主图
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        i = 0
        for img_url in item['gallery']:

            if i == int(i)+ 1:
                continue;
            image_name = sku + '_800' + str(i) + '.jpg'
            file_path = '%s/%s' % (dir_path, image_name)
            with open(file_path,'wb') as handle:
                response = requests.request(img_url)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
            i = int(i) + 1
        return  item




