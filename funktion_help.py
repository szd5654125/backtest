
# help(Strategy.buy)

from datetime import datetime

def timestamp_to_datetime(timestamp):
    timestamp_in_seconds = timestamp / 1000.0
    dt_object = datetime.fromtimestamp(timestamp_in_seconds)
    formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return formatted_date


formatted_date = timestamp_to_datetime(1609459200000)
print(formatted_date)  # 输出应为转换后的日期和时间，包括毫秒
formatted_date1 = timestamp_to_datetime(1580515200000)
print(formatted_date1)  # 输出应为转换后的日期和时间，包括毫秒