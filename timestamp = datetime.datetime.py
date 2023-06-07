import datetime
import pandas as pd

timestamp = pd.to_datetime(1612299600000, unit='ms')
print(timestamp)
timestamp = pd.to_datetime(1612274400000, unit='ms')
print(timestamp)

# 将 datetime 对象转换为字符串
#time_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')

# 打印时间字符串


# dt = datetime.datetime.strptime('2021-02-01 00:00:00', '%Y-%m-%d %H:%M:%S')

# # 将 datetime 对象格式化为 ISO 8601 格式的时间字符串
# iso_str = dt.isoformat() + 'Z'

# # 打印 ISO 8601 格式的时间字符串
# print(iso_str)