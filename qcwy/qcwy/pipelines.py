# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
#import MySQLdb
#import MySQLdb.cursors
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.exc import NoSuchTableError
from scrapy.exceptions import DropItem

import db_setup

#from config import skills, database

#from twisted.enterprise import adbapi
#from scrapy import signals


class QcwyJsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('..\\qcwy\\qcwy\\qcwy.json', 'w', encoding = 'utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii = False) + "\r\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close() 


class QcwyMySQLPipeline(object):
    """docstring for MySQLPipeline"""
    def __init__(self, database):
        self.path = 'mysql://'+database['user']+':'+database['password']\
                +'@'+database['host']+'/'+database['name']+'?charset=utf8'
        self.tableName = database['table']

#        self.connpool = adbapi.ConnectionPool('MySQLdb',
#            host = '127.0.0.1',
#            db = 'job_project',
#            user = 'root',
#            passwd = 'password',
#            cursorclass = MySQLdb.cursors.DictCursor,
#            charset = 'utf8',
#            use_unicode = True
#            )

    @classmethod
    def from_crawler(cls, crawler):
        return cls(database = crawler.settings.get('DATABASE'))
    
    def open_spider(self, spider):        
        self.engine = create_engine(self.path, echo=True)
        if self.engine.has_table(self.tableName):
            self.table = Table(self.tableName, MetaData(self.engine), autoload=True)
        else:
            db_setup.create_jobs_table(self.engine)
            self.table = Jobs.__table__
#            self.table.metadata._bind_to(self.engine)
        self.Session = sessionmaker(self.engine)
#        self.session = Session()
        
#    def close_spider(self, spider):
#        self.session.close()
        
    def process_item(self, item, spider):
        if item.get('title') and item['salary'] > 100 and item['salary'] < 100000:
            session = self.Session() 
            insertHandler = self.table.insert()
            insertHandler.execute(item)
            session.commit()
            session.close()
            return item
        else:
            raise DropItem("Unexpected salary value: %s" % item['salary'])
            
#        self._conditional_insert(item)
#        query = self.connpool.runInteraction(self._conditional_insert, item)
#        query.addErrback(self.handle_error)

#    def _conditional_insert(self, tx, item):        
#        insertHandler = self.table.insert()
#        if item.get('title') and item['salary'] > 100 and item['salary'] < 100000:
#            insertHandler.execute(item)
#            self.session.commit()
#            sql = "insert into alljobs "
##            column = "('%s', '%s', '%s', '%s', '%s', '%s'" % ('salary', 'title', 'company', 'location', 'updatetime', 'link')
#            param = "values ('%s', '%s', '%s', '%s', '%s', '%s'" % (item['salary'], item['title'], item['company'], item['location'], item['updatetime'], item['link'])
#            for skill in skills.keys():
#                param += ", "+str(item[skill])
#            sql += param+")"
#            tx.execute(sql)

#    def handle_error(self, e):
#        adbapi.log.err(e)