# -*- coding: utf-8 -*-

import scrapy


class UbereatsItem(scrapy.Item):
    shop_name = scrapy.Field()
