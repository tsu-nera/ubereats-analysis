# -*- coding: utf-8 -*-
import scrapy
from ..items import ShopItem


class PlaygroundSpider(scrapy.Spider):
    name = 'playground'
    allowed_domains = ['www.ubereats.com']
    start_urls = ['https://www.ubereats.com/ja-JP/']

    def parse(self, response):
        shop = ShopItem()
        shop["name"] = response.css('a.b4.b5.bq.b7::text').extract()

        yield shop
