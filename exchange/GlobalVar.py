import os
import ccxt
import pandas as pd
from Config import *

pd.set_option('display.max_rows', 1000)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
# 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

#根据操作系统设置数据库路径
if os.name == 'nt':
    global_database_path = 'D:\\PythonProjects\\coin_data\\getKey.csv'
elif os.name == 'posix':
    global_database_path = '/Volumes/USB-DISK/PythonProjects/coin_data/getKey.csv'
else:
    print('操作系统不支持')
    exit()

df_key = pd.read_csv(
    filepath_or_buffer = global_database_path, 
    encoding='utf8', 
    sep=',',
) 

# =钉钉
# 在一个钉钉群中，可以创建多个钉钉机器人。
# 建议单独建立一个报错机器人，该机器人专门发报错信息。请务必将报错机器人在id和secret放到function.send_dingding_msg的默认参数中。
robot_id = df_key['robot_id'][0]
secret = df_key['robot_secret'][0] 
robot_id_secret = [robot_id, secret]

# =交易所配置
OKEX_CONFIG = {
    'proxies': {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    },
    'apiKey': df_key['apiKey'][0],
    'secret': df_key['api_secret'][0],
    'password': df_key['password'][0],
    'timeout': exchange_timeout,
    'rateLimit': 10,
    # 'hostname': 'okex.me',  # 无法fq的时候启用
    'enableRateLimit': False}

# 测试时ccxt版本为1.27.28。若不是此版本，可能会报错，可能性很低。print(ccxt.__version__)可以查看ccxt版本。
exchange = ccxt.okex(OKEX_CONFIG)