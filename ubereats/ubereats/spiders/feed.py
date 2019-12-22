# -*- coding: utf-8 -*-
import scrapy
from ..items import ShopItem
from ..constants import MUSASHINAKAHARA_STATION_URL, BASE_DOMAIN


class FeedSpider(scrapy.Spider):
    name = 'feed'
    allowed_domains = [BASE_DOMAIN]
    start_urls = [MUSASHINAKAHARA_STATION_URL]

    def parse(self, response):
        shop = ShopItem()
        shop["name"] = response.css("body").extract()

        yield shop
