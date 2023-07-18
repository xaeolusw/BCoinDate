import time
import pandas as pd
import os

def save_data_to_csv(file_path, exchange, instType, symbol, time_interval, day, df):
    # 创建交易所文件夹
    file_path = os.path.join(file_path, exchange.id)
    if os.path.exists(file_path) is False:
        os.mkdir(file_path)
    # 创建spot文件夹
    file_path = os.path.join(file_path, instType)
    if os.path.exists(file_path) is False:
        os.mkdir(file_path)
    # 创建交易对文件夹
    file_path = os.path.join(file_path, symbol)
    if os.path.exists(file_path) is False:
        os.mkdir(file_path)
    # 创建频次文件夹
    file_path = os.path.join(file_path, time_interval)
    if os.path.exists(file_path) is False:
        os.mkdir(file_path)

    # 拼接文件目录
    file_name = '_'.join([exchange.name, symbol.replace('/', '-'), str(pd.to_datetime(day)).split(' ')[0].replace('-',''),time_interval]) + '.csv'
    file_path = os.path.join(file_path, file_name)

    print(file_path)
    df.to_csv(file_path, index=False)

def get_binance_klines(global_binance_exchange, symbol, time_interval, start_time, end_time, global_instType, global_file_path):
    start_time_since = global_binance_exchange.parse8601(start_time) #parse8601（），用于将 ISO 8601 格式的时间字符串转换为 Unix 时间戳
    end_time_since = global_binance_exchange.parse8601(end_time)

    # =====循环获取数据
    # df_list = pd.DataFrame()
    all_kline_data = []

    while True:
        params = {
            'symbol': symbol,
            'interval': time_interval,
            'startTime': start_time_since, #如果未发送 startTime 和 endTime ，默认返回最近的交易。
            'endTime': end_time_since,
            'limit': 1000
        }  

        kline_data = global_binance_exchange.publicGetKlines(params=params)  # type: ignore # 获取数据
        

        # df = pd.DataFrame(kline_data, dtype=float)  # 将数据转换为dataframe #缺少这两行代码
        # df_list = pd.concat([df], ignore_index=True)  #缺少这两行代码
      
        if len(kline_data) > 1:
            start_time_since = kline_data[-1][0]  # 更新since，为下次循环做准备
            all_kline_data += kline_data
        else:
            break

        # 抓取间隔需要暂停2s，防止抓取过于频繁
        time.sleep(2)

    # 对数据进行整理
    # df = pd.concat(all_kline_data, ignore_index=True)
    df = pd.DataFrame(all_kline_data, dtype=float) 

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
                save_data_to_csv(global_file_path, global_binance_exchange, global_instType, symbol, time_interval, day, df)
                # # 创建交易所文件夹
                # file_path = os.path.join(global_file_path, global_binance_exchange.id)
                # if os.path.exists(file_path) is False:
                #     os.mkdir(file_path)
                # # 创建spot文件夹
                # file_path = os.path.join(file_path, 'spot')
                # if os.path.exists(file_path) is False:
                #     os.mkdir(file_path)
                # # 创建交易对文件夹
                # file_path = os.path.join(file_path, symbol)
                # if os.path.exists(file_path) is False:
                #     os.mkdir(file_path)
                # # 创建频次文件夹
                # file_path = os.path.join(file_path, time_interval)
                # if os.path.exists(file_path) is False:
                #     os.mkdir(file_path)

                # # 拼接文件目录
                # file_name = '_'.join([global_binance_exchange.name, symbol.replace('/', '-'), str(pd.to_datetime(day)).split(' ')[0].replace('-',''),time_interval]) + '.csv'
                # file_path = os.path.join(file_path, file_name)

                # print(file_path)
                # df.to_csv(file_path, index=False)
   
def get_okex_klines(global_okex_exchange, symbol, time_interval, start_time, end_time, global_instType, global_file_path):
    start_time_since = global_okex_exchange.parse8601(start_time)
    if start_time_since != None:
        start_time_since -= 1000 #parse8601（），用于将 ISO 8601 格式的时间字符串转换为 Unix 时间戳
    end_time_since = global_okex_exchange.parse8601(end_time)
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

        kline_data = global_okex_exchange.publicGetMarketHistoryCandles(params=params)['data'] # type: ignore
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
            save_data_to_csv(global_file_path, global_okex_exchange, global_instType, symbol, time_interval, day, df)
            