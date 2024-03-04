import pandas as pd

def update_csv_files():
    # Define new column names
    new_columns = [
        'open_time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_volume', 'count', 'taker_buy_volume',
        'taker_buy_quote_volume', 'ignore'
    ]

    # Loop through all months from January (01) to December (12)
    for month in range(1, 13):
        # Format the file name based on the month
        file_name = f'BTCUSDT_kline_1m/BTCUSDT-1m-2021-{month:02d}.csv'

        try:
            # Read the CSV file assuming it has no header
            df = pd.read_csv(file_name, header=None)

            # Assign new column names to the dataframe
            df.columns = new_columns

            # Save the updated dataframe to the same CSV file
            df.to_csv(file_name, index=False, header=True)
            print(f"Updated file: {file_name}")
        except FileNotFoundError:
            print(f"File not found: {file_name}")
        except Exception as e:
            print(f"An error occurred with file: {file_name}, Error: {e}")


# Call the function to update the CSV files
update_csv_files()