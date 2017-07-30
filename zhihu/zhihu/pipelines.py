# -*- coding: utf-8 -*-
import pymongo
from scrapy.conf import settings
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ZhihuPipeline(object):
    def __init__(self):
        #pymongo.MongoClient连接到数据库
        connection = pymongo.MongoClient(settings['MONGODB_HOST'],settings['MONGODB_PORT'])
        # 创建数据库名称
        db = connection[settings['MONGODB_NAME']]
        #连接的数据集，为dict
        self.post = db[settings['MONGODB_DOCNAME']]
    def process_item(self, item, spider):
        self.post.update({'url_token': item['url_token']},{'$set':dict(item)},upsert=True) # set主要是用来去重的
        print u'插入成功'
        return item
