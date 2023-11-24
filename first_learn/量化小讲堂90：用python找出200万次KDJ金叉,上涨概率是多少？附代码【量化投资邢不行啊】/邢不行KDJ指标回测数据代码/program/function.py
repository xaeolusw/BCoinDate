"""
本代码由邢不行提供，用于计算KDJ指标。
如有问题，可联系邢不行微信xbx6660
"""

import pandas as pd

def rehabilitation(df):
    # =计算涨跌幅
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


def load_file(path, file):
    path += file
    if file in ['sh000001.csv', 'sh000300.csv']:
        df = pd.read_csv(path, encoding='gbk', parse_dates=['candle_end_time'])
        df.rename(columns={'candle_end_time': '交易日期', 'open': '开盘价', 'high': '最高价', 'low': '最低价', 'close': '收盘价'},
                  inplace=True)
        df['前收盘价'] = df['收盘价'].shift()
        df['前收盘价'].fillna(value=df['开盘价'], inplace=True)
    else:
        df = pd.read_csv(path, encoding='gbk', parse_dates=['交易日期'], skiprows=1)
    return df


def analysis(all_df, day_list):
    # 计算N日后涨跌幅大于0的概率
    for signal, group in all_df.groupby('signal'):
        if signal == 1:
            print('\n', '=' * 10, '看涨信号', '=' * 10)
        elif signal == 0:
            print('\n', '=' * 10, '看跌信号', '=' * 10)
        print(group[[str(i) + '日后涨跌幅' for i in day_list]].describe())
        for i in day_list:
            if signal == 1:
                print(str(i) + '天后涨跌幅大于0概率', '\t', float(group[group[str(i) + '日后涨跌幅'] > 0].shape[0]) / group.shape[0])
            elif signal == 0:
                print(str(i) + '天后涨跌幅小于0概率', '\t', float(group[group[str(i) + '日后涨跌幅'] < 0].shape[0]) / group.shape[0])
    return



