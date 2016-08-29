# -*- coding: utf-8 -*-


BOT_NAME = 'housebot'

SPIDER_MODULES = ['housebot.spiders']
NEWSPIDER_MODULE = 'housebot.spiders'

DATABASE = './data/raw_data.db'

# The crawler will update price if it has seen this article before the time
# defined below. TIME_SCALE is an 'arrow' library 'replace' method kwarg
# >>> arrow.now().replace(**TIME_SCALE)
TIME_SCALE = {'hours': -6}

ITEM_PIPELINES = {
        # 'housebot.pipelines.Debug': 100,
        'housebot.pipelines.CleanText' : 100,
        'housebot.pipelines.PriceToDBDropDuplicate': 200,
        'housebot.pipelines.ToMainTable': 300,
        }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
    'housebot.comm.rotate_useragent.RotateUserAgentMiddleware' : 400
    }

DOWNLOAD_DELAY = 5.

CONCURRENT_ITEMS = 1
CONCURRENT_REQUESTS = 1
