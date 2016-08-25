# -*- coding: utf-8 -*-

# Scrapy settings for housebot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'housebot'

SPIDER_MODULES = ['housebot.spiders']
NEWSPIDER_MODULE = 'housebot.spiders'

DATABASE = './data/raw_data.db'

ITEM_PIPELINES = {
        # 'housebot.pipelines.Debug': 100,
        'housebot.pipelines.CleanText' : 400,
        'housebot.pipelines.SQLiteStorePipeline': 500,
        }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 (My name is Bot, HouseBot)'
# USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
    'housebot.comm.rotate_useragent.RotateUserAgentMiddleware' : 400
    }

DOWNLOAD_DELAY = 5.

CONCURRENT_ITEMS = 1
CONCURRENT_REQUESTS = 1
