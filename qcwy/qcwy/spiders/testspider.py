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
        "http://my.51job.com/my/My_SignIn.php",
    ]
    def parse(self, response):
        with open('before', 'wb') as f:
            f.write(response.body)
        jobsearch = scrapy.FormRequest.from_response(response,
                formdata={'lang': 'c', 'stype': '2', 'postchannel' : '0000', 'fromType' : '1', 'line' : '', 'confirmdate':'9', 'from':'', 'keywordtype':'2', 'keyword':'cae', 'jobarea':'010000', 'industrytype':'00','functype':'0000','x':'72', 'y':'10'},
                callback=self.after_post)
        login=scrapy.FormRequest.from_response(response,
                                               formdata={'from_domain':'www.51job.com', 'passport_loginName':'yiqiyu33@hotmail.com', 'passport_password':'D4a677,OP20'},
                                               callback=self.after_post)
        login2=scrapy.FormRequest.from_response(response,
                                               formdata={'username':'yiqiyu33@hotmail.com', 'userpwd':'D4a677,OP20'},
                                                callback=self.after_post)
        return login2
                
    def after_post(self, response):
        with open('after', 'wb') as f:
            f.write(response.body)
        url = "http://search.51job.com/list/%2B,%2B,%2B,%2B,%2B,%2B,cae,0,%2B.html?lang=c&stype=2"
        cookies={
                 'guide':'1' 
                }
        return scrapy.Request(url,cookies=cookies, callback=self.parse_dir_contents)
        
    def parse_dir_contents(self,response):
        open_in_browser(response)
