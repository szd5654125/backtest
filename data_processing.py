import pandas as pd
import glob
from datetime import datetime
import os
import numpy as np
def load_and_process_data(csv_folder_path, x):
    # use glob get all scv file
    csv_files = glob.glob(f'{csv_folder_path}/BTCUSDT-1m-*.csv')

    # sort
    csv_files_sorted = sorted(csv_files)
    df_train = pd.DataFrame()

    # use x files
    for file in csv_files_sorted[:x]:
        df_temp = pd.read_csv(file)
        df_train = pd.concat([df_train, df_temp], ignore_index=True)

    # trans timestamp to readable
    df_train['Open Time'] = pd.to_datetime(df_train['open_time'], unit='ms')
    df_train.set_index('Open Time', inplace=True)

    # filter
    df_train = df_train[['open', 'high', 'low', 'close']]

    # add index 'Open Time' in DataFrame
    df_train = df_train.reset_index()
    # trans 'Open Time' to 'year-month-day'
    df_train['Open Time'] = df_train['Open Time'].dt.strftime('%Y-%m-%d-%H-%M')
    return df_train

def merge_and_save_dataframes_to_csv(*data):
    dataframes = []
    for item in data:
        # if input is DataFrame add in list
        if isinstance(item, pd.DataFrame):
            dataframes.append(item)
        # if input is Series or numpy.ndarray trans to DataFrame
        elif isinstance(item, pd.Series) or isinstance(item, np.ndarray):
            dataframes.append(pd.DataFrame(item))
        else:
            print(f"Unsupported data type: {type(item)}")

    # merge
    merged_df = pd.concat(dataframes, axis=1)

    # reform time
    current_time = datetime.now().strftime('%Y%m%d%H%M')

    # make sure result folder exist
    os.makedirs('result', exist_ok=True)

    file_path = os.path.join('result', f'{current_time}.csv')

    merged_df.to_csv(file_path, index=False)

    print(f'Data saved to {file_path}')