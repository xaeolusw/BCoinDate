"""
更新时间：2021-10-08
《邢不行|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
择时策略实盘需要的相关函数
"""
import ccxt
import math
import time
import pandas as pd
from datetime import datetime, timedelta
import json
import requests
import time
import hmac
import hashlib
import base64
from urllib import parse
from multiprocessing import Pool
from functools import partial
from Config import *
from Signals import *
import Signals
from GlobalVar import *


# =====okex交互函数
# ===通过ccxt、交易所接口获取合约账户信息
def ccxt_fetch_future_account(exchange, max_try_amount=5):
    """
    :param exchange:
    :param max_try_amount:
    :return:

    本程序使用okex5中"获取资金账户余额"、"查看持仓信息"接口，获取账户USDT的余额与持仓信息。
    使用ccxt函数：private_get_account_balance() 与 private_get_account_positions()
    exchange.private_get_account_balance()
    {
        'code': '0', 
        'data': [
            {
                'adjEq': '', 
                'details': [
                    {
                        'availBal': '34.66', 
                        'availEq': '34.66', 
                        'cashBal': '34.66', 
                        'ccy': 'USDT', 
                        'crossLiab': '', 
                        'disEq': '34.6364312', 
                        'eq': '34.66', 
                        'eqUsd': '34.6364312', 
                        'fixedBal': '0', 
                        'frozenBal': '0', 
                        'interest': '', 
                        'isoEq': '0', 
                        'isoLiab': '', 
                        'isoUpl': '0', 
                        'liab': '', 
                        'maxLoan': '', 
                        'mgnRatio': '', 
                        'notionalLever': '0', 
                        'ordFrozen': '0', 
                        'spotInUseAmt': '', 
                        'stgyEq': '0', 
                        'twap': '0', 
                        'uTime': '1690964742627', 
                        'upl': '0', 
                        'uplLiab': ''
                    }
                ], 
                'imr': '', 
                'isoEq': '0', 
                'mgnRatio': '', 
                'mmr': '', 
                'notionalUsd': '', 
                'ordFroz': '', 
                'totalEq': '34.6364312', 
                'uTime': '1691139445709'
            }
        ], 
        'msg': ''
    }
    """

    for _try_time in range(max_try_amount):
        try:
            print('通过ccxt的private_get_account_balance获取所有合约账户信息，尝试次数：', _try_time + 1)
            balance_of = float(
                exchange.private_get_account_balance({'ccy': 'USDT'})['data'][0]['details'][0]['cashBal']) #获取帐户余额（USDT）;
            
            return balance_of
        except Exception as e:
            print('通过ccxt的通过futures_get_accounts获取所有合约账户信息，失败，稍后重试：\n', e)
            time.sleep(medium_sleep_time)

    _error = '通过ccxt的通过futures_get_accounts获取余额与持仓信息，失败次数过多，程序Raise Error'
    send_dingding_and_raise_error(_error)


