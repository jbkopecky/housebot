# -*- coding: utf-8 -*-
import scrapy


class HousebotItem(scrapy.Item):
    ID = scrapy.Field()

    seloger_id = scrapy.Field()
    url = scrapy.Field()

    title = scrapy.Field()
    arrondissement = scrapy.Field()
    prix = scrapy.Field()

    description = scrapy.Field()
    property_list = scrapy.Field()

    agency_name = scrapy.Field()
    agency_phone = scrapy.Field()

    full_description = scrapy.Field()

