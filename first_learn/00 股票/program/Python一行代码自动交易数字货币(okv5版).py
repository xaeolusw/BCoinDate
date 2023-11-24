"""
更新时间：2021-10-08
《邢不行|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

介绍数字货币如何自动交易
"""
import ccxt
import time

# ===获取行情数据
# 申明okex交易所
#exchange = ccxt.okex5()

# 获取最新的ticker数据，运行需要翻墙，btc、ltc
#data = exchange.fetchTicker(symbol='BTC/USDT')
# 获取最新的K线数据：日线、小时线
# data = exchange.fetch_ohlcv(symbol='BTC/USDT', timeframe='1h', limit=50)  # '1h'，'1d'

# 获取币安交易所的相关数据
exchange = ccxt.binance({
    'proxies':{
        "http":'127.0.0.1:7890',
        "https":'127.0.0.1:7890',
    }
    }
)

data = exchange.fetch_ticker(symbol='BTC/USDT')
print(f"交易对：{data['symbol']}")
print(f"时间：{data['datetime']}")
print(f"买一价为： {data['bid']}")

print(data['info']['symbol'])
print(data['info']['lastPrice'])
print(data['info']['quoteVolume'])
#例子：{'symbol': 'BTC/USDT', 'timestamp': 1681368812986, 'datetime': '2023-04-13T06:53:32.986Z', 'high': 30486.0, 'low': 29637.4, 'bid': 30005.35, 'bidVolume': 6.91078, 'ask': 30005.36, 'askVolume': 8.64344, 'vwap': 30041.73180819, 'open': 29936.98, 'close': 30005.36, 'last': 30005.36, 'previousClose': 29936.99, 'change': 68.38, 'percentage': 0.228, 'average': 29971.17, 'baseVolume': 54698.16049, 'quoteVolume': 1643227467.842028, 'info': {'symbol': 'BTCUSDT', 'priceChange': '68.38000000', 'priceChangePercent': '0.228', 'weightedAvgPrice': '30041.73180819', 'prevClosePrice': '29936.99000000', 'lastPrice': '30005.36000000', 'lastQty': '0.06978000', 'bidPrice': '30005.35000000', 'bidQty': '6.91078000', 'askPrice': '30005.36000000', 'askQty': '8.64344000', 'openPrice': '29936.98000000', 'highPrice': '30486.00000000', 'lowPrice': '29637.40000000', 'volume': '54698.16049000', 'quoteVolume': '1643227467.84202780', 'openTime': '1681282412986', 'closeTime': '1681368812986', 'firstId': '3078445428', 'lastId': '3079580598', 'count': '1135171'}}
#{'symbol', 'timestamp', 'datetime' , 'high', 'low', 'bid', 'bidVolume', 'ask', 'askVolume', 'vwap', 'open', 'close', 'last', 'previousClose', 'change', 'percentage',
# 'average', 'baseVolume', 'quoteVolume',
# 'info': {'symbol': 'BTCUSDT', 'priceChange': '68.38000000', 'priceChangePercent': '0.228', 'weightedAvgPrice': '30041.73180819', 'prevClosePrice': '29936.99000000', 'lastPrice': '30005.36000000', 'lastQty': '0.06978000', 'bidPrice': '30005.35000000', 'bidQty': '6.91078000', 'askPrice': '30005.36000000', 'askQty': '8.64344000', 'openPrice': '29936.98000000', 'highPrice': '30486.00000000', 'lowPrice': '29637.40000000', 'volume': '54698.16049000', 'quoteVolume': '1643227467.84202780', 'openTime': '1681282412986', 'closeTime': '1681368812986', 'firstId': '3078445428', 'lastId': '3079580598', 'count': '1135171'}}

#K线数据
data2 = exchange.fetch_ohlcv(symbol='BTC/USDT', timeframe='1h', limit=50) #timeframe 时间，limit 条数；结果：时间、开盘价、最高价、最低价、收盘价、交易量
print(data2)
# print(data2['symbol'])
# print(data2['datetime'])
# print(data2['last'])
#
# print(data2['info']['symbol'])
# print(data2['info']['lastPrice'])
# print(data2['info']['quoteVolume'])


# ===下单交易
# 申明币安交易所
#exchange = ccxt.binance()
# 填写API秘钥
#exchange.apiKey = ''
#exchange.secret = ''

# 获取账户余额
#balance = exchange.fetch_balance()

# 限价单卖出：交易对、买卖数量、价格。如何买？
# order_info = exchange.create_limit_sell_order('BTC/USDT', 0.01, 13000)

# 撤单
# order_info = exchange.cancel_order(id='486207276', symbol='BTC/USDT')

# ===完整案例程序1：反复下单、撤单
# while True:
#     order_info = exchange.create_limit_sell_order('BTC/USDT', 0.01, 14000)
#     print('下单完成')
#     time.sleep(2)
#     order_info = exchange.cancel_order(id=order_info['id'], symbol='BTC/USDT')
#     print('撤单完成')
#     time.sleep(2)


# # ===完整案例程序2：实时监测价格达到止损条件后，卖出止损
# while True:
#     # 获取最新价格数据
#     data = exchange.fetchTicker(symbol='BTC/USDT')
#     new_price = data['bid']
#     print('最新买一价格：', new_price)
#
#     # 判断是否交易
#     if new_price < 10000:
#         # 下单卖出，止损
#         order_info = exchange.create_market_sell_order('BTC/USDT', 0.01)
#         print('达到止损价，下单卖出。', new_price)
#         break
#     else:
#         print('价格未达止损价，5s后继续监测\n')
#         time.sleep(5)

# ===实盘量化程序流程
# 1. 通过行情接口，获取实时数据
# 2. 根据策略处理数据，产生交易信号
# 3. 根据交易信号实际下单。
