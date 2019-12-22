# -*- coding: utf-8 -*-
import scrapy
from ..items import ShopItem
from ..middlewares import close_driver

# UBEREATS_URL = "https://www.ubereats.com/ja-JP/"
UBEREATS_URL = "https://www.ubereats.com/ja-JP/feed/?pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMiVFNiVBRCVBNiVFOCU5NCVCNSVFNCVCOCVBRCVFNSU4RSU5RiVFOSVBNyU4NSUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUpkYXpMbUtMMUdHQVJHSjFYRzlJZVpWWSUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EzNS41ODA3MTQzJTJDJTIybG9uZ2l0dWRlJTIyJTNBMTM5LjY0MjEwNyU3RA%3D%3D/"


class PlaygroundSpider(scrapy.Spider):
    name = 'playground'
    allowed_domains = ['www.ubereats.com']

    start_urls = [UBEREATS_URL]
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "ubereats.middlewares.SeleniumMiddleware": 0,
        },
    }

    def parse(self, response):
        shop = ShopItem()
        shop["name"] = response.css("article div::text").extract()

        yield shop

    def closed(self, reason):
        close_driver
