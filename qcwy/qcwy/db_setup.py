# -*- coding: utf-8 -*-
"""
Created on Sat May 14 16:01:52 2016

@author: Administrator
"""
from sqlalchemy import Column, Integer, String, Date, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *

from settings import DATABASE, SKILLS


Base = declarative_base()


class Jobs(Base):
    __tablename__ = DATABASE['table']
    job_id = Column(Integer, primary_key=True)
    title = Column(String(30))
    link = Column(String(80))
    location = Column(String(20))
    salary = Column(Integer)
    updatetime = Column(Date)
    for skill in SKILLS.keys():
       locals()[skill] = Column(SmallInteger)
    
    
def create_jobs_table(engine):
    Base.metadata.create_all(engine)

