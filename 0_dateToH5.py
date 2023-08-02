import pandas as pd
import glob
import os
import time
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# 筛选出指定币种和指定时间
symbol_list = ['BTCUSDT', 'ETHUSDT']

for symbol in symbol_list:
    # 获取数据的路径
    if os.name == 'nt':
        path = 'D:\\PythonProjects\\coin_data\\binance\\spot\\%s\\5m'%symbol  
    elif os.name == 'posix':
        path = '/Volumes/USB-DISK/PythonProjects/coin_data/binance/spot/%s/5m'%symbol
    else:
        print('操作系统不支持')
        exit()

    path_list = glob.glob(path + "/*.csv")  # python自带的库，获得某文件夹中所有csv文件的路径

    path_list = list(filter(lambda x: symbol in x, path_list))

    # 导入数据
    df_list = []
    for path in sorted(path_list):
        # print(path)
        df = pd.read_csv(path, parse_dates=['candle_begin_time'])
        df = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume', 'quote_asset_volume']]
        df['quote_asset_volume'].rename('quote_volume', inplace=True)
        df_list.append(df)

    # 整理完整数据
    data = pd.concat(df_list, ignore_index=True)
    data.sort_values(by='candle_begin_time', inplace=False)
    data.reset_index(drop=False, inplace=False)

    # 导出完整数据
    if os.name == 'nt':
        path = 'D:\\PythonProjects\\coin_data\\binance_%s_5m.h5' % symbol
        data.to_hdf(path, key='%s_5m' % symbol, mode='w')
        print('转换成功, 转换为%s'%path)
    elif os.name == 'posix':
        path = '/Volumes/USB-DISK/PythonProjects/coin_data/binance_%s_5m.h5' % symbol
        data.to_hdf(path, key='%s_5m' % symbol, mode='w')
        print('转换成功, 转换为%s'%path)
    else:
        print('操作系统不支持')
        exit()
        
    # if os.name == 'nt':
    #     path = 'D:\\PythonProjects\\coin_data\\binance_%s_5m_%s.h5' % (symbol, time.strftime('%Y-%m-%d',time.localtime()))
    #     data.to_hdf(path, key='%s_5m' % symbol, mode='w')
    #     print('转换成功, 转换为%s'%path)
    # elif os.name == 'posix':
    #     path = '/Volumes/USB-DISK/PythonProjects/coin_data/binance_%s_5m_%s.h5' % (symbol, time.strftime('%Y-%m-%d',time.localtime()))
    #     data.to_hdf(path, key='%s_5m' % symbol, mode='w')
    #     print('转换成功, 转换为%s'%path)
    # else:
    #     print('操作系统不支持')
    #     exit()

