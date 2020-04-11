import scrapy


class ShopItem(scrapy.Item):
    id = scrapy.Field()  # Id
    name = scrapy.Field()  # 店名
    reviews = scrapy.Field()  # レビュー数
    point = scrapy.Field()  # 評価
    postal_code = scrapy.Field()  # 郵便番号
    address = scrapy.Field()  # 住所
    url = scrapy.Field()  # 店舗URL
    latitude = scrapy.Field()  # 緯度
    longitude = scrapy.Field()  # 経度
    # open_hour = scrapy.Field()  # 開始時刻
    # close_hour = scrapy.Field()  # 終了時刻
