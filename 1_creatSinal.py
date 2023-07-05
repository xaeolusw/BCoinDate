import pandas as pd
import os
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# =====产生交易信号：布林线策略
# 布林线策略
# 布林线中轨：n天收盘价的移动平均线                                 #20周期简单移动平均线（SMA）
# 布林线上轨：n天收盘价的移动平均线 + m * n天收盘价的标准差
# 布林线上轨：n天收盘价的移动平均线 - m * n天收盘价的标准差
# 当收盘价由下向上穿过上轨的时候，做多；然后由上向下穿过中轨的时候，平仓。
# 当收盘价由上向下穿过下轨的时候，做空；然后由下向上穿过中轨的时候，平仓。

# =====读入数据
# symbol = 'BTCUSDT'
# if os.name == 'nt':
#     path = 'D:\\PythonProjects\\BCoinDate\\data\\binance_%s_15m.h5'%symbol
# elif os.name == 'posix':
#     path = '/Volumes/USB-DISK/PythonProjects/coin_data/binance_%s_15m.h5'%symbol
# else:
#     print('操作系统不支持')
#     exit()

if os.name == 'nt':
    path = 'D:\\PythonProjects\\coin_data\\binance_BTCUSDT_15m.h5'
elif os.name == 'posix':
    path = '/Volumes/USB-DISK/PythonProjects/coin_data/binance_BTCUSDT_15m.h5'
else:
    print('操作系统不支持')
    exit()

df = pd.read_hdf(path, key='BTCUSDT_15m')

# ==计算指标
n = 400
m = 2
# 计算均线
df['median'] = df['close'].rolling(n, min_periods=1).mean() #min_periods=1代表最小周期为1时也进行计算;！！！默认 min_periods=1，我将其改为n，即最小周期为n时才进行计算

# 计算上轨、下轨道
df['std'] = df['close'].rolling(n, min_periods=1).std(ddof=0)  # ddof代表标准差自由度。！！！默认 min_periods=1，我将其改为n，即最小周期为n时才进行计算
df['upper'] = df['median'] + m * df['std']
df['lower'] = df['median'] - m * df['std']

# ==计算信号
# 找出做多信号（上穿上轨）
condition1 = df['close'] > df['upper']  # 当前K线的收盘价 > 上轨
condition2 = df['close'].shift(1) <= df['upper'].shift(1)  # 上一条K线的收盘价 <= 上轨
df.loc[condition1 & condition2, 'signal_long'] = 1  # 将产生做多信号的那根K线的signal设置为1，1代表做多

# 找出做多平仓信号（下穿中轨）
condition1 = df['close'] < df['median']  # 当前K线的收盘价 < 中轨
condition2 = df['close'].shift(1) >= df['median'].shift(1)  # 上一条K线的收盘价 >= 中轨
df.loc[condition1 & condition2, 'signal_long'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

# 找出做空信号（下穿下轨）
condition1 = df['close'] < df['lower']  # 当前K线的收盘价 < 下轨
condition2 = df['close'].shift(1) >= df['lower'].shift(1)  # 上一条K线的收盘价 >= 下轨
df.loc[condition1 & condition2, 'signal_short'] = -1  # 将产生做空信号的那根K线的signal设置为-1，-1代表做空

# 找出做空平仓信号（上穿中轨）
condition1 = df['close'] > df['median']  # 当前K线的收盘价 > 中轨
condition2 = df['close'].shift(1) <= df['median'].shift(1)  # 上一条K线的收盘价 <= 中轨
df.loc[condition1 & condition2, 'signal_short'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

# 合并做多做空信号，去除重复信号
df['signal'] = df[['signal_long', 'signal_short']].sum(axis=1, min_count=1, skipna=True)
temp = df[df['signal'].notnull()][['signal']]
temp = temp[temp['signal'] != temp['signal'].shift(1)]
df['signal'] = temp['signal']

# ==删除无关变量
df.drop(['median', 'std', 'upper', 'lower', 'signal_long', 'signal_short','volume','quote_asset_volume'], axis=1, inplace=True)
# print(df)

# df = df[df['signal'].isna() == False]   #为什么不删除空值？编写资金曲线时需要所有的数据，包括空值

# =====将数据存入hdf文件中
# if os.name == 'nt':
#     path = 'D:\\PythonProjects\\BCoinDate\\data\\%s_signals.h5'%symbol
# elif os.name == 'posix':
#     path = '/Volumes/USB-DISK/PythonProjects/coin_data/%s_signals.h5'%symbol
# else:
#     print('操作系统不支持')
#     exit()

if os.name == 'nt':
    path = 'D:\\PythonProjects\\coin_data\\BTCUSDT_signals.h5'
elif os.name == 'posix':
    path = '/Volumes/USB-DISK/PythonProjects/coin_data/BTCUSDT_signals.h5'
else:
    print('操作系统不支持')
    exit()

df.to_hdf(path, key='df', mode='w')
df.to_csv(path[:-2]+'csv') #将数据存入csv文件中,方便查看
print('生成信号文件成功，文件名为%s'%path)