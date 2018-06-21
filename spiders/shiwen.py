# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
import json
import re 
from gushispider.items import *


class GushiSpider(scrapy.Spider):
    name = 'shiwen'
    allowed_domains = ['haoshiwen.org']
    #start_urls=['http://www.haoshiwen.org/type.php??page=4&page=1']
    start_urls=[]
    for i in range(1,7638):
        url = 'http://www.haoshiwen.org/type.php??page=4&page=%d'%i
        start_urls.append(url)


    def parse(self, response):
        '''
        解析列表
        '''
        #author_urls = response.xpath('//a[contains(@href,"/authors/authorvsw")]/@href')       
        results = response.xpath('//div[@class="sons"]')
        if results:
            for result in results:
                shiwen_item = ShiwenItem() 
                shiwen_item['list_url'] = response.url               
                shiwen_item['title'] = result.xpath('.//a//text()').extract_first()
                shiwen_item['id'] = result.xpath('.//p/a/@href').extract_first().replace('/','')
                shiwen_url = 'http://www.haoshiwen.org/' + result.xpath('.//p/a/@href').extract_first().replace('/','')
                shiwen_item['shiwen_url'] =  shiwen_url
                shiwen_item['author'] = result.xpath('.//p[contains(@style,"color")]/text()').extract_first()
                yield shiwen_item
                yield scrapy.Request(shiwen_url,callback=self.parse_page)


    def parse_page(self,response):
        '''
        解析单一作者作品列表
        '''
        shiwen_item = ShiwenItem()
        shiwen_item['id'] =  response.url.split('/')[-1]
        shiwen_item['caodai'] = response.xpath('//div[@class="shileft"]/div[@class="son2"]/p/text()').extract_first()
        shiwen_item['tag'] = ','.join(response.xpath('//div[@class="shisonconttag"]/a/text()').extract())
        result = response.xpath('//div[@class="shileft"]/div[@class="son2"]/p//text()').extract()
        content = ''.join(result).replace('\r','').replace('\n','').strip(' ')
        shiwen_item['content'] = content 
        yield shiwen_item
 







