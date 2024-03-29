"""
更新时间：2021-10-08
《邢不行|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
通过获取历史K线数据，进一步讲解ccxt的用法
"""
import pandas as pd
import ccxt
import time
import os
from datetime import timedelta

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# =====设定参数
exchange = ccxt.binance()  # huobipro, binance, okex5，使用huobi需要增加limit=2000，XRP-USDT-200327

symbol = 'BTC/USDT'
time_interval = '1h'  # 其他可以尝试的值：'1m', '5m', '15m', '30m', '1H', '2H', '1D', '1W', '1M', '1Y'

# =====抓取数据开始结束时间
start_time = '2020-02-01 00:00:00'
end_time = '2021-02-02 00:00:00'
# end_time = pd.to_datetime(start_time) + timedelta(days=1)

# =====开始循环抓取数据
df_list = []
start_time_since = exchange.parse8601(start_time)
end_time_since = exchange.parse8601(end_time)
# 循环获取历史数据
all_kline_data = []
while True:
    # okex的v5接口比较特殊，另外处理
    if exchange.name == 'OKEX':
        params = {
            'instId': symbol,
            'bar': time_interval,
            'after': end_time_since,
            'limit': '100'
        }
        # 获取K线使
        kline_data = exchange.public_get_market_history_candles(params=params)['data']
        print(kline_data)
        if kline_data:
            end_time_since = kline_data[-1][0]  # 更新since，为下次循环做准备
            all_kline_data += kline_data
            if int(kline_data[-1][0]) < int(start_time_since):
                break
    else:
        df = exchange.fetch_ohlcv(symbol=symbol, timeframe=time_interval, since=start_time_since, limit=2000)

        # 整理数据
        df = pd.DataFrame(df, dtype=float)  # 将数据转换为dataframe
        df['candle_begin_time'] = pd.to_datetime(df[0], unit='ms')  # 整理时间
        print(df)

        # 合并数据
        df_list.append(df)

        # 新的since
        t = pd.to_datetime(df.iloc[-1][0], unit='ms')
        print(t)
        start_time_since = exchange.parse8601(str(t))

        # 判断是否挑出循环
        if t >= pd.to_datetime(end_time) or df.shape[0] <= 1:
            print('抓取完所需数据，或抓取至最新数据，完成抓取任务，退出循环')
            break

        # 抓取间隔需要暂停2s，防止抓取过于频繁
        time.sleep(2)

# 对数据进行整理
df = pd.concat(df_list, ignore_index=True)
df.rename(columns={0: 'MTS', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace=True)
df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms') + timedelta(hours=8)
df = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]
# 选取数据时间段
df = df[df['candle_begin_time'].dt.date == pd.to_datetime(start_time).date()]

# 去重、排序
df.drop_duplicates(subset=['candle_begin_time'], keep='last', inplace=True)
df.sort_values('candle_begin_time', inplace=True)
df.reset_index(drop=True, inplace=True)
# =====保存数据到文件
if df.shape[0] > 0:
    # 根目录，确保该路径存在
    path = '/Users/xingbuxingx/Desktop/数字货币量化课程/2020版数字货币量化投资课程/xbx_coin_2020/data/history_candle_data'

    # 创建交易所文件夹
    path = os.path.join(path, exchange.id)
    if os.path.exists(path) is False:
        os.mkdir(path)
    # 创建spot文件夹
    path = os.path.join(path, 'spot')
    if os.path.exists(path) is False:
        os.mkdir(path)
    # 创建日期文件夹
    path = os.path.join(path, str(pd.to_datetime(start_time).date()))
    if os.path.exists(path) is False:
        os.mkdir(path)

    # 拼接文件目录
    file_name = '_'.join([symbol.replace('/', '-'), time_interval]) + '.csv'
    path = os.path.join(path, file_name)
    print(path)

    df.to_csv(path, index=False)
