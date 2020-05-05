import scrapy

from time import sleep

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from ..items.trip import TripItem
from ..constants.trip import BASE_DOMAIN, BASE_URL, WEEKLY_EARNINGS_BASE_URL

# from scrapy.utils.response import open_in_browser


class TripSpider(scrapy.Spider):
    name = 'trip'
    allowed_domains = [BASE_DOMAIN]

    def __init__(self, year=2020, month=1, day=1, *args, **kwargs):
        super(TripSpider, self).__init__(*args, **kwargs)

        self.year = year
        self.month = month
        self.day = day

        DAILY_EARNINGS_URL = self._url(year, month, day)

        self.start_urls = [DAILY_EARNINGS_URL]

        options = ChromeOptions()

        # options.add_argument("--headless")
        options.add_argument("start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")

        self.driver = Chrome(options=options)

    def _url(self, year, month, day):
        return "{0}/{1}/{2}/{3}".format(WEEKLY_EARNINGS_BASE_URL, year,
                                        month.zfill(2), day.zfill(2))

    def parse(self, response):

        # Login
        self.driver.get(response.url)

        # reCaptureが動いたときは手動で突破する
        sleep(30)

        # reCaptureが動かないときは自動で
        # pit = Pit.get("uber_auth")
        # self.driver.find_element_by_id("useridInput").send_keys(pit['userId'])
        # sleep(1)
        # self.driver.find_elements_by_class_name("btn")[0].click()
        # sleep(1)
        # self.driver.find_element_by_id("password").send_keys(pit['password'])
        # sleep(1)
        # self.driver.find_elements_by_class_name("btn")[0].click()
        # WebDriverWait(self.driver, 30).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "tbody")))

        res = response.replace(body=self.driver.page_source)
        shop_hrefs = res.xpath("//a/@href").re('(/p3/payments/trips/.*)')

        refs_set = set()
        for href in shop_hrefs:
            refs_set.add(BASE_URL + href.split("?showBackLink")[0])

        for ref in refs_set:

            for _ in range(3):  # 最大3回実行
                try:
                    self.driver.get(ref)
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "img")))
                    WebDriverWait(self.driver, 10).until(
                        EC.invisibility_of_element_located((
                            By.CSS_SELECTOR,
                            "div>div>div>div>div>div>div>div>div>div>div>div>div>div"
                        )))
                    # waitがうまくいかないな。とりあえずsleepつかった。
                    sleep(3)
                    res = response.replace(body=self.driver.page_source)
                except TimeoutException:
                    pass
                else:
                    break  # 失敗しなかった時はループを抜ける
            else:
                raise (TimeoutException())  # リトライが全部失敗した時の処理

            trip = TripItem()

            trip["id"] = ref.split("/")[-1]
            trip["year"] = self.year
            trip["date"] = "{}/{}".format(self.month, self.day)
            trip["month"] = self.month
            trip["day"] = self.day
            trip["day_of_week"] = res.css(
                "div>div>div>div>div>div>div>div>div>div>div>div>div>div::text"
            ).extract()[2].split(",")[0]

            trip["distance"] = float(
                res.css("h4::text").extract()[1].strip("km").strip())

            drive_info = res.css(
                "div>div>div>div>div>div>div>div>div>div>div>div>div>div>div>div>div>div>div::text"  # noqa
            ).extract()

            trip["pickup_time"] = drive_info[0].split(
                ":")[0] + ":" + drive_info[0].split(":")[1]
            trip["pickup_address"] = drive_info[1]

            try:
                img_url = res.css("img")[1].xpath("@src").extract()[0]
                pickup_info = img_url.split(
                    "pickup.png%7Cscale%3A2%7C")[1].split(
                        "&path=color")[0].split("&markers=")[0].split("%2C")
                trip["pickup_latitude"] = pickup_info[0]
                trip["pickup_longitude"] = pickup_info[1]
                drop_info = img_url.split(
                    "dropoff.png%7Cscale%3A2%7C")[1].split(
                        "&path=color")[0].split("%2C")
                trip["drop_latitude"] = drop_info[0]
                trip["drop_longitude"] = drop_info[1]
                trip["drop_time"] = drive_info[2].split(
                    ":")[0] + ":" + drive_info[2].split(":")[1]
                trip["drop_address"] = drive_info[3]
            except Exception:
                try:
                    img_url = res.css("img")[2].xpath("@src").extract()[0]
                    pickup_info = img_url.split(
                        "pickup.png%7Cscale%3A2%7C")[1].split(
                            "&path=color")[0].split("&markers=")[0].split(
                                "%2C")
                    trip["pickup_latitude"] = pickup_info[0]
                    trip["pickup_longitude"] = pickup_info[1]
                    drop_info = img_url.split(
                        "dropoff.png%7Cscale%3A2%7C")[1].split(
                            "&path=color")[0].split("%2C")
                    trip["drop_latitude"] = drop_info[0]
                    trip["drop_longitude"] = drop_info[1]
                    trip["drop_time"] = drive_info[2].split(
                        ":")[0] + ":" + drive_info[2].split(":")[1]
                    trip["drop_address"] = drive_info[3]
                except Exception as e:
                    # アプリで住所が空白の場合はpickup情報が取得できないので、
                    # メッセージだけ表示して無視
                    print(e)

            trip["url"] = ref

            # 支払額
            trip["price"] = int(
                res.css("h1::text").extract_first().replace("￥", "").replace(
                    ",", ""))

            # 現金対応
            try:
                trip["cash"] = int(
                    res.css(
                        'div>div>div>div>div>div>div>div>div>div>div>div>div>div>div>div::text'
                    ).extract_first().replace("-￥", "").replace(",", ""))
            except Exception:
                trip["cash"] = 0

            # ピーク
            try:
                test = res.css(
                    "div>div>div>div>div>div>div>div>div>div>div>div>div>div>span::text"
                )[2].extract()
                if '+' in test:
                    trip["peak"] = int(test.replace('+￥', "").replace(',', ""))
                else:
                    trip["peak"] = 0
            except Exception:
                trip["peak"] = 0

            if res.css("h4::text").extract()[0] != "0 秒":
                # シングル案件
                drive_time_minutes = int(
                    res.css("h4::text").extract()[0].split("分")[0])
                drive_time_seconds = int(
                    res.css("h4::text").extract()[0].split("分")[1].strip(
                        "秒").strip())  # noqa
                trip["drive_time"] = round(
                    drive_time_minutes + drive_time_seconds / 60, 1)

                yield trip
            else:
                # ダブル案件
                trip2 = trip.copy()

                trip["price"] = 0
                trip["cash"] = 0
                trip["peak"] = 0
                trip["distance"] = 0
                trip["drive_time"] = 0

                yield trip

                def time_to_num(time_str):
                    tmp = time_str.split(":")
                    return int(tmp[0]) * 60 + int(tmp[1])

                trip2["drive_time"] = time_to_num(
                    trip2["drop_time"]) - time_to_num(trip["pickup_time"])
                trip2["url"] = trip2["url"] + "/"
                yield trip2

    def closed(self, reason):
        self.driver.close()
