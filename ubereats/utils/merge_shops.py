import pandas as pd

MASTER_FILE_PATH = './data/shop_master.csv'
MASTER_PREMERGE_FILE_PATH = './rawdata/shops/shop_master.csv'
GOOGLEMAP_FILE_PATH = './data/googlemap.csv'

master = pd.read_csv(MASTER_FILE_PATH, index_col='id')
master_premerge = pd.read_csv(MASTER_PREMERGE_FILE_PATH, index_col='id')

data = pd.concat([master, master_premerge],
                 sort=False).sort_values("reviews").drop_duplicates(
                     subset="url", keep="first")

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
