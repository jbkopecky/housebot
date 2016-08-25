# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import unicodedata
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import sqlite3
import re

from settings import DATABASE

class Debug(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        print "id: ", item['seloger_id']


class CleanText(object):
    def __init__(self):
        self.to_clean = {
                '\xa0': '0',
                '\xe9': 'e',
                '\xb2': '2',
                '\,': '.',
                '\n': '',
                '\t': '',
                '  ': ' ',
                }

    def process_item(self, item, spider):
        # remove special chars
        for f in item.fields:
            if f in item:
                if isinstance(item[f], str):
                    item[f] = self.clean_it(item[f])
                elif isinstance(item[f], unicode):
                    item[f] = self.to_ascii(item[f])
                    item[f] = self.clean_it(item[f])
                elif isinstance(item[f], list):
                    for k in range(0, len(item[f])):
                        item[f][k] = self.clean_it(item[f][k])
        return item

    def clean_it(self, field):
        strip_d = self.to_clean
        for i in strip_d.keys():
            field = re.sub(i, strip_d[i], field)
        return field

    def to_ascii(self, field):
        return unicodedata.normalize('NFKD', field).encode('ascii','ignore')


class SQLiteStorePipeline(object):
    filename = DATABASE

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, domain):
        try:
            self.conn.execute('insert into blog values(?,?,?)',
                              (item['url'], item['raw'], unicode(domain)))
        except:
            print 'Failed to insert item: ' + item['url']
        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = self.create_table(self.filename)

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_table(self, filename):
        conn = sqlite3.connect(filename)
        conn.execute("""create table annonce
                     (url text primary key, raw text, domain text)""")
        conn.commit()
        return conn
