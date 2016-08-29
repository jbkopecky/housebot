# -*- coding: utf-8 -*-
import unicodedata
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.exceptions import DropItem
import sqlite3
import os.path as path
import arrow
import logging
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
                            item[f][k] = self.remove_useless_spaces(item[f][k])
                        item[f][k] = self.clean_it(item[f][k])
        return item

    def clean_it(self, field):
        strip_d = self.to_clean
        for i in strip_d.keys():
            field = re.sub(i, strip_d[i], field)
        return field

    def to_ascii(self, field):
        return unicodedata.normalize('NFKD', field).encode('ascii','ignore')

    def remove_useless_spaces(self, field):
        field = field.replace("  ", "")
        field = field[1:] if field[0] == " " else field
        field = field[:-1] if field[-1] == " " else field
        return field


class TokenizeTags(object):
    def process_item(self, item, domain):
        tags = {}
        for t in item['property_list']:
            ints = re.findall(r"[^\s][-+]?\d*\.\d+|\d+\s", t)
            if len(ints) > 1:
                logging.error('Too Many Numbers to deal with : %s, %s' % (t,ints))
                tags[t] = 0
            elif len(ints) == 0:
                tags[t] = 0
            else: 
                integer = ints[0]
                tags[t.replace(integer, '[xx]')] = integer
        item['property_list'] = tags
        return item


class ToSqliteDB(object):
    filename = DATABASE
    time_scale = TIME_SCALE

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, domain):
        now = arrow.now()
        seen = self.check_seen_before(item)
        if len(seen) > 0:
            last_seen = max(dates_seen)
            time_limit = now.replace(**self.time_scale).timestamp
            if last_seen < time_limit:
                self.insert_item_price(item, now.timestamp)
            raise DropItem("Already seen %s, %s" % (item['url'], arrow.get(last_seen).humanize()))
        else:
            self.insert_item_price(item, now.timestamp)
            self.insert_item_main(item)
            self.insert_item_tag_list(item)
            self.insert_item_description(item)
            return item

    def check_seen_before(self, item):
        result = self.conn.execute('SELECT date_seen from prix where ID=?',
                (item['ID'],)
                )
        dates_seen = [x[0] for x in result]
        return dates_seen

    def insert_item_price(self, item, timestamp):
        try:
            self.conn.execute('insert into prix values(?,?,?)',
                                (item['ID'], timestamp, item['prix'])
                                )
        except:
            print 'Failed to insert item price: ' + item['ID']

    def insert_item_main(self, item):
        try:
            self.conn.execute('insert into annonce values(?,?,?,?,?,?)',
                             (item['ID'], item['url'], item['title'], item['arrondissement'], item['agency_name'], item['agency_phone'])
                             )
        except:
            print 'Failed to insert item main: ' + item['ID']

    def insert_item_single_tag(self, item_id, tag, tag_value):
        try:
            self.conn.execute('insert into tags values(?,?,?)',
                             (item_id, tag, tag_value)
                             )
        except:
            print 'Failed to insert item tag: ' + item_id + ": " + tag

    def insert_item_tag_list(self, item):
        tags = item['property_list']
        for t in tags:
            if not (t == " " or t == ""):
                self.insert_item_single_tag(item['ID'], t, tags[t])

    def insert_item_description(self, item):
        try:
            self.conn.execute('insert into description values(?,?)',
                             (item['ID'], item['full_description'])
                             )
        except:
            print 'Failed to insert item tag: ' + item_id + ": " + tag

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
        conn = sqlite3.connect(filename) if self.conn is None else self.conn
        conn.execute("""create table prix
                        (ID text, date_seen int, prix text, CONSTRAINT prix_id PRIMARY KEY (ID, date_seen))""")
        conn.execute("""create table annonce
                     (ID text primary key, url text, title text, arrondissement text, agency_name text, agency_phone text)""")
        conn.execute("""create table tags
                     (ID text , tag text, tag_value text, constraint tags_id primary key (ID, tag))""")
        conn.execute("""create table description
                     (ID text primary key, description text)""")
        conn.commit()
        return conn

