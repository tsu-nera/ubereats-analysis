# -*- coding: utf-8 -*-
import scrapy

from ..items import ShopItem
from ..constants import MUSASHINAKAHARA_FEED_URL, BASE_DOMAIN, BASE_URL  # noqa


class FeedSpider(scrapy.Spider):
    name = 'feed'
    allowed_domains = [BASE_DOMAIN]
    start_urls = [MUSASHINAKAHARA_FEED_URL]

    def parse(self, response):
        print("Parsing...\n")

        for href in response.xpath("//a/@href").re(
                '(/ja-JP/.*/food-delivery/.*)'):
            full_url = BASE_URL + href

            yield scrapy.Request(full_url, callback=self.parse_item)

    def parse_item(self, response):

        shop = ShopItem()
        shop["detail_url"] = response.url

        yield shop

        # article = response.css("article.af")[0]
        # shop["name"] = article.css("div")[6].css("div::text").extract()

        # yield shop
