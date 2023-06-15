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

okex = ccxt.okex5({
    'proxies': proxies
})

def get_okex_klines(symbol, time_interval, start_time, end_time):
    start_time_since = okex.parse8601(start_time) -1000 #parse8601（），用于将 ISO 8601 格式的时间字符串转换为 Unix 时间戳
    end_time_since = okex.parse8601(end_time)
    # timestamp = pd.to_datetime(start_time_since, unit='ms')
    # print(timestamp)
    # timestamp = pd.to_datetime(end_time_since, unit='ms')
    # print(timestamp)

    # =====循环获取数据
    df_list = []
    all_kline_data = []

    while True:
        params = {
            'instId': symbol,
            'bar': time_interval,
            'after': end_time_since, #请求此时间戳之前（更旧的数据）的分页内容。
            'before': start_time_since, #请求此时间戳之后（更新的数据）的分页内容            
        }  

        kline_data = okex.publicGetMarketHistoryCandles(params=params)['data']
        # for i in range(len(kline_data)):
        #     print(pd.to_datetime(int(kline_data[i][0]), unit='ms'))
        
        # print(len(kline_data))
        if len(kline_data) > 0:
            df = pd.DataFrame(kline_data, dtype=float)  # 将数据转换为dataframe
            df_list.append(df)  
        
            end_time_since = kline_data[-1][0]  # 更新since，为下次循环做准备
            all_kline_data += kline_data
        else:
            break

        # 抓取间隔需要暂停2s，防止抓取过于频繁
        time.sleep(2)
  
    # 对数据进行整理
    df = pd.concat(df_list, ignore_index=True)
    df.rename(columns={0:'ts', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'vol',6:'volCcy',7:'volCcyQuote',8:'confirm'}, inplace=True)
    df['candle_begin_time'] = pd.to_datetime(df['ts'], unit='ms') 
    df = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'vol','volCcy','volCcyQuote','confirm']]

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
            path = os.path.join(path, okex.id)
            if os.path.exists(path) is False:
                os.mkdir(path)
            # 创建spot文件夹
            path = os.path.join(path, instType)
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
            file_name = '_'.join([okex.name, symbol.replace('/', '-'), str(pd.to_datetime(day)).split(' ')[0].replace('-',''),time_interval]) + '.csv'
            path = os.path.join(path, file_name)

            print(path)
            df.to_csv(path, index=False)


# # =====获取历史币币数据
# # =====设定参数
# symbol_list = ['BTC-USDT','ETH-USDT','EOS-USDT','LTC-USDT'] 
# time_interval_list = ['5m','15m']  # 其他可以尝试的值：'1m', '5m', '15m', '30m', '1H', '2H', '1D', '1W', '1M', '1Y'

# # =====抓取数据开始结束时间
# start_time = '2022-01-01 00:00:00'
# end_time = '2023-05-27 00:00:00'
# # end_time = str(pd.to_datetime(start_time) + timedelta(days=1))

# while start_time < end_time :
#     temp_time = str(pd.to_datetime(end_time) - timedelta(days=1))

#     if temp_time > start_time :
#         for symbol in symbol_list:
#             for time_interval in time_interval_list:
#                 get_okex_klines(symbol, time_interval, temp_time, end_time)
#         end_time = temp_time
#     else:
#         for symbol in symbol_list:
#             for time_interval in time_interval_list:
#                 get_okex_klines(symbol, time_interval, start_time, end_time)
#         break
    

# =====获取前一天永续合约、交割合约数据
# =====设定获取的时间间隔参数
error_list = []
time_interval_list = ['5m','15m']  # 其他可以尝试的值：'1m', '5m', '15m', '30m', '1H', '2H', '1D', '1W', '1M', '1Y'

# =====抓取数据开始结束时间
end_time = datetime.now() - timedelta(days=2)     #days=1代表前一天，days=0代表当天,如此类推
start_time = end_time.strftime("%Y-%m-%d") + ' 00:00:00'
end_time = end_time.strftime("%Y-%m-%d") + ' 23:59:00'
print(f'获取{start_time} 至 {end_time}合约数据')

# =====设定获取的交易对参数
instType_list = ['SWAP','FUTURES'] #SPOT：币币;SWAP：永续合约;FUTURES：交割合约;OPTION：期权
uly_list = ['BTC-USDT','BTC-USD']
for instType in instType_list:
    symbol_list = []

    for uly in uly_list:
        params = {
            'instType': instType, #SPOT：币币;SWAP：永续合约;FUTURES：交割合约;OPTION：期权
            'uly': uly, #标的指数,适用于交割/永续/期权，如 BTC-USD
        #'instFamily': 'BTC-USD', #交易品种.适用于交割/永续/期权，如 BTC-USD          
        } 

        tickers = okex.publicGetMarketTickers(params=params)['data']
        for ticker in tickers:
            symbol_list.append(ticker['instId'])
        #print(symbol_list)

    for symbol in symbol_list:
        for time_interval in time_interval_list:
            get_okex_klines(symbol, time_interval, start_time, end_time)
        

# =====获取前一天币币数据
print(f'获取{start_time} 至 {end_time}币币数据')
instType = 'SPOT'
symbol_list = ['BTC-USDT','ETH-USDT','EOS-USDT','LTC-USDT'] 

for symbol in symbol_list:
    for time_interval in time_interval_list:
        try:
            get_okex_klines(symbol, time_interval, start_time, end_time)
        except Exception as e:
            print(e)
            error_list.append('_'.join([okex.id, symbol, time_interval]))

if len(error_list) > 0:
    print('以下数据抓取失败：')
    print(error_list)
else:
    print('数据抓取成功！')