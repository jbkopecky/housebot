# -*- coding: utf-8 -*-
import unicodedata
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.exceptions import DropItem
import sqlite3
import os.path as path
import arrow
import re

from settings import DATABASE
from settings import TIME_SCALE

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
                '\r': '',
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
                        if isinstance(item[f][k], unicode):
                            item[f][k] = self.to_ascii(item[f][k])
                        item[f][k] = self.clean_it(item[f][k])
        return item

    def clean_it(self, field):
        strip_d = self.to_clean
        for i in strip_d.keys():
            field = re.sub(i, strip_d[i], field)
        return field

    def to_ascii(self, field):
        return unicodedata.normalize('NFKD', field).encode('ascii','ignore')


class PriceToDBDropDuplicate(object):
    filename = DATABASE
    time_scale = TIME_SCALE

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

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

    def process_item(self, item, domain):
        now = arrow.now()
        result = self.conn.execute('SELECT date_seen from prix where ID=?',
                (item['ID'],)
                )
        dates_seen = [x[0] for x in result]
        if len(dates_seen) > 0:
            last_seen = max(dates_seen)
            time_limit = now.replace(**self.time_scale).timestamp
            if last_seen < time_limit:
                self.insert_item(item, now.timestamp)
            raise DropItem("Already seen %s, %s" % (item['url'], arrow.get(last_seen).humanize()))
        else:
            self.insert_item(item, now.timestamp)
            return item

    def insert_item(self, item, timestamp):
        try:
            self.conn.execute('insert into prix values(?,?,?)',
                                (item['ID'], timestamp, item['prix'])
                                )
        except:
            print 'Failed to insert item: ' + item['ID']

    def create_table(self, filename):
        conn = sqlite3.connect(filename)
        conn.execute("""create table prix
                     (ID text, date_seen int, prix text, CONSTRAINT prix_id PRIMARY KEY (ID, date_seen))""")
        conn.commit()
        return conn


class ToMainTable(object):
    filename = DATABASE

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, domain):
        try:
            # ID url title arrondissement prix
            self.conn.execute('insert into annonce values(?,?,?,?)',
                             (item['ID'], item['url'], item['title'], item['arrondissement'], item['agency_name'], item['agency_phone'])
                             )
        except:
            print 'Failed to insert item: ' + item['ID']
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
                     (ID text primary key, url text, title text, arrondissement text, agency_name text, agency_phone text)""")
        conn.commit()
        return conn

