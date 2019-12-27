import scrapy

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

        self.driver.get(response.url)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tbody")))

        res = response.replace(body=self.driver.page_source)
        shop_hrefs = res.xpath("//a/@href").re('(/p3/payments/trips/.*)')

        for href in shop_hrefs:
            full_url = BASE_URL + href

            # yield scrapy.Request(full_url, callback=self.parse_shop)
            print(full_url)
