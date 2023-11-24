import ccxt
import os
import pandas as pd

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
    global_database_path = 'getKlinesDatabase.csv'
    global_file_path = 'D:\\PythonProjects\\coin_data'
elif os.name == 'posix':
    global_database_path = '/Users/aeolus/同步空间/PythonProjects/BCoinDate/creat_date/getKlinesDatabase.csv'
    global_file_path = '/Volumes/USB-DISK/PythonProjects/coin_data'
else:
    print('操作系统不支持')
    exit()

global_error_list = []

global_binance_symbol_list = []  # 'BTCUSDT','ETHUSDT','EOSUSDT','LTCUSDT'
global_okx_symbol_list = []  # 'BTC-USDT','ETH-USDT','EOS-USDT','LTC-USDT'

global_okx_instType_list = ['SWAP', 'FUTURES']  # SPOT：币币;SWAP：永续合约;FUTURES：交割合约;OPTION：期权
global_okx_uly_list = ['BTC-USDT', 'BTC-USD']

global_instType = 'SPOT'

# 从csv文件中读取初始数据
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
df = pd.read_csv(
    filepath_or_buffer=global_database_path,
    encoding='utf8',
    sep=',',
)

global_time_interval_list = []  # 其他可以尝试的值：'1m', '5m', '15m', '30m', '1H', '2H', '1D', '1W', '1M', '1Y'
for symbol in df['symbol']:
    global_binance_symbol_list.append(symbol + 'USDT')
    global_okx_symbol_list.append(symbol + '-USDT')

for interval in df['interval']:
    if interval != '0':
        global_time_interval_list.append(interval)

global_start_time = df['start_time'][0]
global_end_time = df['end_time'][0]
global_update_time = df['update_time'][0]

