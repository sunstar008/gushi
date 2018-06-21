# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import Request
from scrapy.exceptions import DropItem
from gushispider.items import *

class GushispiderPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[GushispiderItem.collection].create_index([('id', pymongo.ASCENDING)])
        self.db[AuthorItem.collection].create_index([('id', pymongo.ASCENDING)])

    def process_item(self, item, spider):
        if isinstance(item, GushispiderItem) or isinstance(item, YiZhuShangItem):
            self.db[item.collection].update({'id': item.get('id')}, {'$set': item}, True)
        if isinstance(item, AuthorItem):
            #self.db[item.collection].insert(dict(item))
            self.db[item.collection].update({'id': item.get('id')}, {'$set': item}, True)
        if isinstance(item, GuwenItem) or isinstance(item, ShiwenItem):
            self.db[item.collection].update({'id': item.get('id')}, {'$set': item}, True)        
        return item
    
    def close_spider(self, spider):
        self.client.close()