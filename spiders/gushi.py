# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
import json
import re 
from gushispider.items import *


class GushiSpider(scrapy.Spider):
    name = 'gushi'
    allowed_domains = ['so.gushiwen.org']
    #start_urls=['https://so.gushiwen.org/authors/default.aspx?p=354&c=']
    start_urls=[]
    for i in range(1,355):
        url = 'https://so.gushiwen.org/authors/default.aspx?p=%d&c='%i
        start_urls.append(url)


    def parse(self, response):
        '''
        解析作者列表
        '''
        #author_urls = response.xpath('//a[contains(@href,"/authors/authorvsw")]/@href')
        results = response.xpath('//div[@class="sonspic"]')
        if results:
            for result in results:
                author_item = AuthorItem()
                author_item['start_url'] = response.url
                author_item['author'] = result.xpath('.//p[@style="height:22px;"]/a/b/text()').extract_first()
                author_item['jianjie'] = result.xpath('.//p[@style=" margin:0px;"]/text()').extract_first()
                author_item['num'] = int(re.findall(r'(\d*?)篇诗文',result.xpath('.//p[@style=" margin:0px;"]/a/text()').extract_first())[0])
                author_url = 'https://so.gushiwen.org' + result.xpath('.//p[@style=" margin:0px;"]/a/@href').extract_first()
                author_item['id'] = result.xpath('.//p[@style=" margin:0px;"]/a/@href').extract_first()
                author_item['first_url'] = author_url
                yield author_item

                yield scrapy.Request(author_url,callback=self.parse_authorpage)


    def parse_authorpage(self,response):
        '''
        解析单一作者作品列表
        '''
        pages = int(response.xpath('//div[@class="title"]/h1/span/text()').extract_first('0').split('/')[-1].replace(r'页',''))#获取当前页码
        print('page:%d'%pages)
        if pages:
            for page in range(1,pages+1):
                t2 = 'A%d.aspx'%page 
                url = response.url.replace('A1.aspx',t2)
                print('url:%s'%url)    
                yield scrapy.Request(url,callback=self.parse_authoronepage)
    def parse_authoronepage(self,response):
        '''
        解析单一作者作品一页
        '''
        result = response.xpath('//a')
        if result:
            gushi_item = GushispiderItem()
            turl = response.xpath('//a[contains(@href,"/shiwenv_")]/@href').extract()
            for i in range(1,len(turl)+1):
                shiwen_id = turl[i-1].split('_')[-1].split('.')[0]
                gushi_item['id'] = shiwen_id
                gushi_item['author_url'] = response.url
                gushi_item['url'] = 'https://so.gushiwen.org' + turl[i-1]
                t1 ='//div[@class="sons"][%d]//p/a/b/text()'%i
                gushi_item['title'] = response.xpath(t1).extract_first()
                t2 = '//div[@class="sons"][%d]//p[@class="source"]/a/text()'%i
                gushi_item['caodai'] = response.xpath(t2).extract_first()
                gushi_item['author'] = response.xpath(t2).extract()[1]
                t3 = '//div[@class="sons"][%d]//div[@class="tag"]/a/text()'%i
                gushi_item['tag'] = ','.join(response.xpath(t3).extract())
                t4 = '//div[@class="sons"][%d]//div[@class="contson"]//text()'%i
                gushi_item['content'] =''.join(response.xpath(t4).extract()).replace('\n','')                
                yield gushi_item

                yi_url = 'https://so.gushiwen.org/shiwen2017/ajaxshiwencont.aspx?id=%s&value=yi'%shiwen_id
                yield scrapy.Request(yi_url,callback=self.parse_yi)
                zhu_url = 'https://so.gushiwen.org/shiwen2017/ajaxshiwencont.aspx?id=%s&value=zhu'%shiwen_id
                yield scrapy.Request(zhu_url,callback=self.parse_zhu)
                shang_url = 'https://so.gushiwen.org/shiwen2017/ajaxshiwencont.aspx?id=%s&value=shang'%shiwen_id
                yield scrapy.Request(shang_url,callback=self.parse_shang)



    def parse_yi(self,response):
        '''
        解析单个作品的译文
        '''
        yi_zhu_shang_item = YiZhuShangItem()
        shiwen_id = re.findall('id=(.*?)&',response.url)[0]
        yi_zhu_shang_item['id'] = shiwen_id
        result = response.xpath('//p/span/text()').extract()
        yi_zhu_shang_item['yi'] = ''.join(result).replace('\n','')
        yield yi_zhu_shang_item

    def parse_zhu(self,response):
        '''
        解析单个作品的译文
        '''
        yi_zhu_shang_item = YiZhuShangItem()
        shiwen_id = re.findall('id=(.*?)&',response.url)[0]
        yi_zhu_shang_item['id'] = shiwen_id
        result = response.xpath('//p/span/text()').extract()
        yi_zhu_shang_item['zhu'] = ''.join(result).replace('\n','')
        yield yi_zhu_shang_item   

    def parse_shang(self,response):
        '''
        解析单个作品的译文
        '''
        yi_zhu_shang_item = YiZhuShangItem()
        shiwen_id = re.findall('id=(.*?)&',response.url)[0]
        yi_zhu_shang_item['id'] = shiwen_id
        result = response.xpath('//p//text()').extract()
        yi_zhu_shang_item['shang'] = ''.join(result).replace('\n','')
        yield yi_zhu_shang_item

        








