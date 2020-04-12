import pandas as pd

MASTER_FILE_PATH = './data/shop_master.csv'
MASTER_PREMERGE_FILE_PATH = './rawdata/shops/shop_master.csv'

master = pd.read_csv(MASTER_FILE_PATH, index_col='id')
master_premerge = pd.read_csv(MASTER_PREMERGE_FILE_PATH, index_col='id')

data = pd.concat([master, master_premerge],
                 sort=False).sort_values("reviews").drop_duplicates(
                     subset="url", keep="first")

diff_df = data[~data['url'].isin(master['url'])]

for row in diff_df.iterrows():
    item = row[1]
    print(item["name"], item["url"])

# import webbrowser
# for i, url in diff_df['url'].iteritems():
#     webbrowser.open(url)
