import pandas as pd
import os
from datetime import timedelta
from Signals import *
from Position import *
from Evaluate import *
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# =====手工设定策略参数
symbol = 'BTCUSDT'
para = [1000, 2]

face_value = 0.01  # btc是0.01，不同的币种要进行不同的替换
c_rate = 5 / 10000  # 手续费，commission fees，默认为万分之5。不同市场手续费的收取方法不同，对结果有影响。比如和股票就不一样。
slippage = 1 / 1000  # 滑点 ，可以用百分比，也可以用固定值。建议币圈用百分比，股票用固定值
leverage_rate = 3  # 交易所的杠杆倍数。
min_margin_ratio = 1 / 100  # 最低保证金率，低于就会爆仓
rule_type = '15T'
drop_days = 10  # 币种刚刚上线10天内不交易


# =====读入数据
if os.name == 'nt':
    df = pd.read_hdf(r'D:\PythonProjects\BCoinDate\data\binance_BTCUSDT_5m.h5', key='BTCUSDT_15m')
elif os.name == 'posix':
    df = pd.read_hdf(r'/Volumes/USB-DISK/PythonProjects/coin_data/binance_BTCUSDT_15m.h5', key='BTCUSDT_15m')
else:
    print('操作系统不支持')
    exit()


# # 任何原始数据读入都进行一下排序、去重，以防万一
# # df = df[df['candle_begin_time'] >= pd.to_datetime('2023-01-01')]
# df.sort_values(by=['candle_begin_time'], inplace=True)
# df.drop_duplicates(subset=['candle_begin_time'], inplace=True)
# df.reset_index(inplace=True, drop=True)


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

listDf = pd.DataFrame(["para", "equity_curve"])
# =====计算交易信号
for i in range(1, 100):
    for j in range(1, 3):
        para = [i * 10, j]
        print(para)
        # listDf["para"] = para
        df = signal_simple_bolling(df, para=para)


        # =====计算实际持仓
        df = position_for_OKEx_future(df)


        # =====计算资金曲线
        # 选取相关时间。币种上线10天之后的日期
        t = df.iloc[0]['candle_begin_time'] + timedelta(days=drop_days)
        df = df[df['candle_begin_time'] > t]
        # 计算资金曲线
        df = equity_curve_for_OKEx_USDT_future_next_open(df, slippage=slippage, c_rate=c_rate, leverage_rate=leverage_rate,
                                                        face_value=face_value, min_margin_ratio=min_margin_ratio)
        # print(df)
        print('策略最终收益：', df.iloc[-1]['equity_curve'])
        # listDf["equity_curve"] = df.iloc[-1]['equity_curve']