# ===通过ccxt、交易所接口获取合约账户持仓信息
def ccxt_fetch_future_position(exchange, max_try_amount=5):
    """
    :param exchange:
    :param max_try_amount:
    :return:
    本程序使用okex5中"查看持仓信息"接口，获取账户USDT的余额与持仓信息。
    使用ccxt函数：private_get_account_positions()
    接口返回数据格式样例：
    {
        'code': '0', 
        'data': [
            {
                'adl': '5', 
                'availPos': '1', 
                'avgPx': '1701.27',     #持仓均价
                'baseBal': '', 
                'baseBorrowed': '', 
                'baseInterest': '', 
                'bizRefId': '', 
                'bizRefType': '', 
                'cTime': '1693454176011', 
                'ccy': 'USDT', 
                'closeOrderAlgo': [], 
                'deltaBS': '', 
                'deltaPA': '', 
                'fee': '', 
                'fundingFee': '', 
                'gammaBS': '', 
                'gammaPA': '', 
                'idxPx': '1701.31', 
                'imr': '', 
                'instId': 'ETH-USDT-230929',  #产品ID
                'instType': 'FUTURES', 
                'interest': ''ID
                'last': '1704.21',  #当前价格
                'lever': '10',  #最大杠杆
                'liab': '', 
                'liabCcy': '', 
                'liqPenalty': '', 
                'liqPx': '1538.0742893018582', 
                'margin': '17.0127', 
                'markPx': '1703.76', 
                'mgnMode': 'isolated', 
                'mgnRatio': '22.514516911615093', 
                'mmr': '0.681504', 
                'notionalUsd': '170.40496392', 
                'optVal': '', 
                'pendingCloseOrdLiabVal': '', 
                'pnl': '', 
                'pos': '1',     #持仓量
                'posCcy': '', 
                'posId': '617326789572333579', 
                'posSide': 'long', 
                'quoteBal': '', 
                'quoteBorrowed': '', 
                'quoteInterest': '', 
                'realizedPnl': '', 
                'spotInUseAmt': '', 
                'spotInUseCcy': '', 
                'thetaBS': '', 
                'thetaPA': '', 
                'tradeId': 
                '1638985', 
                'uTime': '1693454176011', 
                'upl': '0.2490000000000009',    #持仓收益
                'uplLastPx': '0.2940000000000055', 
                'uplRatio': '0.0146361247773719',   #持仓收益率
                'uplRatioLastPx': 
                '0.0172812075684647', 
                'usdPx': '', 
                'vegaBS': '', 
                'vegaPA': ''
            }
        ], 
        'msg': ''
    }
    返回结果说明：
    1.币本位合约和usdt本位合约的信息会一起返回。
    2.一个币种同时有多头或者空头，会分别返回
    """
    for _ in range(max_try_amount):
        try:
            # 获取数据
            # df = pd.DataFrame(exchange.private_get_account_positions()['data'], dtype=float)  #会报错：could not convert string to float: ''，修改如下：
            df = pd.DataFrame(exchange.private_get_account_positions()['data'])

            df = df[['instId','pos', 'upl', 'uplRatio', 'avgPx','last','lever']] #选择特定列。
            
            def convert_to_float(x):
                try:
                    return float(x)
                except:
                    return x
            df = df.applymap(convert_to_float)
            # 整理数据
            # 防止账户初始化时出错

            if "instId" in df.columns:
                df['index'] = df['instId'].str.lower()
                df.set_index(keys='index', inplace=True)
                df.index.name = None
                df['instrument_id'] = df['instId']
            return df
        except Exception as e:
            print('通过ccxt的通过futures_get_position获取所有合约的持仓信息，失败，稍后重试。失败原因：\n', e)
            time.sleep(medium_sleep_time)

    _ = '通过ccxt的通过futures_get_position获取所有合约的持仓信息，失败次数过多，程序Raise Error'
    send_dingding_and_raise_error(_)


# ===通过ccxt获取K线数据
def ccxt_fetch_candle_data(exchange: ccxt.okex5, symbol, time_interval, limit, max_try_amount=5):
    """
    本程序使用ccxt的fetch_ohlcv()函数，获取最新的K线数据，用于实盘
    :param exchange:
    :param symbol:
    :param time_interval:
    :param limit:
    :param max_try_amount:
    :return:
    """
    for _ in range(max_try_amount):
        try:
            # 获取数据
            # data = exchange.fetch_ohlcv(symbol=symbol, timeframe=time_interval, limit=limit)
            data = exchange.publicGetMarketCandles({
                'instId': symbol,
                'bar': time_interval,
                'limit': limit,
            })['data']
            # 整理数据
            df = pd.DataFrame(data, dtype=float)
            df.rename(columns={0: 'MTS', 1: 'open', 2: 'high',
                               3: 'low', 4: 'close', 5: 'volume'}, inplace=True)
            df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms')
            df['candle_begin_time_GMT8'] = df['candle_begin_time'] + timedelta(hours=8)
            df = df[['candle_begin_time_GMT8', 'open', 'high', 'low', 'close', 'volume']]
            return df
        except Exception as e:
            print('获取fetch_ohlcv获取合约K线数据，失败，稍后重试。失败原因：\n', e)
            time.sleep(short_sleep_time)

    _ = '获取fetch_ohlcv合约K线数据，失败次数过多，程序Raise Error'
    send_dingding_and_raise_error(_)


