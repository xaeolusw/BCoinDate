import pandas as pd
import os
from datetime import timedelta
from Signals import *
from Position import *
from Evaluate import *
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# =====手工设定策略参数
symbol = 'BTCUSDT'
para = [360, 3]

face_value = 0.01  # btc是0.01，不同的币种要进行不同的替换
c_rate = 5 / 10000  # 手续费，commission fees，默认为万分之5。不同市场手续费的收取方法不同，对结果有影响。比如和股票就不一样。
slippage = 1 / 1000  # 滑点 ，可以用百分比，也可以用固定值。建议币圈用百分比，股票用固定值
leverage_rate = 3  # 交易所的杠杆倍数。
min_margin_ratio = 1 / 100  # 最低保证金率，低于就会爆仓
rule_type = '1d'
drop_days = 10  # 币种刚刚上线10天内不交易


# =====读入数据
if os.name == 'nt':
    df = pd.read_hdf('D:\\PythonProjects\\coin_data\\binance_%s_%s.h5'%(symbol,rule_type), key='%s_%s'% (symbol, rule_type))
elif os.name == 'posix':
    df = pd.read_hdf('/Volumes/USB-DISK/PythonProjects/coin_data/binance_%s_%s.h5'%(symbol,rule_type), key='%s_%s'% (symbol, rule_type))
else:
    print('操作系统不支持')
    exit()

# 任何原始数据读入都进行一下排序、去重，以防万一
df.sort_values(by=['candle_begin_time'], inplace=True) # type: ignore
df.drop_duplicates(subset=['candle_begin_time'], inplace=True) # type: ignore
df.reset_index(inplace=True, drop=True)

# =====计算交易信号
print(para)
df = df[df['candle_begin_time'] >= pd.to_datetime('2020-01-01')]
df.reset_index(inplace=True, drop=True)

df = signal_simple_primeCost(df, para=[20, 60])

# df = signal_simple_bolling(df, para=para)


# =====计算实际持仓
df = position_for_OKEx_future(df)


# =====计算资金曲线
# 选取相关时间。币种上线10天之后的日期
# t = df.iloc[0]['candle_begin_time'] + timedelta(days=drop_days)       #在此处选取不合理，应该在生成signal前选取
# df = df[df['candle_begin_time'] > t]

# 计算资金曲线
df = equity_curve_for_OKEx_USDT_future_next_open(df, slippage=slippage, c_rate=c_rate, leverage_rate=leverage_rate,
                                                        face_value=face_value, min_margin_ratio=min_margin_ratio)


print('策略最终收益：', df.iloc[-1]['equity_curve'])

if os.name == 'nt':
    path = 'D:\\PythonProjects\\coin_data\\%s_%s_equity_curve.h5'%(symbol,rule_type)
elif os.name == 'posix':
    path = '/Volumes/USB-DISK/PythonProjects/coin_data/%s_%s_equity_curve.h5'%(symbol,rule_type)
else:
    print('操作系统不支持')
    exit()

# df.to_hdf(path, key='df', mode='w')
df.to_csv(path[:-2]+'csv') #将数据存入csv文件中,方便查看
print('生成资金曲线文件成功，文件名为%s'%path)
