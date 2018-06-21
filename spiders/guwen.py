# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
import json
import re 
from gushispider.items import *


class GushiSpider(scrapy.Spider):
    name = 'guwen'
    allowed_domains = ['haoshiwen.org']
    #start_urls=['http://www.haoshiwen.org/book.php?id=1']
    start_urls=[]
    for i in range(1,88):
        url = 'http://www.haoshiwen.org/book.php?id=%d'%i
        start_urls.append(url)


    def parse(self, response):
        '''
        解析列表
        '''
        #author_urls = response.xpath('//a[contains(@href,"/authors/authorvsw")]/@href')
        #
        title  = response.xpath('//div[@class="son2Title2"]//text()').extract_first().replace(r'在线阅读','')
        results = response.xpath('//div[@class="guwencont2"]/a')
        if results:
            for result in results:
                guwen_item = GuwenItem() 
                guwen_item['book_url'] = response.url               
                guwen_item['title'] = title
                guwen_item['id'] = result.xpath('./@href').extract_first()
                sector_url = 'http://www.haoshiwen.org/' + result.xpath('./@href').extract_first()
                guwen_item['sector_url'] = sector_url
                guwen_item['sector_name'] = result.xpath('.//text()').extract_first()
                yield guwen_item
                yield scrapy.Request(sector_url,callback=self.parse_sectorpage)


    def parse_sectorpage(self,response):
        '''
        解析单一作者作品列表
        '''
        guwen_item = GuwenItem()
        guwen_item['id'] = response.url.split('/')[-1]
        result = response.xpath('//div[@class="authorShow"]/p/text()').extract()
        content = ''.join(result).replace('\r','').replace('\n','').strip(' ')
        if len(content)==0:
            result = response.xpath('//div[@class="authorShow"]//text()').extract()
            content = ''.join(result).replace('\r','').replace('\n','').replace("[下一章>>]",'').replace("[返回目录▲]",'').split("script>');")[-1].strip(' ') 
        guwen_item['content'] = content 
        yield guwen_item
 