# =====趋势策略相关函数
# 根据账户信息、持仓信息，更新symbol_info
def update_symbol_info(exchange, symbol_info, symbol_config):
    """
    本函数通过private_get_account_balance()获取账户信息，private_get_account_positions()获取账户持仓信息，并用这些信息更新symbol_config
    :param exchange:
    :param symbol_info:
    :param symbol_config:
    :return:
    """
    # 初始化持仓方向.默认为没有持仓
    symbol_info['持仓方向'] = 0
    # 通过交易所接口获取合约账户信息
    balance_of = ccxt_fetch_future_account(exchange)
    # 将账户信息和symbol_info合并
    symbol_info['账户余额'] = balance_of

    # 通过交易所接口获取合约账户持仓信息
    future_position = ccxt_fetch_future_position(exchange)
    # print(future_position)
    # print(symbol_info)
    # exit()
    # 将持仓信息和symbol_info合并
    if not future_position.empty:
        # 去除无关持仓：账户中可能存在其他合约的持仓信息，这些合约不在symbol_config中，将其删除。
        
        instrument_id_list = [symbol_config[x]['instrument_id'] for x in symbol_config.keys()]
        future_position = future_position[future_position.instrument_id.isin(instrument_id_list)]

        # print(instrument_id_list)
        # print(future_position)
        if future_position.empty:
            return symbol_info


        # 从future_position中获取原始数据
        symbol_info['最大杠杆'] = future_position['lever']
        # print(symbol_info['最大杠杆'])
        # print(future_position['lever'])
        # exit()
        symbol_info['当前价格'] = future_position['last']

        symbol_info['持仓量'] = future_position['pos']
        symbol_info['持仓均价'] = future_position['avgPx']
        symbol_info['持仓收益率'] = future_position['uplRatio']
        symbol_info['持仓收益'] = future_position['upl']
        symbol_info['产品ID'] = future_position['instId']

        # 当账户是买卖模式的时候,接口返回的持仓数量负数为做空,正数为做多
        symbol_info['pos'] = future_position['pos']
        symbol_info.loc[symbol_info['pos'] < 0, '持仓方向'] = -1
        symbol_info.loc[symbol_info['pos'] > 0, '持仓方向'] = 1
        del symbol_info['pos']

        # 检验是否同时持有多头和空头, 买卖模式不会存在同时多头和空头,这里理论来说可以去掉
        if len(symbol_info[symbol_info.duplicated('产品ID')]) > 1:
            print(symbol_info['产品ID'], '当前账户同时存在多仓和空仓，请平掉其中至少一个仓位后再运行程序，程序exit')
            exit()

    return symbol_info


# 获取需要的K线数据，并检测质量。
def get_candle_data(exchange, symbol_config, time_interval, run_time, max_try_amount, candle_num, symbol):
    """
    使用ccxt_fetch_candle_data(函数)，获取指定交易对最新的K线数据，并且监测数据质量，用于实盘。
    :param exchange:
    :param symbol_config:
    :param time_interval:
    :param run_time:
    :param max_try_amount:
    :param symbol:
    :param candle_num:
    :return:
    尝试获取K线数据，并检验质量
    """
    # 标记开始时间
    start_time = datetime.now()
    print('开始获取K线数据：', symbol, '开始时间：', start_time)

    # 获取数据合约的相关参数
    instrument_id = symbol_config[symbol]["instrument_id"]  # 合约id
    signal_price = None

    # 尝试获取数据
    for i in range(max_try_amount):
        # 获取symbol该品种最新的K线数据
        df = ccxt_fetch_candle_data(exchange, instrument_id, time_interval, limit=candle_num)
        if df.empty:
            continue  # 再次获取

        # 判断是否包含最新一根的K线数据。例如当time_interval为15分钟，run_time为14:15时，即判断当前获取到的数据中是否包含14:15这根K线
        # 【其实这段代码可以省略】
        if time_interval.endswith('m') or time_interval.endswith('M'):
            _ = df[df['candle_begin_time_GMT8'] == (run_time - timedelta(minutes=int(time_interval[:-1])))]
        elif time_interval.endswith('h') or time_interval.endswith('H'):
            _ = df[df['candle_begin_time_GMT8'] == (run_time - timedelta(hours=int(time_interval[:-1])))]
        else:
            print('time_interval不以m或者h结尾，出错，程序exit')
            exit()
        if _.empty:
            print('获取数据不包含最新的数据，重新获取')
            time.sleep(short_sleep_time)
            continue  # 再次获取

        else:  # 获取到了最新数据
            signal_price = df.iloc[-1]['close']  # 该品种的最新价格
            df = df[df['candle_begin_time_GMT8'] < pd.to_datetime(run_time)]  # 去除run_time周期的数据
            print('结束获取K线数据', symbol, '结束时间：', datetime.now())
            return symbol, df, signal_price

    print('获取candle_data数据次数超过max_try_amount，数据返回空值')
    return symbol, pd.DataFrame(), signal_price


