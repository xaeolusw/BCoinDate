import pandas as pd
import os
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# =====读入数据(首次使用)
# symbol = 'BTCUSDT'
if os.name == 'nt':
    df = pd.read_hdf(r'D:\\PythonProjects\\BCoinDate\\data\\binance_BTCUSDT_5m.h5', key='BTCUSDT_5m')
elif os.name == 'posix':
    df = pd.read_hdf(r'/Volumes/USB-DISK/PythonProjects/coin_data/binance_BTCUSDT_5m.h5', key='BTCUSDT_5m')
else:
    print('操作系统不支持')
    exit()
    

# 任何原始数据读入都进行一下排序、去重，以防万一
df.sort_values(by=['candle_begin_time'], inplace=True)
df.drop_duplicates(subset=['candle_begin_time'], inplace=True)
df.reset_index(inplace=True, drop=True)


# =====转换为其他分钟数据
rule_type = '15T'
period_df = df.resample(rule=rule_type, on='candle_begin_time', label='left', closed='left').agg(
    {'open': 'first',
     'high': 'max',
     'low': 'min',
     'close': 'last',
     'volume': 'sum',
     'quote_asset_volume': 'sum',
     })
period_df.dropna(subset=['open'], inplace=True)  # 去除一天都没有交易的周期
period_df = period_df[period_df['volume'] > 0]  # 去除成交量为0的交易周期
period_df.reset_index(inplace=True)
df = period_df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume', 'quote_asset_volume']]
# df = df[df['candle_begin_time'] >= pd.to_datetime('2017-01-01')]
df.reset_index(inplace=True, drop=True)


if os.name == 'nt':
    df.to_hdf(r'D:\\PythonProjects\\BCoinDate\\data\\binance_BTCUSDT_5m.h5', key='BTCUSDT_15m', mode='a')
elif os.name == 'posix':
    df.to_hdf(r'/Volumes/USB-DISK/PythonProjects/coin_data/binance_BTCUSDT_15m.h5', key='BTCUSDT_15m')
else:
    print('操作系统不支持')
    exit()

