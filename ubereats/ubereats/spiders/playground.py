# -*- coding: utf-8 -*-
import scrapy
from ..items import ShopItem

# UBEREATS_URL = "https://www.ubereats.com/ja-JP/"
UBEREATS_URL = "https://www.ubereats.com/ja-JP/feed/?pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMiVFNiVBRCVBNiVFOCU5NCVCNSVFNCVCOCVBRCVFNSU4RSU5RiVFOSVBNyU4NSUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUpkYXpMbUtMMUdHQVJHSjFYRzlJZVpWWSUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EzNS41ODA3MTQzJTJDJTIybG9uZ2l0dWRlJTIyJTNBMTM5LjY0MjEwNyU3RA%3D%3D/"


class PlaygroundSpider(scrapy.Spider):
    name = 'playground'
    allowed_domains = ['www.ubereats.com']
    start_urls = [UBEREATS_URL]

    def parse(self, response):
        shop = ShopItem()
        shop["name"] = response.css("body").extract()

        yield shop
