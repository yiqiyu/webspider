# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import MySQLdb
import MySQLdb.cursors
from parameters import skills


from twisted.enterprise import adbapi
from scrapy import signals

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
    def __init__(self):
        self.connpool = adbapi.ConnectionPool('MySQLdb',
            host = '127.0.0.1',
            db = 'job_project',
            user = 'root',
            passwd = 'password',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True
            )
            
    def process_item(self, item, spider):
        query = self.connpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx, item):
        if item.get('title'):
            sql = "insert into alljobs "
#            column = "('%s', '%s', '%s', '%s', '%s', '%s'" % ('salary', 'title', 'company', 'location', 'updatetime', 'link')
            param = "values ('%s', '%s', '%s', '%s', '%s', '%s'" % (item['salary'], item['title'], item['company'], item['location'], item['updatetime'], item['link'])
            for skill in skills.values():
                param += ", "+str(item[skill])
            sql += param+")"
            tx.execute(sql)

    def handle_error(self, e):
        adbapi.log.err(e)