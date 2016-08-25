# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HousebotItem(scrapy.Item):
    ID = scrapy.Field()

    seloger_id = scrapy.Field()
    link_to_annonce = scrapy.Field()

    title = scrapy.Field()
    arrondissement = scrapy.Field()
    prix = scrapy.Field()

    description = scrapy.Field()
    property_list = scrapy.Field()

    agency_name = scrapy.Field()
    agency_phone = scrapy.Field()

    full_description = scrapy.Field()
