# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy import Request

from housebot.items import HousebotItem
from housebot.settings import DATABASE
from housebot.settings import ARRONDISSEMENTS
from housebot.settings import SHUFFLE_URLS
from housebot.settings import N_LIST

import logging
from os import path
import sqlite3
import itertools as it
from random import shuffle


def options_dict_to_options_string(options):
    if options is None:
        return ''
    options_list = [ str(x) + "=" + str(options[x]) for x in options ]
    options_string = "&".join(options_list)
    return "?" + options_string


def combine_options(options):
    varNames = sorted(options)
    combinations = [dict(zip(varNames, prod)) for prod in it.product(*(options[varName] for varName in varNames))]
    return combinations


def make_to_scrape_url_list(base_url, options, do_shuffle=False):
    option_list = combine_options(options)
    urls = [base_url + options_dict_to_options_string(opts) for opts in option_list]
    if do_shuffle:
        shuffle(urls)
    return urls


def fetch_seen_IDs(filename):
    seen_ids = []
    if path.exists(filename):
        conn = sqlite3.connect(filename)
        result = conn.execute('SELECT ID from annonce')
        seen_ids = [x[0] for x in result]
    return seen_ids


class SelogerSpider(Spider):
    name = "seloger"
    allowed_domains = ["seloger.com", "bellesdemeures.com"]
    base_url = 'http://www.seloger.com/list.htm'
    arr = ARRONDISSEMENTS
    options = {
            'idtt':           [2],
            'idtypebien':     [1],
            'tri':            ['d_dt_crea'],
            'LISTING-LISTpg': range(1,N_LIST),
            'ci':             arr,
                }
    start_urls = make_to_scrape_url_list(base_url, options, do_shuffle=SHUFFLE_URLS)
    seen_ids = fetch_seen_IDs(DATABASE)

    def parse(self, response):
        articles = response.xpath('//article')
        if len(articles) == 0:
            logging.info("No article listing in this page %s !!!" % response.url)
        else:
            for sel in articles:
                item = HousebotItem()

                item['seloger_id'] = sel.xpath('@data-listing-id').extract()[0]
                item['ID'] = item['seloger_id']

                info = sel.xpath('.//div[contains(@class, "listing_info")]')
                url = info.xpath('.//h2/a/@href').extract()[0]

                item['url'] = url
                item['title'] = info.xpath('.//h2/a/text()').extract()[0]
                item['arrondissement'] = info.xpath('.//h2/a/span/text()').extract()[0]
                item['prix'] = info.xpath('.//a[contains(@class, "amount")]/text()').extract()[0]
                # item['description'] = ''.join(info.xpath('.//p[contains(@class, "description")]/text()').extract())

                agen = sel.xpath('.//div[contains(@class, "agency_contact")]')
                item['agency_name'] = agen.xpath('.//*[contains(@class, "agency_name")]/@data-tooltip').extract()[0]
                item['agency_phone'] = agen.xpath('.//div[contains(@class, "agency_phone")]/@data-phone').extract()[0]
                domain = url.split("/")[2]

                if item['ID'] not in self.seen_ids:
                    if domain == "www.seloger.com":
                        yield Request(
                                    url, 
                                    callback=self.parse_seloger,
                                    meta={'item':item},
                                    dont_filter=True
                                      )
                    elif domain == "www.bellesdemeures.com":
                        yield Request(
                                    url,
                                    callback=self.parse_bellesdemeures,
                                    meta={'item':item},
                                    dont_filter=True
                                      )
                    else:
                        logging.info("Dropping %s because %s is not a supported domain redirection !" % (url, domain))
                        yield
                else:
                    yield item

    def parse_seloger(self, response):
        item = response.meta['item']
        if 'Location' in response.headers.keys():
            if 'expiree' in response.headers['Location']:
                logging.info("%s has expired, skipping..." % item['url'])
                return
        desc = response.xpath('//*[@id="detail"]/p[@class="description"]/text()').extract()
        if len(desc) == 0:
            logging.error("Did not find a description for %s" % item['url'])
            return
        else:
            item['full_description'] = desc[0]
            item['property_list'] = response.xpath('//*[@id="detail"]/ol/li/text()').extract()
            yield item

    def parse_bellesdemeures(self, response):
        item = response.meta['item']
        if 'Location' in response.headers.keys():
            if 'expiree' in response.headers['Location']:
                logging.info("%s has expired, skipping..." % item['url'])
                return
        desc = response.xpath('//*[@id="detail_description"]/p[@class="descriptif "]/text()').extract()
        if len(desc) == 0:
            logging.error("Did not find a description for %s" % item['url'])
            return
        else:
            item['full_description'] = desc[0]
            item['property_list'] = response.xpath('//*[@id="detail_criteres"]/ul/li/text()').extract()
            yield item

