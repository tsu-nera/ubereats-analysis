import scrapy

from time import sleep
from pit import Pit

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from ..items.trip import TripItem
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
            refs_set.add(BASE_URL + href)

        for ref in refs_set:
            self.driver.get(ref)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img.af")))
            res = response.replace(body=self.driver.page_source)

            trip = TripItem()

            trip["id"] = ref.split("/")[-1]
            trip["year"] = self.year
            trip["date"] = "{}/{}".format(self.month, self.day)
            trip["month"] = self.month
            trip["day"] = self.day
            trip["day_of_week"] = res.css(
                "div>div>div>div>div>div>div>div>div>div>div>div>div>div::text"
            ).extract()[2].split(",")[0]

            drive_time_minutes = int(
                res.css("h4::text").extract()[0].split("分")[0])
            drive_time_seconds = int(
                res.css("h4::text").extract()[0].split("分")[1].strip(
                    "秒").strip())  # noqa
            trip["drive_time"] = drive_time_minutes + drive_time_seconds / 60
            trip["distance"] = float(
                res.css("h4::text").extract()[1].strip("km").strip())

            drive_info = res.css(
                "div>div>div>div>div>div>div>div>div>div>div>div>div>div>div>div>div>div>div::text"
            ).extract()

            trip["pickup_time"] = drive_info[0].split(
                ":")[0] + ":" + drive_info[0].split(":")[1]
            trip["pickup_address"] = drive_info[1]
            trip["drop_time"] = drive_info[2].split(
                ":")[0] + ":" + drive_info[2].split(":")[1]
            trip["drop_address"] = drive_info[3]

            trip["price"] = res.css(
                "div>div>div>div>div>div>div>div>div>div>div>div>div>div>div>div::text"
            ).extract()[2].strip("￥")

            img_url = res.css("img")[1].xpath("@src").extract()[0]
            pickup_info = img_url.split("pickup.png%7Cscale%3A2%7C")[1].split(
                "&path=color")[0].split("%2C")
            trip["pickup_latitude"] = pickup_info[0]
            trip["pickup_logitude"] = pickup_info[1]
            drop_info = img_url.split("dropoff.png%7Cscale%3A2%7C")[1].split(
                "&path=color")[0].split("%2C")
            trip["drop_latitude"] = drop_info[0]
            trip["drop_logitude"] = drop_info[1]

            yield trip

    def closed(self, reason):
        self.driver.close()
