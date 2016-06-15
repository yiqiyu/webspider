# -*- coding: utf-8 -*-

import logging
import scrapy
import codecs
import re

from scrapy.selector import Selector

from qcwy.items import QcwyItem
from qcwy.parameters import keywordcode, skills, formdata

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


is_start_page = True
has_tested = False

def Search(kw, desc):
    """
    查找关键字的函数，输入为关键字字符串和需查找的字符串，如果存在关键字则返回1，否则0
    """
    flag = 0
    kws = re.compile(kw, re.I)
    if kws.search(desc.strip()):
        flag = 1
    return flag
    
def ContentScanner(content):
    """
    查找内容路径的函数，输入为selector对象，输出为文字内容所在的xpath路径
    """
    lines = content.extract()
    desc = []
    for line in lines:    
        pre = re.findall(u"\S+", line)
        raw = ''
        for word in pre:
            raw = raw+word
        sentence = re.sub(r'<\S+?>','', raw)
        desc.append(sentence)
    return sentence

def SalaryScanner(content):
    """
    计算平均月薪，输入为字符串，返回平均月薪
    """
    year_check = re.compile(u'年')
    day_check = re.compile(u'日')
    tt_check = re.compile(u'万')
    num = re.findall(r'\d+', content)
    aver = 0
    for i in num:
        aver += int(i)
    aver = aver/len(num)
    if year_check.search(content):
        aver /= 12
    elif day_check.search(content):
        aver = aver*30
    if tt_check.search(content):
        aver *= 10000
    if aver < 100:
        aver *= 10000
    if aver > 100000:
        aver /=12
    return aver
        

class TestfollowSpider(scrapy.Spider):
   
    name = "qcwysearch"
    allowed_domains = ["51job.com"]
    start_urls = [
        "http://my.51job.com/my/My_SignIn.php",
    ]
    count = 1
    cookies={'guide':'1' }
    def parse(self, response):
#        登录界面
        login=scrapy.FormRequest.from_response(response,
                                               formdata=formdata,
                                                callback=self.after_post)
        yield login
        
    def after_post(self, response):
#        登录界面进入后
        url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&funttype=0000&"+keywordcode
        return scrapy.Request(url,cookies=self.cookies, callback=self.parse_dir_contents)     

    def parse_dir_contents(self, response):
        """
        爬取的基本信息和翻页操作
        """
        with open('after', 'ab') as f:
            f.write(str(self.count))
            self.count+=1
            f.write('\r\n')
        
        for sel in response.xpath('//body/div[@class="dw_wp"]/div[@class="dw_table"]/div[@class="el"]'):
            temp = sel.xpath('p/span/a')
            item = {}
            item['title'] = temp.xpath('@title').extract()[0]
            link = temp.xpath('@href').extract()[0]

            
            item['link'] = link
            item['company'] = sel.xpath('span[@class="t2"]/a/text()').extract()[0]
            item['location'] = sel.xpath('span[@class="t3"]/text()').extract()[0]
            if sel.xpath('span[@class="t4"]/text()').extract():
                item['salary'] = SalaryScanner(sel.xpath('span[@class="t4"]/text()').extract()[0])
            else:
                item['salary'] = None
            item['updatetime'] = '2016-'+sel.xpath('span[@class="t5"]/text()').extract()[0]
            
            yield scrapy.Request(link, callback=self.parse_details, meta={'item':item})
            
        next_page = response.xpath('//body/div[@class="dw_wp"]/div[@class="dw_page"]/div/div/div/ul/li[last()]/a/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, cookies=self.cookies, callback=self.parse_dir_contents)
            
    
    def parse_details(self, response):
        """
        进入招聘页面爬取详细信息，并返回item
        """
        item = QcwyItem()
        basicInfo = response.meta['item']
        mainbox = response.xpath('/html/body/div[@class="tCompanyPage"]/div[2]/div[3]/div[4]/div')
        #提取详细描述
        desc = ContentScanner(mainbox)
        for key,value in skills.items():
            item[key] = Search(value, desc)
        
        for key,value in basicInfo.items():
            item[key] = value
        yield item
