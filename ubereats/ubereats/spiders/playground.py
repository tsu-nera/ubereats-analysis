# -*- coding: utf-8 -*-
import scrapy
from ..items import ShopItem


class PlaygroundSpider(scrapy.Spider):
    name = 'playground'
    allowed_domains = ['www.ubereats.com']
    start_urls = ['https://www.ubereats.com/ja-JP/kawasaki/']

    def parse(self, response):
        shop = ShopItem()
        shop["name"] = response.css("article div::text")[1].extract()

        yield shop
