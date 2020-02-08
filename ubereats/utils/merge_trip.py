import pandas as pd

MASTER_FILE_PATH = './data/trip_master.csv'
TARGET_FILE_PATH = "./rawdata/trips/latest_trips.csv"

master = pd.read_csv(MASTER_FILE_PATH, index_col='id')
df = pd.read_csv(TARGET_FILE_PATH, index_col="id")

data = pd.concat([master, df], sort=False).drop_duplicates(subset="url",
                                                           keep="last")

data.to_csv(MASTER_FILE_PATH, index=True, mode="w")
