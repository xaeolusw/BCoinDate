import pandas as pd
import ccxt
import time
import os
from datetime import timedelta, datetime

# =====设定参数
#定义全局变量类
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

global_binance_exchange = ccxt.binance({
    'proxies': proxies
})

global_okex_exchange = ccxt.okex5({
    'proxies': proxies
})
    
# global_database_path = ''
# global_file_path = ''

if os.name == 'nt':
    global_database_path = r'D:\PythonProjects\coin_data\getKlinesDatabase.csv'
    global_file_path = r'D:\PythonProjects\coin_data'
elif os.name == 'posix':
    global_database_path = r'/Volumes/USB-DISK/getKlinesDatabase.csv'
    global_file_path = r'/Volumes/USB-DISK/PythonProjects/coin_data'
else:
    print('操作系统不支持')
    exit()

global_error_list = []
global_time_interval_list = []  # 其他可以尝试的值：'1m', '5m', '15m', '30m', '1H', '2H', '1D', '1W', '1M', '1Y'

global_binance_symbol_list = []  #'BTCUSDT','ETHUSDT','EOSUSDT','LTCUSDT'

global_okx_symbol_list = []  #'BTC-USDT','ETH-USDT','EOS-USDT','LTC-USDT'
global_okx_instType_list = ['SWAP','FUTURES'] #SPOT：币币;SWAP：永续合约;FUTURES：交割合约;OPTION：期权
global_okx_uly_list = ['BTC-USDT','BTC-USD']

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
df = pd.read_csv(
    filepath_or_buffer = global_database_path, #MAC系统下的路径r'/Volumes/USB-DISK/getKlinesDatabase.csv';Windows系统下的路径r'D:\PythonProjects\getKlinesDatabase.csv'
    encoding='utf8', 
    sep=',',
)  # 从csv文件中读取数据

for symblo in df['symbol']:
    global_binance_symbol_list.append(symblo + 'USDT')
    global_okx_symbol_list.append(symblo + '-USDT')
     
for interval in df['interval']:
    if interval != '0':
        global_time_interval_list.append(interval)

global_start_time = df['start_time'][0]
global_end_time = df['end_time'][0]
global_update_time = df['update_time'][0]
global_instType = 'SPOT'
# getPreDayDate = True
# start_time = '2023-06-16 00:00:00'
# end_time = '2023-06-18 23:59:00'

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

def get_binance_klines(symbol, time_interval, start_time, end_time):
    global global_binance_exchange, global_instType, global_file_path
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
   
def get_okex_klines(symbol, time_interval, start_time, end_time):
    global global_okex_exchange, global_instType
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
            # 根目录，确保该路径存在
            #path = r'/Volumes/USB-DISK/PythonProjects/coin_data'
            #MAC系统下的路径:'/Volumes/USB-DISK/PythonProjects/coin_data'
            #Windows系统下的路径:'D:\PythonProjects\coin_data'

            # 创建交易所文件夹
            # filePath = os.path.join(global_file_path, global_okex_exchange.id)
            # if os.path.exists(filePath) is False:
            #     os.mkdir(filePath)
            # # 创建spot文件夹
            # filePath = os.path.join(filePath, global_instType)
            # if os.path.exists(filePath) is False:
            #     os.mkdir(filePath)
            # # 创建交易对文件夹
            # filePath = os.path.join(filePath, symbol)
            # if os.path.exists(filePath) is False:
            #     os.mkdir(filePath)
            # # 创建频次文件夹
            # filePath = os.path.join(filePath, time_interval)
            # if os.path.exists(filePath) is False:
            #     os.mkdir(filePath)

            # # 拼接文件目录
            # file_name = '_'.join([global_okex_exchange.name, symbol.replace('/', '-'), str(pd.to_datetime(day)).split(' ')[0].replace('-',''),time_interval]) + '.csv'
            # filePath = os.path.join(filePath, file_name)

            # print(filePath)
            # df.to_csv(filePath, index=False)

#手工设置起始时间时以下代码禁止
pre_pre_day = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
# print('pre_pre_day:',pre_pre_day,'global_update_time:',global_update_time)
# exit()
if pre_pre_day == global_update_time:
    if datetime.now().hour < 8:
        print('请过８点后再更新昨天数据！')
        exit()
    else:
        print('更新昨天数据中')
        global_update_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        getPreDayDate = True
elif pre_pre_day > global_update_time:
    print('批量更新数据中')
    getPreDayDate = False
else:
    print('数据已是最新')
    exit()

