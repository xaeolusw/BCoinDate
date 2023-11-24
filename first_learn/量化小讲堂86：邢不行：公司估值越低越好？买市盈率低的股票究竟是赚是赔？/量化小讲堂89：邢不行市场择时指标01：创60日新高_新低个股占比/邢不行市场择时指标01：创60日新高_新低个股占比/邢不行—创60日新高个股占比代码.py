"""
邢不行-创60日新高个股占比代码
邢不行微信：xbx971
相关网址：
创60日新高个股占比：https://www.quantclass.cn/service/stock/strategy/macro/stock-market-ltma20
创60日新低个股占比：https://www.quantclass.cn/service/stock/strategy/macro/stock-market-ltmi20
"""

import os
import pandas as pd

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# 输入下载数据的路径名
file_path = r'邢不行历史日线数据'

# 起始日期
start_time = '20070101'
end_time = '20221231'

# 价格复权
def rehabilitation(df):
    # 计算涨跌幅
    df['涨跌幅'] = df['收盘价'] / df['前收盘价'] - 1
    # =计算复权价：计算所有因子当中用到的价格，都使用复权价
    df['复权因子'] = (1 + df['涨跌幅']).cumprod()
    df['收盘价_复权'] = df['复权因子'] * (df.iloc[0]['收盘价'] / df.iloc[0]['复权因子'])
    df['开盘价_复权'] = df['开盘价'] / df['收盘价'] * df['收盘价_复权']
    df['最高价_复权'] = df['最高价'] / df['收盘价'] * df['收盘价_复权']
    df['最低价_复权'] = df['最低价'] / df['收盘价'] * df['收盘价_复权']
    # 原始的价格叫xx_原，复权两个字去掉
    df.rename({'开盘价': '开盘价_原', '最高价': '最高价_原', '最低价': '最低价_原', '收盘价': '收盘价_原'}, inplace=True)
    df.rename({'开盘价_复权': '开盘价', '最高价_复权': '最高价', '最低价_复权': '最低价', '收盘价_复权': '收盘价'}, inplace=True)
    return df

# 获取文件夹下的所有csv文件
file_list = os.listdir(file_path)
file_list = [f for f in file_list if '.csv' in f]

# 如需知道某个股票的指标信号和数值，可使用下方代码
# file_list = ['sz300750.csv']

dfs = []
for f in file_list:
    print(f)
    # 加载数据
    df = pd.read_csv(os.path.join(file_path, f), encoding='gbk', parse_dates=['交易日期'])
    df = rehabilitation(df)
    dfs.append(df)
all_df = pd.concat(dfs, ignore_index=True)

# 规定时间段
all_df = all_df[all_df['交易日期'] >= pd.to_datetime(start_time)]
all_df = all_df[all_df['交易日期'] <= pd.to_datetime(end_time)]

# 如需计算指数，可用
# all_df = all_df.loc[all_df['沪深300成分股']=='Y']
# all_df = all_df.loc[all_df['上证50成分股']=='Y']
# all_df = all_df.loc[all_df['创业板指成分股']=='Y']
# all_df = all_df.loc[all_df['中证500成分股']=='Y']

n = 60
df_new = pd.DataFrame()
all_df['signal'] = 0

# 计算今日前59日最高价
all_df['前日最高价'] = all_df['最高价'].shift(1)
all_df.loc[all_df['最高价'] > all_df['前日最高价'].rolling(n-1).max(), 'signal'] = 1
all_df['signal_two'] = 0
all_df['前日最低价'] = all_df['最低价'].shift(1)
all_df.loc[all_df['最低价'] < all_df['前日最低价'].rolling(n-1).min(), 'signal_two'] = 1

# 计算创新高新低个股占比
df_new['创新高数'] = all_df.groupby(['交易日期'])['signal'].sum()
df_new['创新低数'] = all_df.groupby(['交易日期'])['signal_two'].sum()
df_new['个股总数'] = all_df.groupby(['交易日期'])['股票代码'].count()
df_new['创新高个股占比'] = df_new['创新高数'] / df_new['个股总数']
df_new['创新低个股占比'] = df_new['创新低数'] / df_new['个股总数']

# 计算创业板指外各指数可用
# df_new['创新高个股占比'] = df_new['创新高数'] / 500
# df_new['创新低个股占比'] = df_new['创新低数'] / 500

df_new.reset_index(inplace=True)

# 输出结果
df_new.to_csv('60日新高新低个股占比.csv', encoding='gbk')

print(df_new)