# 串行获取K线数据
def single_threading_get_data(exchange, symbol_info, symbol_config, time_interval, run_time, candle_num,
                              max_try_amount=5):
    """
    串行逐个获取所有交易对的K线数据，速度较慢
    若获取数据失败，返回空的dataframe。
    :param exchange:
    :param symbol_info:
    :param symbol_config:
    :param time_interval:
    :param run_time:
    :param candle_num:
    :param max_try_amount:
    :return:
    """
    # 函数返回的变量
    symbol_candle_data = {}
    for symbol in symbol_config.keys():
        symbol_candle_data[symbol] = pd.DataFrame()

    # 逐个获取symbol对应的K线数据
    for symbol in symbol_config.keys():
        _, symbol_candle_data[symbol], symbol_info.at[symbol, '信号价格'] = get_candle_data(exchange, symbol_config,
                                                                                            time_interval, run_time,
                                                                                            max_try_amount, candle_num,
                                                                                            symbol)

    return symbol_candle_data


# 根据最新数据，计算最新的signal
def calculate_signal(symbol_info, symbol_config, symbol_candle_data):
    """
    计算交易信号
    :param symbol_info:
    :param symbol_config:
    :param symbol_candle_data:
    :return:
    """

    # 输出变量
    symbol_signal = {}

    # 逐个遍历交易对
    for symbol in symbol_config.keys():

        # 赋值相关数据
        df = symbol_candle_data[symbol].copy()  # 最新数据
        now_pos = symbol_info.at[symbol, '持仓方向']  # 当前持仓方向
        # avg_price = symbol_info.at[symbol, '持仓均价']  # 当前持仓均价

        # 需要计算的目标仓位
        target_pos = None

        # 根据策略计算出目标交易信号。
        if not df.empty:  # 当原始数据不为空的时候
            # target_pos = getattr(Signals, symbol_config[symbol]['strategy_name'])(df, now_pos, avg_price,
            #                                                                       symbol_config[symbol]['para'])
            target_pos = getattr(Signals, symbol_config[symbol]['strategy_name'])(df,
                                                                                  para=symbol_config[symbol]['para'])
        symbol_info.at[symbol, '目标仓位'] = target_pos  # 这行代码似乎可以删除

        # 根据目标仓位和实际仓位，计算实际操作，"1": "开多"，"2": "开空"，"3": "平多"， "4": "平空"
        if now_pos == 1 and target_pos == 0:  # 平多
            symbol_signal[symbol] = [3]
        elif now_pos == -1 and target_pos == 0:  # 平空
            symbol_signal[symbol] = [4]
        elif now_pos == 0 and target_pos == 1:  # 开多
            symbol_signal[symbol] = [1]
        elif now_pos == 0 and target_pos == -1:  # 开空
            symbol_signal[symbol] = [2]
        elif now_pos == 1 and target_pos == -1:  # 平多，开空
            symbol_signal[symbol] = [3, 2]
        elif now_pos == -1 and target_pos == 1:  # 平空，开多
            symbol_signal[symbol] = [4, 1]

        symbol_info.at[symbol, '信号时间'] = datetime.now()  # 计算产生信号的时间

    return symbol_signal


