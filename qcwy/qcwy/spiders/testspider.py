# -*- coding: utf-8 -*-
"""
Created on Fri May 06 15:01:21 2016

@author: Administrator
"""

import logging
import scrapy
import urllib
import codecs

from scrapy.utils.response import open_in_browser

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
           "workyear" : "99"        #99表示所有，01无经验，02一到三年，03三到五年，04五到十年
            }
#把字符串编码成符合url规范的编码
keywordcode = urllib.urlencode(keyword)

class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ["51job.com"]
    start_urls = [
        "http://jobs.51job.com/shanghai-pdxq/54740360.html?s=1",
    ]
    def parse(self, response):
        with open('test', 'wb') as f:
            f.write('start\r\n')
        desc = response.xpath('/html/body/div[@class="tCompanyPage"]/div[2]/div[3]/div[4]/div/text()').extract()
        for sel in desc:
#            i=sel.xpath('text()').extract()
#            for j in i:
#                with open('test', 'ab') as f:
#                    f.write(j+'\r\n')
            with open ('test', 'ab') as f:
                if sel:
                    f.write(sel+'1\r\n')
            
