import pandas as pd
import ccxt
import os
from datetime import timedelta, datetime
from getKlinesFunction import *

# 定义全局变量类
# 设置代理服务器
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

# 设置币安和OKEx交易所
global_binance_exchange = ccxt.binance({
    'proxies': proxies
})

global_okex_exchange = ccxt.okex5({
    'proxies': proxies
})

# 根据操作系统设置数据库路径
if os.name == 'nt':
    global_database_path = 'D:\\PythonProjects\\coin_data\\getKlinesDatabase.csv'
    global_file_path = 'D:\\PythonProjects\\coin_data'
elif os.name == 'posix':
    global_database_path = '/Volumes/USB-DISK/PythonProjects/coin_data/getKlinesDatabase.csv'
    global_file_path = '/Volumes/USB-DISK/PythonProjects/coin_data'
else:
    print('操作系统不支持')
    exit()

global_error_list = []

global_binance_symbol_list = []  # 'BTCUSDT','ETHUSDT','EOSUSDT','LTCUSDT'
global_okx_symbol_list = []  # 'BTC-USDT','ETH-USDT','EOS-USDT','LTC-USDT'

global_okx_instType_list = ['SWAP','FUTURES'] #SPOT：币币;SWAP：永续合约;FUTURES：交割合约;OPTION：期权
global_okx_uly_list = ['BTC-USDT','BTC-USD']

global_instType = 'SPOT'

# 从csv文件中读取初始数据
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
df = pd.read_csv(
    filepath_or_buffer = global_database_path, 
    encoding='utf8', 
    sep=',',
)  

global_time_interval_list = []  # 其他可以尝试的值：'1m', '5m', '15m', '30m', '1H', '2H', '1D', '1W', '1M', '1Y'
for symblo in df['symbol']:
    global_binance_symbol_list.append(symblo + 'USDT')
    global_okx_symbol_list.append(symblo + '-USDT')

for interval in df['interval']:
    if interval != '0':
        global_time_interval_list.append(interval)

global_start_time = df['start_time'][0]
global_end_time = df['end_time'][0]
global_update_time = df['update_time'][0]

# if global_start_time == np.nan:
#     print('首次获取数据')
# else:
#     print('1')
# print(global_start_time)
# exit()

# exit()
if True:
    pre_pre_day = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
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
        global_start_time = (datetime.strptime(global_update_time, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d') + ' 00:00:00'
        global_update_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        global_end_time = global_update_time + ' 23:59:59'
    else:
        print('数据已是最新')
        exit()
else:
    getPreDayDate = False
    

if getPreDayDate:
    # =====每天抓取数据
    start_time = global_update_time + ' 00:00:00'
    end_time = global_update_time + ' 23:59:00'
    global_instType = 'spot'
    print(f'获取binance{start_time} 至 {end_time}数据')

    for symbol in global_binance_symbol_list:
        for time_interval in global_time_interval_list:
            try:
                get_binance_klines(global_binance_exchange, symbol, time_interval, start_time, end_time, global_instType, global_file_path)
            except Exception as e:
                print(e)
                global_error_list.append('_'.join([str(global_binance_exchange.id), symbol, time_interval]))

    # =====获取okx前一天币币数据
    print(f'获取okx{start_time} 至 {end_time}币币数据')
    global_instType = 'SPOT' 
    for symbol in global_okx_symbol_list:
        for time_interval in global_time_interval_list:
            try:
                get_okex_klines(global_okex_exchange, symbol, time_interval, start_time, end_time, global_instType, global_file_path)
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
                get_okex_klines(global_okex_exchange, symbol, time_interval, start_time, end_time, global_instType, global_file_path)
else:
    binance_end_time = global_end_time
    okx_end_time = global_end_time
    okx_future_end_time = global_end_time
      
    # print(f'抓取binance{global_start_time}到{binance_end_time}的币币数据！')

    # # get_binance_klines(global_binance_exchange, 'BTCUSDT', '5m', global_start_time, binance_end_time, global_instType, global_file_path)
    # # exit()
    # while global_start_time < binance_end_time :
    #     temp_time = str(pd.to_datetime(binance_end_time) - timedelta(days=30))

    #     if temp_time > global_start_time :
    #         for symbol in global_binance_symbol_list:
    #             for time_interval in global_time_interval_list:
    #                 try:
    #                     get_binance_klines(global_binance_exchange, symbol, time_interval, temp_time, binance_end_time, global_instType, global_file_path)
    #                 except Exception as e:
    #                     print(e)
    #                     global_error_list.append([symbol, time_interval, temp_time, binance_end_time])
    #         binance_end_time = temp_time
    #     else:
    #         for symbol in global_binance_symbol_list:
    #             for time_interval in global_time_interval_list:
    #                 try:
    #                     get_binance_klines(global_binance_exchange, symbol, time_interval, global_start_time, binance_end_time, global_instType, global_file_path)
    #                 except Exception as e:
    #                     print(e)
    #                     global_error_list.append([symbol, time_interval, global_start_time, binance_end_time])
    #         break

    # =====选择开始、结束时间抓取数据
    print(f'抓取okx{global_start_time}到{okx_end_time}的币币数据！')

    while global_start_time < okx_end_time :
        temp_time = str(pd.to_datetime(okx_end_time) - timedelta(days=1))

        if temp_time > global_start_time :
            for symbol in global_okx_symbol_list:
                for time_interval in global_time_interval_list:
                    get_okex_klines(global_okex_exchange, symbol, time_interval, temp_time, okx_end_time, global_instType, global_file_path)
            okx_end_time = temp_time
        else:
            for symbol in global_okx_symbol_list:
                for time_interval in global_time_interval_list:
                    get_okex_klines(global_okex_exchange, symbol, time_interval, global_start_time, okx_end_time, global_instType, global_file_path)
            break

    # =====抓取数据开始结束时间
    print(f'获取okx{global_start_time} 至 {okx_future_end_time}合约数据')

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
                get_okex_klines(global_okex_exchange, symbol, time_interval, global_start_time, okx_future_end_time, global_instType, global_file_path)

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