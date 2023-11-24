import pandas as pd
import os
from datetime import timedelta
from Signals import *
from Position import *
from Evaluate import *
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# =====参数设定
# 手工设定策略参数
symbol = 'BTCUSDT'

if symbol == 'BTCUSDT':
    face_value = 0.01  # btc是0.01，不同的币种要进行不同的替换;ETH是0.1
elif symbol == 'ETHUSDT':
    face_value = 0.1
else:
    face_value = 0.1
c_rate = 5 / 10000  # 手续费，commission fees，默认为万分之5。不同市场手续费的收取方法不同，对结果有影响。比如和股票就不一样。
slippage = 1 / 1000  # 滑点 ，可以用百分比，也可以用固定值。建议币圈用百分比，股票用固定值
leverage_rate = 3   ## 交易所的杠杆倍数。
min_margin_ratio = 1 / 100  # 最低保证金率，低于就会爆仓
rule_type = '15T'
drop_days = 10  # 币种刚刚上线10天内不交易


# =====读入数据
if os.name == 'nt':
    df = pd.read_hdf('D:\\PythonProjects\\coin_data\\binance_%s_15m.h5'%symbol, key='%s_15m'%symbol)
elif os.name == 'posix':
    df = pd.read_hdf('/Volumes/USB-DISK/PythonProjects/coin_data/binance_%s_15m.h5'%symbol, key='%s_15m'%symbol)
else:
    print('操作系统不支持')
    exit()

# 任何原始数据读入都进行一下排序、去重，以防万一
df.sort_values(by=['candle_begin_time'], inplace=True)
df.drop_duplicates(subset=['candle_begin_time'], inplace=True)
df.reset_index(inplace=True, drop=True)


# # =====转换为其他分钟数据
# rule_type = '15T'
# period_df = df.resample(rule=rule_type, on='candle_begin_time', label='left', closed='left').agg(
#     {'open': 'first',
#      'high': 'max',
#      'low': 'min',
#      'close': 'last',
#      'volume': 'sum',
#      'quote_asset_volume': 'sum',
#      })
# period_df.dropna(subset=['open'], inplace=True)  # 去除一天都没有交易的周期
# period_df = period_df[period_df['volume'] > 0]  # 去除成交量为0的交易周期
# period_df.reset_index(inplace=True)
# df = period_df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume', 'quote_asset_volume']]
# df = df[df['candle_begin_time'] >= pd.to_datetime('2017-01-01')]
# df.reset_index(inplace=True, drop=True)


# =====获取策略参数组合
para_list = signal_simple_bolling_para_list()


# =====遍历参数
rtn = pd.DataFrame()
for para in para_list:
    _df = df.copy()

    # 选取相关时间。币种上线10天之后的日期
    # t = _df.iloc[0]['candle_begin_time'] + timedelta(days=drop_days)
    # _df = _df[_df['candle_begin_time'] > t]

    # 计算交易信号
    _df = signal_simple_bolling(_df, para=para)
    # 计算实际持仓
    _df = position_for_OKEx_future(_df)
    # 计算资金曲线
    # 选取相关时间。币种上线10天之后的日期  # #在此处选取不合理，应该在生成signal前选取！！！
    # t = _df.iloc[0]['candle_begin_time'] + timedelta(days=drop_days)
    # _df = _df[_df['candle_begin_time'] > t]
    # 计算资金曲线
    _df = equity_curve_for_OKEx_USDT_future_next_open(_df, slippage=slippage, c_rate=c_rate, leverage_rate=leverage_rate,
                                                      face_value=face_value, min_margin_ratio=min_margin_ratio)
    # 计算收益
    r = _df.iloc[-1]['equity_curve']
    print(para, '策略最终收益：', r)
    rtn.loc[str(para), 'equity_curve'] = r

# =====输出
# rtn.sort_values(by='equity_curve', ascending=False, inplace=True)
# print(rtn)

if os.name == 'nt':
    path = 'D:\\PythonProjects\\coin_data\\%s.csv'%symbol
elif os.name == 'posix':
    path = '/Volumes/USB-DISK/PythonProjects/coin_data/%s.csv'%symbol
else:
    print('操作系统不支持')
    exit()

rtn.to_csv(path) #将数据存入csv文件中,方便查看
print('生成资金曲线文件成功，文件名为%s'%path)