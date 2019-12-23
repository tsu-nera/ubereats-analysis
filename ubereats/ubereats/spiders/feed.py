import scrapy
import re

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ..items import ShopItem
from ..constants import MUSASHINAKAHARA_FEED_URL, BASE_DOMAIN, BASE_URL  # noqa


class FeedSpider(scrapy.Spider):
    name = 'feed'
    allowed_domains = [BASE_DOMAIN]
    start_urls = [MUSASHINAKAHARA_FEED_URL]

    def __init__(self):
        options = ChromeOptions()

        options.add_argument("--headless")
        options.add_argument("start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")

        self.driver = Chrome(options=options)

    def parse(self, response):
        print("Parsing...\n")

        self.driver.get(response.url)
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "article.af")))

        res = response.replace(
            body=self.driver.page_source)  # レスポンスオブジェクトのHTMLをseleniumのものと差し替える

        for href in res.xpath("//a/@href").re('(/ja-JP/.*/food-delivery/.*)'):
            full_url = BASE_URL + href

            yield scrapy.Request(full_url, callback=self.parse_shop)

        # 1つの店舗を試したいときのデバッグ用
        # href = res.xpath("//a/@href").re('(/ja-JP/.*/food-delivery/.*)')[0]
        # full_url = BASE_URL + href
        # yield scrapy.Request(full_url, callback=self.parse_shop)

    def parse_shop(self, response):

        shop = ShopItem()

        shop["name"] = response.css("h1::text").get().strip()
        point = response.css("span::text")[0].get().strip()

        if point != '•':
            shop["point"] = float(point)
            shop["reviews"] = int(
                response.css("span::text")[2].get().strip().strip("(").strip(
                    ")").strip("+"))

        address_info = response.css("p::text")[1].get().strip()
        postal_code_pattern = "[0-9]{3}-?[0-9]{4}"

        postal_code = re.findall(postal_code_pattern, address_info)
        if len(postal_code) != 0:
            shop["postal_code"] = postal_code[0]

        shop["address"] = re.sub(postal_code_pattern, "",
                                 address_info).replace(",", "")

        shop["url"] = response.url.strip()
        shop["detail_url"] = BASE_URL + response.xpath("//p/a/@href").get()

        request = scrapy.Request(shop['detail_url'],
                                 callback=self.parse_shop_detail)
        request.meta['shop'] = shop
        yield request

    def parse_shop_detail(self, response):
        shop = response.meta['shop']

        self.driver.get(response.url)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//figure/img")))
        res = response.replace(body=self.driver.page_source)

        map_url = [
            s for s in res.css("img").xpath("@src").getall()
            if "maps.googleapis.com" in s
        ][0]
        map_info = map_url.split("center=")[1].split("&zoom=")[0].split("%2C")

        shop["latitude"] = map_info[0]
        shop["longitude"] = map_info[1]

        hour_list = [
            s for s in res.css("tbody>tr>td::text").getall() if ":" in s
        ]

        shop["open_hour"] = hour_list[0]
        shop["close_hour"] = hour_list[-1]

        yield shop

    def closed(self, reason):
        self.driver.close()
