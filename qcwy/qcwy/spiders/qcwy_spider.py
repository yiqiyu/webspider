# -*- coding: utf-8 -*-

import logging
import re
import string
import sys
import urllib

from scrapy.selector import Selector
import scrapy

from qcwy.items import QcwyItem
from qcwy.settings import KEYWORD, SKILLS, FORMDATA


reload(sys)
sys.setdefaultencoding('utf-8')


#把字符串编码成符合url规范的编码
KEYWORD_CODE = urllib.urlencode(KEYWORD)

    
def HTMLCleaner(content):
    """
    HTML文本整理，输入为文字内容所在的xpath路径，输出为文字内容
    """
    lines = content.extract()
    sentence = ''
    for line in lines:
        #去掉描述中的空字符
        pre = re.findall(u"\S+", line)
        raw = string.join(pre,sep='')
        sentence += re.sub(r'<\S+?>','', raw)
    return sentence


def SalaryScanner(content):
    """
    计算平均月薪，输入为字符串，返回平均月薪
    """
    if not content:
        return None
    content = content[0]
    year_check = re.compile(u'年')
    day_check = re.compile(u'日')
    unit_check = re.compile(u'万')
    num = re.findall(r'\d+', content)
    aver = sum(map(int, num))/len(num)
    if year_check.search(content):
        aver /= 12
    elif day_check.search(content):
        aver *= 30
    if unit_check.search(content):
        aver *= 10000
    return aver
        

class TestfollowSpider(scrapy.Spider):   
    name = "qcwysearch"
    allowed_domains = ["51job.com"]
    start_urls = ["http://my.51job.com/my/My_SignIn.php"]
    cookies={'guide':'1' }
        
    def parse(self, response):
#        登录界面
        yield scrapy.FormRequest.from_response(response,
                                               formdata=FORMDATA,
                                               callback=self.after_post)
        
    def after_post(self, response):
#        登录界面进入后
        url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&funttype=0000&"+KEYWORD_CODE
        return scrapy.Request(url,cookies=self.cookies, callback=self.parse_dir_contents)     

    def parse_dir_contents(self, response):
        """
        爬取的基本信息和翻页操作
        """
        #按条目逐条爬取基本信息        
        for sel in response.xpath('//body/div[@class="dw_wp"]/div[@class="dw_table"]/div[@class="el"]'):
            basic_info = {}
            basic_info['title'] = sel.xpath('p/span/a/@title').extract()[0]
            basic_info['link'] = link = sel.xpath('p/span/a/@href').extract()[0]
            basic_info['company'] = sel.xpath('span[@class="t2"]/a/text()').extract()[0]
            basic_info['location'] = sel.xpath('span[@class="t3"]/text()').extract()[0]
            basic_info['salary'] = SalaryScanner(sel.xpath('span[@class="t4"]/text()').extract())
            basic_info['updatetime'] = '2016-'+sel.xpath('span[@class="t5"]/text()').extract()[0]         
            yield scrapy.Request(link, callback=self.parse_details, meta={'basic_info':basic_info})           
        #翻页操作
        next_page = response.xpath('//body/div[@class="dw_wp"]/div[@class="dw_page"]/div/div/div/ul/li[last()]/a/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, cookies=self.cookies, callback=self.parse_dir_contents)
            
    
    def parse_details(self, response):
        """
        进入招聘页面爬取详细信息，并返回item
        """
        item = QcwyItem()
        basic_info = response.meta['basic_info']
        mainbox = response.xpath('/html/body/div[@class="tCompanyPage"]/div[2]/div[3]/div[4]/div')
        #提取详细描述
        desc = HTMLCleaner(mainbox)
        hasSkill = lambda kw,desc: 1 if re.search(kw, desc.strip(), re.I) else 0        
        for skill,skill_desc in SKILLS.items():
            item[skill] = hasSkill(skill_desc, desc)       
        item.update(basic_info)
        yield item
