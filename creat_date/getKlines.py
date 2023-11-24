from getKlinesFunction import *

from datetime import timedelta, datetime

def main():
    global global_start_time, global_end_time, global_update_time

    print(f'开始时间：{global_start_time}')
    print(f'结束时间：{global_end_time}')
    print(f'更新时间：{global_update_time}')

    pre_day = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    if datetime.now().hour < 8:  # 早于8点不更新数据，退出。
        print('请过８点后再更新昨天数据！')
    elif pre_day <= global_update_time:
        print('数据已是最新')
    elif pre_day > global_update_time:
        global_start_time = (datetime.strptime(global_update_time, '%Y-%m-%d') + timedelta(days=1)).strftime(
            '%Y-%m-%d') + ' 00:00:00'
        global_update_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        global_end_time = global_update_time + ' 23:59:59'
        print(f'开始更新{global_start_time}至{global_end_time}的数据。')
    exit()

    binance_end_time = global_end_time
    #     okx_end_time = global_end_time
    #     okx_future_end_time = global_end_time

    #     # print(f'抓取binance{global_start_time}到{binance_end_time}的币币数据！')

    #     # # get_binance_klines(global_binance_exchange, 'BTCUSDT', '5m', global_start_time, binance_end_time, global_instType, global_file_path)
    #     # # exit()
    #     # while global_start_time < binance_end_time :
    #     #     temp_time = str(pd.to_datetime(binance_end_time) - timedelta(days=30))

    #     #     if temp_time > global_start_time :
    #     #         for symbol in global_binance_symbol_list:
    #     #             for time_interval in global_time_interval_list:
    #     #                 try:
    #     #                     get_binance_klines(global_binance_exchange, symbol, time_interval, temp_time, binance_end_time, global_instType, global_file_path)
    #     #                 except Exception as e:
    #     #                     print(e)
    #     #                     global_error_list.append([symbol, time_interval, temp_time, binance_end_time])
    #     #         binance_end_time = temp_time
    #     #     else:
    #     #         for symbol in global_binance_symbol_list:
    #     #             for time_interval in global_time_interval_list:
    #     #                 try:
    #     #                     get_binance_klines(global_binance_exchange, symbol, time_interval, global_start_time, binance_end_time, global_instType, global_file_path)
    #     #                 except Exception as e:
    #     #                     print(e)
    #     #                     global_error_list.append([symbol, time_interval, global_start_time, binance_end_time])
    #     #         break

    #     # =====选择开始、结束时间抓取数据
    #     print(f'抓取okx{global_start_time}到{okx_end_time}的币币数据！')

    #     while global_start_time < okx_end_time :
    #         temp_time = str(pd.to_datetime(okx_end_time) - timedelta(days=1))

    #         if temp_time > global_start_time :
    #             for symbol in global_okx_symbol_list:
    #                 for time_interval in global_time_interval_list:
    #                     get_okex_klines(global_okex_exchange, symbol, time_interval, temp_time, okx_end_time, global_instType, global_file_path)
    #             okx_end_time = temp_time
    #         else:
    #             for symbol in global_okx_symbol_list:
    #                 for time_interval in global_time_interval_list:
    #                     get_okex_klines(global_okex_exchange, symbol, time_interval, global_start_time, okx_end_time, global_instType, global_file_path)
    #             break

    #     # =====抓取数据开始结束时间
    #     print(f'获取okx{global_start_time} 至 {okx_future_end_time}合约数据')

    #     # =====设定获取的交易对参数
    #     # instType_list = ['SWAP','FUTURES'] #SPOT：币币;SWAP：永续合约;FUTURES：交割合约;OPTION：期权
    #     # uly_list = ['BTC-USDT','BTC-USD']
    #     for instType in global_okx_instType_list:
    #         symbol_list = []
    #         global_instType = instType

    #         for uly in global_okx_uly_list:
    #             params = {
    #                 'instType': instType, #SPOT：币币;SWAP：永续合约;FUTURES：交割合约;OPTION：期权
    #                 'uly': uly, #标的指数,适用于交割/永续/期权，如 BTC-USD
    #             #'instFamily': 'BTC-USD', #交易品种.适用于交割/永续/期权，如 BTC-USD
    #             }

    #             tickers = global_okex_exchange.publicGetMarketTickers(params=params)['data'] # type: ignore
    #             for ticker in tickers:
    #                 symbol_list.append(ticker['instId'])
    #             #print(symbol_list)

    #         for symbol in symbol_list:
    #             for time_interval in global_time_interval_list:
    #                 get_okex_klines(global_okex_exchange, symbol, time_interval, global_start_time, okx_future_end_time, global_instType, global_file_path)

    # if len(global_error_list) > 0:
    #     print('以下数据抓取失败：')
    #     for error in global_error_list:
    #         print(error)
    # else:
    #     print('数据抓取成功！')
    #     # df['start_time'][0] = global_update_time
    #     # df['end_time'][0] = global_update_time
    #     df['update_time'][0] = global_update_time
    #     df.to_csv(global_database_path, index=False)


if __name__ == '__main__':
    main()
