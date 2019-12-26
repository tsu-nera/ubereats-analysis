import scrapy

from ..constants_drive import BASE_DOMAIN, WEEKLY_EARNINGS_BASE_URL


class DriveSpider(scrapy.Spider):
    name = 'drive'
    allowed_domains = [BASE_DOMAIN]

    year = 2019
    month = 12
    day = 26

    DAILY_EARNINGS_URL = WEEKLY_EARNINGS_BASE_URL + "/" + str(
        year) + "/" + str(month) + "/" + str(day)  # noqa

    start_urls = [DAILY_EARNINGS_URL]

    def parse(self, response):
        pass
nn