# -*- coding: utf-8 -*-

"""
爬虫的Item结构
"""

from scrapy.item import Item, Field

from settings import SKILLS


class QcwyItem(Item):
    #定义要抓取信息的Item结构
    title = Field()   #职位名称
    link = Field()   #详情链接
    location = Field()   #地址
    company = Field()   #公司名称   
    updatetime = Field()   #更新时间
    salary = Field()   #薪水
    #技能
    for skill in SKILLS.keys():
       locals()[skill] = Field()
    

