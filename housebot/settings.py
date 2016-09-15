# -*- coding: utf-8 -*-

BOT_NAME = 'housebot'

SPIDER_MODULES = ['housebot.spiders']
NEWSPIDER_MODULE = 'housebot.spiders'

DATABASE = './data/raw_data.db'

# The crawler will update price if it has seen this article before the time
# defined below. TIME_SCALE is an 'arrow' library 'replace' method kwarg
# >>> arrow.now().replace(**TIME_SCALE)
TIME_SCALE = {'hours': -6}

# List Pages to scrape
ARRONDISSEMENTS = ['7501%02i' % x for x in range(1,21)]
N_LIST = 11
SHUFFLE_URLS = True

ITEM_PIPELINES = {
        # 'housebot.pipelines.Debug': 100,
        'housebot.pipelines.CleanText' : 100,
        'housebot.pipelines.TokenizeTags': 200,
        'housebot.pipelines.ToSqliteDB': 300,
        }

DOWNLOADER_MIDDLEWARES = {
    # Use these Middlewares to go through proxies defined in PROXY_LIST file:
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy_proxies.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    # Use these Middlewares to rotate UserAgents:
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
    'housebot.comm.rotate_useragent.RotateUserAgentMiddleware' : 400
    }

DOWNLOAD_DELAY = .5

# Proxy Settings:
RETRY_TIMES = 10
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
PROXY_LIST = './data/proxy/list.txt'

CONCURRENT_ITEMS = 1 # We do not parallelize pipelines because of sqlite.
# CONCURRENT_REQUESTS = 1
