import scrapy


class ShopItem(scrapy.Item):
    name = scrapy.Field()  # 店名
    reviews = scrapy.Field()  # レビュー数
    point = scrapy.Field()  # 5点評価
    postal_code = scrapy.Field()  # 郵便番号
    address = scrapy.Field()  # 住所
    url = scrapy.Field()  # 店舗URL
    detail_url = scrapy.Field()  # 店舗詳細URL
    latitude = scrapy.Field()  # 緯度
    longitude = scrapy.Field()  # 経度
