# -*- coding: utf-8 -*-

import scrapy


class ShopItem(scrapy.Item):
    name = scrapy.Field()
    detail_url = scrapy.Field()
    review = scrapy.Field()
