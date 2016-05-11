# -*- coding: utf-8 -*-

import logging
import scrapy
import urllib
import codecs
import re
import copy

from scrapy.selector import Selector

from qcwy.items import QcwyItem

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#同一属性两个条件联合用,分隔
keyword = {
           "jobarea" : "020000,030200,010000,040000,080200,00",   #北上广深杭
           "industrytype" : "32",   #32表示互联网，42银行，03证券/金融，43保险
           "keyword" : "数据分析",
           "workyear" : "99",        #99表示所有，01无经验，02一到三年，03三到五年，04五到十年
            }
#把字符串编码成符合url规范的编码
keywordcode = urllib.urlencode(keyword)

is_start_page = True
has_tested = False

class TestfollowSpider(scrapy.Spider):
   
    name = "qcwysearch"
    allowed_domains = ["51job.com"]
    start_urls = [
        "http://my.51job.com/my/My_SignIn.php",
    ]
    count = 1
    cookies={'guide':'1' }
    def parse(self, response):
        login=scrapy.FormRequest.from_response(response,
                                               formdata={'username':'yiqiyu33@hotmail.com', 'userpwd':'D4a677,OP20'},
                                                callback=self.after_post)
        yield login
        
    def after_post(self, response):
        with open('after', 'wb') as f:
            f.write('start\r\n')
        with open('link', 'wb') as f:
            f.write('start\r\n')
        url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&funttype=0000&"+keywordcode
        return scrapy.Request(url,cookies=self.cookies, callback=self.parse_dir_contents)     

    def parse_dir_contents(self, response):
        with open('after', 'ab') as f:
            f.write(str(self.count))
            self.count+=1
            f.write('\r\n')
#            f.write(response.body)    
        
        for sel in response.xpath('//body/div[@class="dw_wp"]/div[@class="dw_table"]/div[@class="el"]'):
            temp = sel.xpath('p/span/a')
            item = QcwyItem()
            item['title'] = temp.xpath('@title').extract()[0]
            link = temp.xpath('@href').extract()[0]
            with open('text', 'wb') as f:
                f.write('start\r\n')           
            has_excel = []
            yield scrapy.Request(link, callback=self.parse_details, meta={'has_excel':has_excel})
            with open('link', 'ab') as f:
                f.write(link+'\r\n')

            
            item['link'] = link
            item['company'] = sel.xpath('span[@class="t2"]/a/text()').extract()[0]
            item['location'] = sel.xpath('span[@class="t3"]/text()').extract()[0]
            if sel.xpath('span[@class="t4"]/text()').extract():
                item['salary'] = sel.xpath('span[@class="t4"]/text()').extract()[0]
            else:
                item['salary'] = None
            item['updatetime'] = sel.xpath('span[@class="t5"]/text()').extract()[0]
            item['has_excel'] = 1 if has_excel else 0
            

            yield item
#        next_page = response.xpath('//body/div[@class="dw_wp"]/div[@class="dw_page"]/div/div/div/ul/li[last()]/a/@href')
#        if next_page:
#            url = response.urljoin(next_page[0].extract())
#            yield scrapy.Request(url, cookies=self.cookies, callback=self.parse_dir_contents)
            
    
    def parse_details(self, response):
        with open('text', 'ab') as f:
            f.write('OK\r\n')
#        item = response.meta['item']
        desc = response.xpath('/html/body/div[@class="tCompanyPage"]/div[2]/div[3]/div[4]/div/text()').extract()
        excel = re.compile('excel', re.I)
        has_excel = response.meta['has_excel']
        for line in desc:
            if excel.search(line):
                has_excel.append(True)
                with open('text', 'ab') as f:
                    f.write(line+'\r\n')
#        item['has_excel'] = 1 if has_excel else 0
