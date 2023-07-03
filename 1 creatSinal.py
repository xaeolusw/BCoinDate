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

# =====读入数据(除首次外使用)
# symbol = 'BTCUSDT'
if os.name == 'nt':
    df = pd.read_hdf(r'D:\\PythonProjects\\BCoinDate\\data\\binance_BTCUSDT_5m.h5', key='BTCUSDT_5m')
elif os.name == 'posix':
    df = pd.read_hdf(r'/Volumes/USB-DISK/PythonProjects/coin_data/binance_BTCUSDT_15m.h5', key='BTCUSDT_15m')
else:
    print('操作系统不支持')
    exit()

# ==计算指标
n = 400
m = 2
# 计算均线
df['median'] = df['close'].rolling(n, min_periods=1).mean()

# 计算上轨、下轨道
df['std'] = df['close'].rolling(n, min_periods=1).std(ddof=0)  # ddof代表标准差自由度
df['upper'] = df['median'] + m * df['std']
df['lower'] = df['median'] - m * df['std']

# ==计算信号
# 找出做多信号
condition1 = df['close'] > df['upper']  # 当前K线的收盘价 > 上轨
condition2 = df['close'].shift(1) <= df['upper'].shift(1)  # 之前K线的收盘价 <= 上轨
df.loc[condition1 & condition2, 'signal_long'] = 1  # 将产生做多信号的那根K线的signal设置为1，1代表做多

# 找出做多平仓信号
condition1 = df['close'] < df['median']  # 当前K线的收盘价 < 中轨
condition2 = df['close'].shift(1) >= df['median'].shift(1)  # 之前K线的收盘价 >= 中轨
df.loc[condition1 & condition2, 'signal_long'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

# 找出做空信号
condition1 = df['close'] < df['lower']  # 当前K线的收盘价 < 下轨
condition2 = df['close'].shift(1) >= df['lower'].shift(1)  # 之前K线的收盘价 >= 下轨
df.loc[condition1 & condition2, 'signal_short'] = -1  # 将产生做空信号的那根K线的signal设置为-1，-1代表做空

# 找出做空平仓信号
condition1 = df['close'] > df['median']  # 当前K线的收盘价 > 中轨
condition2 = df['close'].shift(1) <= df['median'].shift(1)  # 之前K线的收盘价 <= 中轨
df.loc[condition1 & condition2, 'signal_short'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

# 合并做多做空信号，去除重复信号
df['signal'] = df[['signal_long', 'signal_short']].sum(axis=1, min_count=1, skipna=True)
temp = df[df['signal'].notnull()][['signal']]
temp = temp[temp['signal'] != temp['signal'].shift(1)]
df['signal'] = temp['signal']

# ==删除无关变量
df.drop(['median', 'std', 'upper', 'lower', 'signal_long', 'signal_short','quote_asset_volume'], axis=1, inplace=True)
print(df)
# df = df[df['signal'].isna() == False]   #为什么不删除空值？编写资金曲线时需要所有的数据，包括空值

# =====将数据存入hdf文件中
# df.to_csv('/Volumes/USB-DISK/PythonProjects/coin_data/signals.csv', index=False)
if os.name == 'nt':
    df.to_hdf(r'D:\\PythonProjects\\BCoinDate\\data\\signals.h5', key='df', mode='w')
elif os.name == 'posix':
    df.to_hdf(r'/Volumes/USB-DISK/PythonProjects/coin_data/signals.h5', key='df', mode='w')
else:
    print('操作系统不支持')
    exit()
