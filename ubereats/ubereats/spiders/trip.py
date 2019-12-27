import scrapy

from time import sleep
from pit import Pit

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from ..constants.trip import BASE_DOMAIN, BASE_URL, WEEKLY_EARNINGS_BASE_URL


class TripSpider(scrapy.Spider):
    name = 'trip'
    allowed_domains = [BASE_DOMAIN]

    year = 2019
    month = 12
    day = 26

    DAILY_EARNINGS_URL = WEEKLY_EARNINGS_BASE_URL + "/" + str(
        year) + "/" + str(month) + "/" + str(day)  # noqa

    start_urls = [DAILY_EARNINGS_URL]

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

        # Login
        self.driver.get(response.url)

        # reCaptureが動いたときは手動で突破する
        # sleep(30)
        # reCaptureが動かないときは自動で
        pit = Pit.get("uber_auth")
        self.driver.find_element_by_id("useridInput").send_keys(pit['userId'])
        self.driver.find_elements_by_class_name("btn")[0].click()
        sleep(1)
        self.driver.find_element_by_id("password").send_keys(pit['password'])
        self.driver.find_elements_by_class_name("btn")[0].click()
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tbody")))

        res = response.replace(body=self.driver.page_source)
        shop_hrefs = res.xpath("//a/@href").re('(/p3/payments/trips/.*)')

        refs_set = set()
        for href in shop_hrefs:
            refs_set.add(BASE_URL + href.strip("?showBackLink=1"))

        for refs in refs_set:
            # yield scrapy.Request(full_url, callback=self.parse_shop)
            print(refs)
