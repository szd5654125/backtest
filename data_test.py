import pandas as pd
import glob

csv_files = glob.glob('BTCUSDT_kline/BTCUSDT-15m-*.csv')

csv_files_sorted = sorted(csv_files)

x = 18  # 示例：只读取排序后的前2个文件

df_train = pd.DataFrame()

for file in csv_files_sorted[:x]:
    df_temp = pd.read_csv(file)
    df_train = pd.concat([df_train, df_temp], ignore_index=True)

df_train['Open Time'] = pd.to_datetime(df_train['open_time'], unit='ms')
df_train.set_index('Open Time', inplace=True)
duplicates = df_train.index[df_train.index.duplicated(keep=False)]
if duplicates.empty:
    print("No duplicates in 'open_time'. Safe to set as index.")
else:
    print("No duplicates in 'open_time'. Safe to set as index.")
    print(df_train.loc[duplicates])

df_train.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)

df_train = df_train[['Open', 'High', 'Low', 'Close', 'Volume']]
df_train = (df_train / 1e4).assign(Volume=df_train.Volume * 1e4)


