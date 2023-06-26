import pandas as pd
import glob
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# 获取数据的路径
path = '/Volumes/USB-DISK/PythonProjects/coin_data/binance/spot/BTCUSDT/5m'  # 改成电脑本地的地址
path_list = glob.glob(path + "/*.csv")  # python自带的库，获得某文件夹中所有csv文件的路径

# 筛选出指定币种和指定时间
symbol = 'BTCUSDT'
path_list = list(filter(lambda x: symbol in x, path_list))

# 导入数据
df_list = []
for path in sorted(path_list):
    # print(path)
    df = pd.read_csv(path, parse_dates=['candle_begin_time'])
    df = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume', 'quote_asset_volume']]
    df['quote_asset_volume'].rename('quote_volume', inplace=True)
    df_list.append(df)
    # print(df.head(5))

# 整理完整数据
data = pd.concat(df_list, ignore_index=True)
data.sort_values(by='candle_begin_time', inplace=False)
data.reset_index(drop=False, inplace=False)

# 导出完整数据
data.to_hdf('/Volumes/USB-DISK/PythonProjects/coin_data/binance_%s.h5' % symbol, key='BTCUSDT_5m', mode='w')
print(data)

