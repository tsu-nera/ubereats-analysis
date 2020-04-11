# -*- coding: utf-8 -*-

import pandas as pd

MASTER_FILE_PATH = './data/shop_master.csv'
GOOGLEMAP_FILE_PATH = './data/googlemap.csv'

dir_path = "./rawdata/shops/"

file_name = "shop.csv"
TARGET_FILE_PATH = dir_path + file_name

master = pd.read_csv(MASTER_FILE_PATH, index_col='id')
df = pd.read_csv(TARGET_FILE_PATH, index_col="id")

data = pd.concat([master, df], sort=False).drop_duplicates(subset="url",
                                                           keep="last")

# master
data.to_csv(MASTER_FILE_PATH, index=True, mode="w")

# googlemap
googlemap = pd.DataFrame()
googlemap["店名"] = data["name"]
googlemap["住所"] = data["address"]
googlemap["緯度"] = data["latitude"]
googlemap["経度"] = data["longitude"]
# googlemap["開始"] = data["open_hour"]
# googlemap["終了"] = data["close_hour"]
googlemap["点数"] = data["point"]
googlemap["レビュー数"] = data["reviews"]
googlemap["URL"] = data["url"]

googlemap.to_csv(GOOGLEMAP_FILE_PATH, index=False, mode="w")
