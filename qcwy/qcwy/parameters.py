# -*- coding: utf-8 -*-
"""
Created on Thu May 12 11:35:31 2016

@author: Dante

搜索参数
"""
import collections
import urllib

#同一属性两个条件联合用,分隔
keyword = {
           'jobarea': '020000,030200,010000,040000,080200,00',   #北上广深杭
           'industrytype': '00',   #32表示互联网，42银行，03证券/金融，43保险, 00全体
           'keyword': '数据分析',
           'workyear': '99',        #99表示所有，01无经验，02一到三年，03三到五年，04五到十年
            }
#把字符串编码成符合url规范的编码
keywordcode = urllib.urlencode(keyword)

#所需要的搜索的技能表，key为技能名，value为对应正则表达式
skills = {
        'has_excel': 'excel',
        'has_mining': u'数据挖掘',
        'has_python': 'python',
        'has_hadoop': 'Hadoop',
        'has_hive': 'HIVE',
        'has_sql': 'SQL',
        'has_sas': 'SAS',
        'has_spss': 'SPSS',
        'has_java': 'java',
        'has_GA': 'Google Analytics|GA',
        'has_crawler': u'爬虫',
        'has_ETL': u'数据仓库|ETL',
        'has_R': u'R语言|(([\u4e00-\u9fa5]|\uff0c|\u3001|/|\\\\)R([\u4e00-\u9fa5]|\uff0c|\u3001|/|\\\\))',
        'has_mlearning': u'机械学习|scikit',
        'has_modeling': u'建模|数学模型',
        'has_algorithm': u'算法',
        'has_visialize': u'可视化|tableau'
        }
 
#输入你的登录名与密码 
formdata = {'username': 'yiqiyu33@hotmail.com', 'userpwd': 'D4a677,OP20'}