# 在合约市场下单
def okex_future_place_order(exchange, symbol_info, symbol_config, symbol_signal, max_try_amount, symbol):
    """
    :param exchange:
    :param symbol_info:
    :param symbol_config:
    :param symbol_signal:
    :param max_try_amount:
    :param symbol:
    :return:
    """
    # 下单参数
    params = {
        'instId': symbol_config[symbol]["instrument_id"],  # 合约代码
        'tdMode': 'isolated',  # 设置为全仓,可以调整    isolated：逐仓    cross：全仓   cash：非保证金
        'ordType': 'limit',  # 设置为限价单
    }

    order_id_list = []
    # 按照交易信号下单
    for order_type in symbol_signal[symbol]:
        num = 0
        while True:
            try:
                response = float(
                    exchange.public_get_market_ticker({"instId": symbol_config[symbol]["instrument_id"]})['data'][0][
                        'last'])
                symbol_info.at[symbol, "信号价格"] = response
                # 当只要开仓或者平仓时，直接下单操作即可。但当本周期即需要平仓，又需要开仓时，需要在平完仓之后，
                # 重新评估下账户资金，然后根据账户资金计算开仓账户然后开仓。下面这行代码即处理这个情形。
                # "长度为2的判定"定位【平空，开多】或【平多，开空】两种情形，"下单类型判定"定位 处于开仓的情形。
                if len(symbol_signal[symbol]) == 2 and order_type in [1, 2]:  # 当两个条件同时满足时，说明当前处于平仓后，需要再开仓的阶段。
                    time.sleep(short_sleep_time)  # 短暂的休息1s，防止之平仓后，账户没有更新
                    _, symbol_info["账户余额"] = ccxt_fetch_future_account(exchange)

                # 确定下单参数
                params['side'] = 'buy' if order_type in [1, 4] else 'sell'
                params['px'] = float(cal_order_price(response, order_type))
                params['sz'] = int(cal_order_size(symbol, symbol_info, symbol_config[symbol]['leverage']))

                print('开始下单：', datetime.now())
                order_info = exchange.private_post_trade_order(params)
                ordId = order_info['data'][0]['ordId']
                print(order_info, '下单完成：', datetime.now())
                time.sleep(5)  # 等待三秒

                # 获取订单信息
                state = exchange.private_get_trade_order({'instId': symbol_config[symbol]["instrument_id"],
                                                          'ordId': ordId})['data'][0]['state']

                # 判断是否成交,如果没有成交撤销挂单,重新获取最新价格下单
                # canceled：撤单成功  live：等待成交  partially_filled：部分成交   filled：完全成交
                if state == 'live':
                    print('订单超过三秒未成交,重新获取价格下单')
                    exchange.private_post_trade_cancel_order(
                        {'instId': symbol_config[symbol]["instrument_id"], 'ordId': ordId})
                    if num >= max_try_amount:
                        send_dingding_msg('下单未成交次数超过max_try_amount，终止下单，程序不退出', robot_id, secret)
                        break
                    num += 1
                    time.sleep(2)
                    continue
                order_id_list.append(ordId)
                break

            except Exception as e:
                print(e)
                print(symbol, '下单失败，稍等后继续尝试')
                time.sleep(short_sleep_time)
                max_try_amount -= 1
                if max_try_amount <= 0:
                    print('下单失败次数超过max_try_amount，终止下单')
                    send_dingding_msg('下单失败次数超过max_try_amount，终止下单，程序不退出', robot_id, secret)
                    # exit() 若在子进程中（Pool）调用okex_future_place_order，触发exit会产生孤儿进程

    return symbol, order_id_list


# 串行下单
def single_threading_place_order(exchange, symbol_info, symbol_config, symbol_signal, max_try_amount=5):
    """
    :param exchange:
    :param symbol_info:
    :param symbol_config:
    :param symbol_signal:
    :param max_try_amount:
    :return:
    串行使用okex_future_place_order()函数，下单

    函数返回值案例：
                         symbol      信号价格                       信号时间
    4476028903965698  eth-usdt  227.1300 2020-03-01 11:53:00.580063
    4476028904156161  xrp-usdt    0.2365 2020-03-01 11:53:00.580558
    """
    # 函数输出变量
    symbol_order = pd.DataFrame()

    # 如果有交易信号的话
    if symbol_signal:
        # 遍历有交易信号的交易对
        for symbol in symbol_signal.keys():
            # 下单
            _, order_id_list = okex_future_place_order(exchange, symbol_info, symbol_config, symbol_signal,
                                                       max_try_amount, symbol)

            # 记录
            for order_id in order_id_list:
                symbol_order.loc[order_id, 'symbol'] = symbol
                # 从symbol_info记录下单相关信息
                symbol_order.loc[order_id, '信号价格'] = symbol_info.loc[symbol, '信号价格']
                symbol_order.loc[order_id, '信号时间'] = symbol_info.loc[symbol, '信号时间']

    return symbol_order


