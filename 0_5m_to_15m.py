import pandas as pd
import os
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# =====读入数据(首次使用)
symbol = 'BTCUSDT'
if os.name == 'nt':
    df = pd.read_hdf('D:\\PythonProjects\\coin_data\\binance_%s_5m.h5'%symbol, key='%s_5m'%symbol)
elif os.name == 'posix':
    df = pd.read_hdf('/Volumes/USB-DISK/PythonProjects/coin_data/binance_%s_5m.h5'%symbol, key='%s_5m'%symbol)
else:
    print('操作系统不支持')
    exit()
    
# 任何原始数据读入都进行一下排序、去重，以防万一
df.sort_values(by=['candle_begin_time'], inplace=True)
df.drop_duplicates(subset=['candle_begin_time'], inplace=True)
df.reset_index(inplace=True, drop=True)

# =====转换为其他分钟数据
rule_type = '30T'
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
    path = 'D:\\PythonProjects\\coin_data\\binance_%s_%s.h5' % (symbol, rule_type)
    df.to_hdf(path, key='%s_%s'% (symbol, rule_type), mode='a')
    print('转换成功, 转换为%s'%path)
elif os.name == 'posix':
    path = '/Volumes/USB-DISK/PythonProjects/coin_data/binance_%s_%s.h5' % (symbol, rule_type)
    df.to_hdf(path, key='%s_%s'% (symbol, rule_type))
    print('转换成功, 转换为%s'%path)
else:
    print('操作系统不支持')
    exit()

