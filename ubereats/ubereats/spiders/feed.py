# -*- coding: utf-8 -*-
import scrapy
from ..items import ShopItem
from ..constants import MUSASHINAKAHARA_FEED_URL, BASE_DOMAIN  # noqa


class FeedSpider(scrapy.Spider):
    name = 'feed'
    allowed_domains = [BASE_DOMAIN]
    start_urls = [MUSASHINAKAHARA_FEED_URL]

    def parse(self, response):
        shop = ShopItem()
        shop["name"] = response.css("body").extract()

        yield shop