# 获取成交数据
def update_order_info(exchange, symbol_config, symbol_order, max_try_amount=5):
    """
    根据订单号，检查订单信息，获得相关数据
    :param exchange:
    :param symbol_config:
    :param symbol_order:
    :param max_try_amount:
    :return:

    函数返回值案例：
                             symbol      信号价格                       信号时间  订单状态 开仓方向 委托数量 成交数量    委托价格    成交均价                      委托时间
    4476028903965698  eth-usdt  227.1300 2020-03-01 11:53:00.580063  完全成交   开多  100  100  231.67  227.29  2020-03-01T03:53:00.896Z
    4476028904156161  xrp-usdt    0.2365 2020-03-01 11:53:00.580558  完全成交   开空  100  100  0.2317  0.2363  2020-03-01T03:53:00.906Z
    """

    # 下单数据不为空
    if symbol_order.empty is False:
        # 这个遍历下单id
        for order_id in symbol_order.index:
            time.sleep(medium_sleep_time)  # 每次获取下单数据时sleep一段时间
            order_info = None
            # 根据下单id获取数据
            for i in range(max_try_amount):
                try:
                    para = {
                        'instId': symbol_config[symbol_order.at[order_id, 'symbol']]["instrument_id"],
                        'ordId': order_id
                    }
                    order_info = exchange.private_get_trade_order(para)
                    break
                except Exception as e:
                    print(e)
                    print('根据订单号获取订单信息失败，稍后重试')
                    time.sleep(medium_sleep_time)
                    if i == max_try_amount - 1:
                        send_dingding_msg("重试次数过多，获取订单信息失败，程序退出")
                        raise ValueError('重试次数过多，获取订单信息失败，程序退出')

            if order_info:
                symbol_order.at[order_id, "订单状态"] = okex_order_state[order_info['data'][0]["state"]]
                symbol_order.at[order_id, "开仓方向"] = okex_order_type[order_info['data'][0]["posSide"]]
                symbol_order.at[order_id, "委托数量"] = order_info['data'][0]["sz"]
                symbol_order.at[order_id, "成交数量"] = order_info['data'][0]["accFillSz"]
                symbol_order.at[order_id, "委托价格"] = order_info['data'][0]["px"]
                symbol_order.at[order_id, "成交均价"] = order_info['data'][0]["avgPx"]
                symbol_order.at[order_id, "委托时间"] = pd.to_datetime(order_info['data'][0]["cTime"], unit='ms')
            else:
                print('根据订单号获取订单信息失败次数超过max_try_amount，发送钉钉')

    return symbol_order


# =====辅助功能函数
# ===下次运行时间，和课程里面讲的函数是一样的
def next_run_time(time_interval, ahead_seconds=5):
    """
    根据time_interval，计算下次运行的时间，下一个整点时刻。
    目前只支持分钟和小时。
    :param time_interval: 运行的周期，15m，1h
    :param ahead_seconds: 预留的目标时间和当前时间的间隙
    :return: 下次运行的时间
    案例：
    5m  当前时间为：12:33:51  返回时间为：12:35:00
    5m  当前时间为：12:34:51  返回时间为：12:40:00

    10m  当前时间为：12:38:51  返回时间为：12:40:00

    15m  当前时间为：12:50:51  返回时间为：13:00:00
    15m  当前时间为：12:39:51  返回时间为：12:45:00

    30m  当前时间为：21日的23:33:51  返回时间为：22日的00:00:00
    30m  当前时间为：14:37:51  返回时间为：14:56:00

    1h  当前时间为：14:37:51  返回时间为：15:00:00
    """

    if time_interval.endswith('m') or time_interval.endswith('h'):
        pass
    elif time_interval.endswith('T'):
        time_interval = time_interval.replace('T', 'm')
    elif time_interval.endswith('H'):
        time_interval = time_interval.replace('H', 'h')
    else:
        print('time_interval格式不符合规范。程序exit')
        exit()

    ti = pd.to_timedelta(time_interval)

    now_time = datetime.now()
    # print('现在时间为：%s'%now_time)
    # now_time = datetime(2019, 5, 9, 23, 50, 30)  # 修改now_time，可用于测试
    this_midnight = now_time.replace(hour=0, minute=0, second=0, microsecond=0)
    min_step = timedelta(minutes=1)

    target_time = now_time.replace(second=0, microsecond=0)

    while True:
        target_time = target_time + min_step
        # print('target_time: %s'%target_time)
        delta = target_time - this_midnight
        # print((target_time - now_time).seconds)
        # print(ahead_seconds) 
        if delta.seconds % ti.seconds == 0 and (target_time - now_time).seconds >= ahead_seconds:
            # 当符合运行周期，并且目标时间有足够大的余地，默认为60s
            break

    print('程序下次运行的时间：', target_time, '\n')
    return target_time


