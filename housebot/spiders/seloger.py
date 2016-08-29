# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy import Request
from housebot.items import HousebotItem
import logging
import itertools as it


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


def make_to_scrape_url_list(base_url, options):
    option_list = combine_options(options)
    urls = [base_url + options_dict_to_options_string(opts) for opts in option_list]
    return urls


class SelogerSpider(Spider):
    name = "seloger"
    allowed_domains = ["housebot.com"]
    base_url = 'http://www.seloger.com/list.htm'
    arr = ['7501%02i' % x for x in range(1,20)]
    # arr = [750112]
    options = {
            'idtt':           [2],
            'idtypebien':     [1],
            'tri':            ['d_dt_crea'],
            'LISTING-LISTpg': range(1,100),
            # 'LISTING-LISTpg': [1],
            'ci':             arr,
                }
    start_urls = make_to_scrape_url_list(base_url, options)

    def parse(self, response):
        for sel in response.xpath('//article'):
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
            if domain == "www.seloger.com":
                yield Request(url, callback=self.parse_seloger, meta={'item':item}, dont_filter=True)
            elif domain == "www.bellesdemeures.com":
                yield Request(url, callback=self.parse_bellesdemeures, meta={'item':item}, dont_filter=True)

    def parse_seloger(self, response):
        item = response.meta['item']
        if 'Location' in response.headers.keys():
            if 'expiree' in response.headers['Location']:
                logging.info("%s has expired, skipping..." % item['url'])
                return
        desc = response.xpath('//*[@id="detail"]/p[@class="description"]/text()').extract()
        item['full_description'] = desc[0]
        item['property_list'] = response.xpath('//*[@id="detail"]/ol/li/text()').extract()
        yield item

    def parse_bellesdemeures(self, response):
        item = response.meta['item']
        if 'Location' in response.headers.keys():
            if 'expiree' in response.headers['Location']:
                logging.info("%s has expired, skipping..." % item['url'])
                return
        item['full_description'] = response.xpath('//*[@id="detail_description"]/p[@class="descriptif "]/text()').extract()[0]
        item['property_list'] = response.xpath('//*[@id="detail_criteres"]/ul/li/text()').extract()
        yield item

