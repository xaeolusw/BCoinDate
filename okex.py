import pandas as pd
import ccxt
import time
import os
from datetime import timedelta

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# =====设定参数
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

okex = ccxt.okex5({
    'proxies': proxies
})

# =====获取产品行情数据
params = {
    'instType': 'SPOT', #SPOT：币币;SWAP：永续合约;FUTURES：交割合约;OPTION：期权
    #'uly': 'BTC-USDT', #标的指数,适用于交割/永续/期权，如 BTC-USD
    #'instFamily': 'BTC-USD', #交易品种.适用于交割/永续/期权，如 BTC-USD          
} 

tickers = okex.publicGetMarketTickers(params=params)
print(tickers)