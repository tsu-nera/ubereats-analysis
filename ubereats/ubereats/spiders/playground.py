# -*- coding: utf-8 -*-
import scrapy
from ..items import UbereatsItem


class PlaygroundSpider(scrapy.Spider):
    name = 'playground'
    allowed_domains = ['www.ubereats.com']
    start_urls = ['https://www.ubereats.com/ja-JP']

    def parse(self, response):
        pass
