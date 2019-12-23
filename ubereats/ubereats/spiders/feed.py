import scrapy

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

        # options.add_argument("--headless")
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

        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "article.af")))

        res = response.replace(
            body=self.driver.page_source)  # レスポンスオブジェクトのHTMLをseleniumのものと差し替える

        for href in res.xpath("//a/@href").re('(/ja-JP/.*/food-delivery/.*)'):
            full_url = BASE_URL + href

            yield scrapy.Request(full_url, callback=self.parse_item)

        self.driver.close()

    def parse_item(self, response):

        shop = ShopItem()
        shop["detail_url"] = response.url

        yield shop

        # article = response.css("article.af")[0]
        # shop["name"] = article.css("div")[6].css("div::text").extract()

        # yield shop
