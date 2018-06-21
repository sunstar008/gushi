# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GushispiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'gushi'
    author_url = scrapy.Field()
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    caodai = scrapy.Field()
    author = scrapy.Field()
    tag = scrapy.Field()
    content = scrapy.Field()
    yi = scrapy.Field()
    zhu = scrapy.Field()
    shang = scrapy.Field()
class YiZhuShangItem(scrapy.Item):
    collection = 'gushi'
    id = scrapy.Field()
    yi = scrapy.Field()
    zhu = scrapy.Field()
    shang = scrapy.Field()   

class AuthorItem(scrapy.Item):
    collection = 'author'
    id = scrapy.Field()
    start_url = scrapy.Field()
    author = scrapy.Field()
    jianjie = scrapy.Field()
    num = scrapy.Field()
    first_url = scrapy.Field()
class GuwenItem(scrapy.Item):
    collection = 'guwen'
    book_url = scrapy.Field()
    title = scrapy.Field()
    id = scrapy.Field()
    sector_url = scrapy.Field()
    sector_name = scrapy.Field()
    content = scrapy.Field()
class ShiwenItem(scrapy.Item):
    collection = 'shiwen'
    list_url = scrapy.Field()
    title = scrapy.Field()
    id = scrapy.Field()
    caodai = scrapy.Field()
    shiwen_url = scrapy.Field()
    author = scrapy.Field()
    tag = scrapy.Field()
    content = scrapy.Field()


