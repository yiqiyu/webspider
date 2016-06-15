# -*- coding: utf-8 -*-
"""
Created on Sat May 14 16:01:52 2016

@author: Administrator
"""
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from parameters import skills, keyword
import mysql.connector

def main():



##    登录参数
#    conn = mysql.connector.connect(user='root', password='password', 
#                                   database='job_project', use_unicode=True)
#    cursor = conn.cursor()
##    表结构
#    sql = '''CREATE TABLE IF NOT EXISTS ALLJOBS
#                    (
#                    SALARY INT(6),
#                    TITLE VARCHAR(30),
#                    COMPANY VARCHAR(30),
#                    LOCATION VARCHAR(20),
#                    UPDATETIME DATE,
#                    LINK VARCHAR(80)
#                    )
#                    '''
#    cursor.execute(sql)
#                
#    for skill in skills.keys():
#        sql = 'ALTER TABLE ALLJOBS ADD COLUMN '+skill+' TINYINT(1) NOT NULL'
#        cursor.execute(sql)
#    
#    cursor.close()
#    conn.close()
#        

if __name__ == '__main__':
    main()