# ===获取全部历史数据
def fetch_okex_symbol_history_candle_data(exchange, symbol, time_interval, max_len, max_try_amount=5):
    """
    获取某个币种在okex交易所所有能获取的历史数据，目前v3接口最多获取1440根。
    :param exchange:
    :param symbol:
    :param time_interval:
    :param max_len:
    :param max_try_amount:
    :return:

    函数核心逻辑：
    1.找到最早那根K线的开始时间，以此为参数获取数据
    2.获取数据的最后一行数据，作为新的k线开始时间，继续获取数据
    3.如此循环直到最新的数据
    """

    # 获取当前时间
    now_milliseconds = int(time.time() * 1e3)

    # 每根K线的间隔时间
    time_interval_int = int(time_interval[:-1])  # 若15m，则time_interval_int = 15；若2h，则time_interval_int = 2
    if time_interval.endswith('m'):
        time_segment = time_interval_int * 60 * 1000  # 15分钟 * 每分钟60s
    elif time_interval.endswith('H'):
        time_segment = time_interval_int * 60 * 60 * 1000  # 2小时 * 每小时60分钟 * 每分钟60s

    # 计算开始和结束的时间
    since = now_milliseconds - time_segment
    end = since - max_len * time_segment

    # 循环获取历史数据
    all_kline_data = []
    while True:
        kline_data = []
        params = {
            'instId': symbol,
            'bar': time_interval,
            'after': since,
            'limit': '100'
        }

        # 获取K线使，要多次尝试
        for i in range(max_try_amount):
            try:
                kline_data = exchange.public_get_market_candles(params=params)['data']
                break
            except Exception as e:
                print(e)
                time.sleep(medium_sleep_time)
                if i == (max_try_amount - 1):
                    _ = '【获取需要交易币种的历史数据】阶段，fetch_okex_symbol_history_candle_data函数中，' \
                        '使用ccxt的fetch_ohlcv获取K线数据失败，程序Raise Error'
                    send_dingding_and_raise_error(_)

        if kline_data:
            if int(kline_data[-1][0]) < end:
                break
            since = kline_data[-1][0]  # 更新since，为下次循环做准备
            all_kline_data += kline_data
        else:
            print('【获取需要交易币种的历史数据】阶段，fetch_ohlcv失败次数过多，程序exit，请检查原因。')
            exit()

    # 对数据进行整理
    df = pd.DataFrame(all_kline_data, dtype=float)
    df.rename(columns={0: 'MTS', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace=True)
    df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms')
    df['candle_begin_time_GMT8'] = df['candle_begin_time'] + timedelta(hours=8)
    df = df[['candle_begin_time_GMT8', 'open', 'high', 'low', 'close', 'volume']]

    # 删除重复的数据
    df.drop_duplicates(subset=['candle_begin_time_GMT8'], keep='last', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # 为了保险起见，去掉最后一行最新的数据
    df = df[:-1]

    print(symbol, '获取历史数据行数：', len(df))

    return df


# ===依据时间间隔, 自动计算并休眠到指定时间
def sleep_until_run_time(time_interval, ahead_time=1):
    """
    根据next_run_time()函数计算出下次程序运行的时候，然后sleep至该时间
    :param time_interval:
    :param ahead_time:
    :return:
    """
    # 计算下次运行时间
    run_time = next_run_time(time_interval, ahead_time)
    # sleep
    time.sleep(max(0, (run_time - datetime.now()).seconds))
    while True:  # 在靠近目标时间时
        if datetime.now() > run_time:
            break

    return run_time


# ===在每个循环的末尾，编写报告并且通过订订发送
def dingding_report_every_loop(symbol_info, symbol_signal, symbol_order, run_time, robot_id_secret):
    """
    :param symbol_info:
    :param symbol_signal:
    :param symbol_order:
    :param run_time:
    :param robot_id_secret:
    :return:
    """
    content = ''

    # 订单信息
    if symbol_signal:
        symbol_order_str = ['\n\n' + y.to_string() for x, y in symbol_order.iterrows()]  # 持仓信息
        content += '# =====订单信息' + ''.join(symbol_order_str) + '\n\n'

    # 持仓信息
    symbol_info_str = ['\n\n' + str(x) + '\n' + y.to_string() for x, y in symbol_info.iterrows()]
    content += '# =====持仓信息' + ''.join(symbol_info_str) + '\n\n'

    # 发送，每间隔30分钟或者有交易的时候，发送一次
    if run_time.minute % 30 == 0 or symbol_signal:
        send_dingding_msg(content, robot_id, secret)


# ===为了达到成交的目的，计算实际委托价格会向上或者向下浮动一定比例默认为0.02
def cal_order_price(price, order_type, ratio=0.02):
    if order_type in [1, 4]:
        return price * (1 + ratio)
    elif order_type in [2, 3]:
        return price * (1 - ratio)


# ===计算实际开仓张数
def cal_order_size(symbol, symbol_info, leverage, volatility_ratio=0.98):
    """
    根据实际持仓以及杠杆数，计算实际开仓张数
    :param symbol:
    :param symbol_info:
    :param leverage:
    :param volatility_ratio:
    :return:
    """
    # 当账户目前有持仓的时候，必定是要平仓，所以直接返回持仓量即可
    hold_amount = symbol_info.at[symbol, "持仓量"]
    if pd.notna(hold_amount):  # 不为空
        return abs(hold_amount)

    # 当账户没有持仓时，是开仓
    price = float(symbol_info.at[symbol, "信号价格"])
    coin_value = coin_value_table[symbol]
    e = float(symbol_info.loc[symbol, "账户余额"])
    # 不超过账户最大杠杆
    l = min(float(leverage), float(symbol_info.at[symbol, "最大杠杆"]))
    size = math.floor(e * l * volatility_ratio / (price * coin_value))
    return max(size, 1)  # 防止出现size为情形0，设置最小下单量为1


# ===发送钉钉相关函数
# 计算钉钉时间戳
def cal_timestamp_sign(secret):
    # 根据钉钉开发文档，修改推送消息的安全设置https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
    # 也就是根据这个方法，不只是要有robot_id，还要有secret
    # 当前时间戳，单位是毫秒，与请求调用时间误差不能超过1小时
    # python3用int取整
    timestamp = int(round(time.time() * 1000))
    # 密钥，机器人安全设置页面，加签一栏下面显示的SEC开头的字符串
    secret_enc = bytes(secret.encode('utf-8'))
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = bytes(string_to_sign.encode('utf-8'))
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    # 得到最终的签名值
    sign = parse.quote_plus(base64.b64encode(hmac_code))
    return str(timestamp), str(sign)


# 发送钉钉消息
def send_dingding_msg(content, robot_id='',
                      secret=''):
    """
    :param content:
    :param robot_id:  你的access_token，即webhook地址中那段access_token。例如如下地址：https://oapi.dingtalk.com/robot/
n    :param secret: 你的secret，即安全设置加签当中的那个密钥
    :return:
    """
    try:
        msg = {
            "msgtype": "text",
            "text": {"content": content + '\n' + '（发送时间：' + datetime.now().strftime("%m-%d %H:%M:%S") + '）' }}
        
        headers = {"Content-Type": "application/json;charset=utf-8"}

        # https://oapi.dingtalk.com/robot/send?access_token=XXXXXX&timestamp=XXX&sign=XXX
        timestamp, sign_str = cal_timestamp_sign(secret)
        url = 'https://oapi.dingtalk.com/robot/send?access_token=' + robot_id + \
              '&timestamp=' + timestamp + '&sign=' + sign_str
        body = json.dumps(msg)
        r = requests.post(url, data=body, headers=headers, timeout=10)
        print(r.text)
        print('成功发送钉钉')
    except Exception as e:
        print("发送钉钉失败:", e)


# price 价格 money 资金量 leverage 杠杆 ratio 最小变动单位
def calculate_max_size(price, money, leverage, ratio):
    return math.floor(money * leverage / price / ratio)


def send_dingding_and_raise_error(content):
    print(content)
    send_dingding_msg(content, robot_id, secret)
    raise ValueError(content)