# print(pre_pre_day,global_update_time,getPreDayDate)
# exit()
#程序开始：
# if False: #手工设置起始时间时使用
if getPreDayDate:
    # =====每天抓取数据
    start_time = global_update_time + ' 00:00:00'
    end_time = global_update_time + ' 23:59:00'
    global_instType = 'spot'
    print(f'获取binance{start_time} 至 {end_time}数据')

    for symbol in global_binance_symbol_list:
        for time_interval in global_time_interval_list:
            try:
                get_binance_klines(symbol, time_interval, start_time, end_time)
            except Exception as e:
                print(e)
                global_error_list.append('_'.join([str(global_binance_exchange.id), symbol, time_interval]))

    # =====获取okx前一天币币数据
    print(f'获取okx{start_time} 至 {end_time}币币数据')
    global_instType = 'SPOT' 
    for symbol in global_okx_symbol_list:
        for time_interval in global_time_interval_list:
            try:
                get_okex_klines(symbol, time_interval, start_time, end_time)
            except Exception as e:
                print(e)
                global_error_list.append('_'.join([str(global_okex_exchange.id), symbol, time_interval]))

    # =====抓取数据开始结束时间
    print(f'获取okx{start_time} 至 {end_time}合约数据')

    # =====设定获取的交易对参数
    # instType_list = ['SWAP','FUTURES'] #SPOT：币币;SWAP：永续合约;FUTURES：交割合约;OPTION：期权
    # uly_list = ['BTC-USDT','BTC-USD']
    for instType in global_okx_instType_list:
        symbol_list = []
        global_instType = instType

        for uly in global_okx_uly_list:
            params = {
                'instType': instType, #SPOT：币币;SWAP：永续合约;FUTURES：交割合约;OPTION：期权
                'uly': uly, #标的指数,适用于交割/永续/期权，如 BTC-USD
            #'instFamily': 'BTC-USD', #交易品种.适用于交割/永续/期权，如 BTC-USD          
            } 

            tickers = global_okex_exchange.publicGetMarketTickers(params=params)['data'] # type: ignore
            for ticker in tickers:
                symbol_list.append(ticker['instId'])
            #print(symbol_list)

        for symbol in symbol_list:
            for time_interval in global_time_interval_list:
                get_okex_klines(symbol, time_interval, start_time, end_time)
else:
    #=====选择开始、结束时间抓取数据
    start_time = (datetime.strptime(global_update_time, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d') + ' 00:00:00'
    # global_update_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    global_update_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    binance_end_time = global_update_time + ' 23:59:59'

    # #手工设置起始时间
    # start_time = '2023-06-22 00:00:00'
    # binance_end_time = '2023-06-23 23:59:59'

    okx_end_time = binance_end_time

    okx_future_end_time = binance_end_time
      
    print(f'抓取binance{start_time}到{binance_end_time}的币币数据！')

    while start_time < binance_end_time :
        temp_time = str(pd.to_datetime(binance_end_time) - timedelta(days=30))

        if temp_time > start_time :
            for symbol in global_binance_symbol_list:
                for time_interval in global_time_interval_list:
                    try:
                        get_binance_klines(symbol, time_interval, temp_time, binance_end_time)
                    except Exception as e:
                        print(e)
                        global_error_list.append([symbol, time_interval, temp_time, binance_end_time])
            binance_end_time = temp_time
        else:
            for symbol in global_binance_symbol_list:
                for time_interval in global_time_interval_list:
                    try:
                        get_binance_klines(symbol, time_interval, start_time, binance_end_time)
                    except Exception as e:
                        print(e)
                        global_error_list.append([symbol, time_interval, start_time, binance_end_time])
            break

    # =====选择开始、结束时间抓取数据
    print(f'抓取okx{start_time}到{binance_end_time}的币币数据！')

    while start_time < okx_end_time :
        temp_time = str(pd.to_datetime(okx_end_time) - timedelta(days=1))

        if temp_time > start_time :
            for symbol in global_okx_symbol_list:
                for time_interval in global_time_interval_list:
                    get_okex_klines(symbol, time_interval, temp_time, okx_end_time)
            okx_end_time = temp_time
        else:
            for symbol in global_okx_symbol_list:
                for time_interval in global_time_interval_list:
                    get_okex_klines(symbol, time_interval, start_time, okx_end_time)
            break

    # =====抓取数据开始结束时间
    print(f'获取okx{start_time} 至 {okx_future_end_time}合约数据')

    # =====设定获取的交易对参数
    # instType_list = ['SWAP','FUTURES'] #SPOT：币币;SWAP：永续合约;FUTURES：交割合约;OPTION：期权
    # uly_list = ['BTC-USDT','BTC-USD']
    for instType in global_okx_instType_list:
        symbol_list = []
        global_instType = instType

        for uly in global_okx_uly_list:
            params = {
                'instType': instType, #SPOT：币币;SWAP：永续合约;FUTURES：交割合约;OPTION：期权
                'uly': uly, #标的指数,适用于交割/永续/期权，如 BTC-USD
            #'instFamily': 'BTC-USD', #交易品种.适用于交割/永续/期权，如 BTC-USD          
            } 

            tickers = global_okex_exchange.publicGetMarketTickers(params=params)['data'] # type: ignore
            for ticker in tickers:
                symbol_list.append(ticker['instId'])
            #print(symbol_list)

        for symbol in symbol_list:
            for time_interval in global_time_interval_list:
                get_okex_klines(symbol, time_interval, start_time, okx_future_end_time)

if len(global_error_list) > 0:
    print('以下数据抓取失败：')
    for error in global_error_list:
        print(error)
else:
    print('数据抓取成功！')
    # df['start_time'][0] = global_update_time
    # df['end_time'][0] = global_update_time
    df['update_time'][0] = global_update_time
    df.to_csv(global_database_path, index=False)