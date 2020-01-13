import scrapy


class TripItem(scrapy.Item):
    id = scrapy.Field()  # 乗車ID
    date = scrapy.Field()  # 日時
    year = scrapy.Field()  # 年
    month = scrapy.Field()  # 月
    day = scrapy.Field()  # 日
    day_of_week = scrapy.Field()  # 曜日
    drive_time = scrapy.Field()  # 時間(分)
    distance = scrapy.Field()  # 距離(km)
    pickup_time = scrapy.Field()  # ピックアップ時刻
    pickup_address = scrapy.Field()  # ピックアップ住所
    pickup_latitude = scrapy.Field()  # ピックアップ緯度
    pickup_longitude = scrapy.Field()  # ピックアップ経度
    drop_time = scrapy.Field()  # 到着時刻
    drop_address = scrapy.Field()  # 到着住所
    drop_latitude = scrapy.Field()  # ドロップ緯度
    drop_longitude = scrapy.Field()  # ドロップ経度
    price = scrapy.Field()  # 支払い額
    url = scrapy.Field()  # URL
    cash = scrapy.Field()  # 現金
    peak = scrapy.Field()  # ピーク料金
