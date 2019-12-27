import scrapy
import re
import time

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from ..items.shop import ShopItem
from ..constants.shop import MUSASHINAKAHARA_SHOP_URL, BASE_DOMAIN, BASE_URL  # noqa
from ..constants.shop import MUSASHINAKAHARA_SEARCH_NAKAHARA_URL, MUSASHINAKAHARA_SEARCH_KOSUGI_URL, MUSASHINAKAHARA_SEARCH_SHINJO_URL  # noqa


class ShopSpider(scrapy.Spider):
    name = 'shop'
    allowed_domains = [BASE_DOMAIN]

    start_urls = [MUSASHINAKAHARA_SHOP_URL]

    # start_urls = [
    #     MUSASHINAKAHARA_SEARCH_KOSUGI_URL,
    #     MUSASHINAKAHARA_SEARCH_NAKAHARA_URL,
    #     MUSASHINAKAHARA_SEARCH_SHINJO_URL
    # ]
    # start_urls = [MUSASHINAKAHARA_SEARCH_KOSUGI_URL]

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

        self.driver.get(response.url)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article.af")))

        pre_loaded_count = 0

        res = response.replace(body=self.driver.page_source)
        shop_hrefs = res.xpath("//a/@href").re('(/ja-JP/.*/food-delivery/.*)')
        loaded_count = len(shop_hrefs)

        while loaded_count > pre_loaded_count:
            print("preloaded count:" + str(pre_loaded_count) +
                  "/loaded count:" + str(loaded_count))

            for href in shop_hrefs[pre_loaded_count:]:
                full_url = BASE_URL + href

                yield scrapy.Request(full_url, callback=self.parse_shop)

            # ブラウザ有効のときはこれをコメントアウトすると下にスクロールする。
            # headlessのときはエラーするので注意
            # self.driver.execute_script(
            #     "window.scrollTo(0, document.body.scrollHeight);")

            buttons = self.driver.find_elements_by_xpath(
                "//button[contains(text(), 'さらに表示')]")

            for button in buttons:
                button.click()

            time.sleep(5)

            pre_loaded_count = loaded_count

            res = response.replace(body=self.driver.page_source)
            shop_hrefs = res.xpath("//a/@href").re(
                '(/ja-JP/.*/food-delivery/.*)')
            loaded_count = len(shop_hrefs)

    def parse_shop(self, response):

        shop = ShopItem()

        shop["name"] = response.css("h1::text").get().strip()
        point = response.css("span::text")[0].get().strip()

        if point != '•':
            shop["point"] = float(point)
            shop["reviews"] = int(
                response.css("span::text")[2].get().strip().strip("(").strip(
                    ")").strip("+"))

        address_info = response.css("p::text")[-1].get().strip()
        postal_code_pattern = "[0-9]{3}-?[0-9]{4}"

        postal_code = re.findall(postal_code_pattern, address_info)
        if len(postal_code) != 0:
            shop["postal_code"] = postal_code[0]

        shop["address"] = re.sub(postal_code_pattern, "",
                                 address_info).replace(",", "").strip()

        shop["url"] = response.url.strip().split("?promo=")[0]
        shop["id"] = shop["url"].split("/")[-2]
        detail_url = BASE_URL + response.xpath("//p/a/@href").get()

        request = scrapy.Request(detail_url, callback=self.parse_shop_detail)
        request.meta['shop'] = shop
        yield request

    def parse_shop_detail(self, response):
        shop = response.meta['shop']

        for _ in range(3):  # 最大3回実行
            try:
                self.driver.get(response.url)
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//figure/img")))
                res = response.replace(body=self.driver.page_source)
            except TimeoutException:
                pass
            else:
                break  # 失敗しなかった時はループを抜ける
        else:
            raise (TimeoutException())  # リトライが全部失敗した時の処理

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
