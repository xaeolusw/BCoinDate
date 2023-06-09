import pandas as pd
import ccxt
import time
import os
from datetime import timedelta, datetime

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# =====设定参数
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

binance = ccxt.binance({
    'proxies': proxies
})

def get_binance_klines(symbol, time_interval, start_time, end_time):
    start_time_since = binance.parse8601(start_time) #parse8601（），用于将 ISO 8601 格式的时间字符串转换为 Unix 时间戳
    end_time_since = binance.parse8601(end_time)

    # =====循环获取数据
    df_list = []
    all_kline_data = []

    while True:
        params = {
            'symbol': symbol,
            'interval': time_interval,
            'startTime': start_time_since, #如果未发送 startTime 和 endTime ，默认返回最近的交易。
            'endTime': end_time_since,
            'limit': 1000,
        }  

        kline_data = binance.publicGetKlines(params=params)

        df = pd.DataFrame(kline_data, dtype=float)  # 将数据转换为dataframe #缺少这两行代码
        df_list.append(df)  #缺少这两行代码
      
        if df.shape[0] > 1:
            start_time_since = kline_data[-1][0]  # 更新since，为下次循环做准备
            all_kline_data += kline_data
        else:
            break

        # 抓取间隔需要暂停2s，防止抓取过于频繁
        time.sleep(2)

    # 对数据进行整理
    df = pd.concat(df_list, ignore_index=True)

    if df.shape[0] > 0:
        df.rename(columns={0: 'MTS', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume',6:'kline_close_time',7:'quote_asset_volume',8:'number_of_trades',9:'taker_buy_base_asset_volume',10:'taker_buy_quote_asset_volume'}, inplace=True)
        df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms') 
        df = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume','kline_close_time','quote_asset_volume','number_of_trades','taker_buy_base_asset_volume','taker_buy_quote_asset_volume']]

        df_group = df.groupby(pd.to_datetime(df['candle_begin_time']).dt.date, as_index=False)
        for day, df in df_group:
            df.drop_duplicates(subset=['candle_begin_time'], keep='last', inplace=True)
            df.sort_values('candle_begin_time', inplace=True)
            df.reset_index(drop=True, inplace=True)
    
            # =====保存数据到文件
            if df.shape[0] > 0:
                # 根目录，确保该路径存在
                path = '/Volumes/USB-DISK/PythonProjects/coin_data'

                # 创建交易所文件夹
                path = os.path.join(path, binance.id)
                if os.path.exists(path) is False:
                    os.mkdir(path)
                # 创建spot文件夹
                path = os.path.join(path, 'spot')
                if os.path.exists(path) is False:
                    os.mkdir(path)
                # 创建交易对文件夹
                path = os.path.join(path, symbol)
                if os.path.exists(path) is False:
                    os.mkdir(path)
                # 创建频次文件夹
                path = os.path.join(path, time_interval)
                if os.path.exists(path) is False:
                    os.mkdir(path)

                # 拼接文件目录
                file_name = '_'.join([binance.name, symbol.replace('/', '-'), str(pd.to_datetime(day)).split(' ')[0].replace('-',''),time_interval]) + '.csv'
                path = os.path.join(path, file_name)

                print(path)
                df.to_csv(path, index=False)
   

# =====设定参数
error_list = []
symbol_list = ['BTCUSDT','ETHUSDT','EOSUSDT','LTCUSDT']  #'BTCUSDT','ETHUSDT','EOSUSDT','LTCUSDT'
time_interval_list = ['5m','15m']  # 其他可以尝试的值：'1m', '5m', '15m', '30m', '1H', '2H', '1D', '1W', '1M', '1Y'

# # =====选择开始、结束时间抓取数据
# start_time = '2023-06-10 00:00:00'
# end_time = '2023-06-10 23:59:00'

# while start_time < end_time :
#     temp_time = str(pd.to_datetime(end_time) - timedelta(days=30))

#     if temp_time > start_time :
#         for symbol in symbol_list:
#             for time_interval in time_interval_list:
#                 try:
#                     get_binance_klines(symbol, time_interval, temp_time, end_time)
#                 except Exception as e:
#                     print(e)
#                     error_list.append([symbol, time_interval, temp_time, end_time])
#         end_time = temp_time
#     else:
#         for symbol in symbol_list:
#             for time_interval in time_interval_list:
#                 try:
#                     get_binance_klines(symbol, time_interval, start_time, end_time)
#                 except Exception as e:
#                     print(e)
#                     error_list.append([symbol, time_interval, start_time, end_time])
#         break


# =====每天抓取数据
start_time = datetime.now() - timedelta(days=0) #days=1代表前一天，days=0代表当天,如此类推
# print(start_time)
end_time = start_time.strftime("%Y-%m-%d") + ' 23:59:00'
# print(end_time)
start_time = start_time.strftime("%Y-%m-%d") + ' 00:00:00'
# print(start_time)
# exit()
print(f'获取{start_time} 至 {end_time}数据')

for symbol in symbol_list:
    for time_interval in time_interval_list:
        try:
            get_binance_klines(symbol, time_interval, start_time, end_time)
        except Exception as e:
            print(e)
            error_list.append('_'.join([binance.id, symbol, time_interval]))

if len(error_list) > 0:
    print('以下数据抓取失败：')
    print(error_list)
else:
    print('******数据抓取成功！******')