import pandas as pd
import webbrowser

FILE_PATH1 = './data/shop_master.csv'
FILE_PATH2 = './tmp/shop_master.csv'

df1 = pd.read_csv(FILE_PATH1, index_col='id')
df2 = pd.read_csv(FILE_PATH2, index_col="id")

print(len(df1), len(df2))

diff_df = df1[~df1['url'].isin(df2['url'])]

for i, url in diff_df['url'].iteritems():
    webbrowser.open(url)
