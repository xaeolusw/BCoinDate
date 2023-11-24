"""
本代码由邢不行提供，用于计算KDJ指标。
如有问题，可联系邢不行微信xbx6660
"""

from program.function import rehabilitation

# KDJ指标
def cal_kdj(df_kdj, n=9, close='收盘价', high='最高价', low='最低价'):
    df_kdj = rehabilitation(df_kdj)
    df_kdj['H'] = df_kdj[high].rolling(n).max()
    df_kdj['L'] = df_kdj[low].rolling(n).min()
    if df_kdj.empty:
        return df_kdj
    df_kdj['RSV'] = (df_kdj[close] - df_kdj['L']) / (df_kdj['H'] - df_kdj['L']) * 100
    df_kdj['K'] = df_kdj['RSV'].ewm(span=2, adjust=False).mean()
    df_kdj['D'] = df_kdj['K'].ewm(span=2, adjust=False).mean()
    df_kdj['J'] = df_kdj['K'] * 3 - df_kdj['D'] * 2

    # #KD金叉死叉
    df_kdj.loc[(df_kdj['K'].shift(1) <= df_kdj['D'].shift(1)) & (
            df_kdj['K'] > df_kdj['D']), 'signal'] = 1  # 买入信号
    df_kdj.loc[(df_kdj['K'].shift(1) >= df_kdj['D'].shift(1)) & (
            df_kdj['K'] < df_kdj['D']), 'signal'] = 0  # 卖出信号

    # 低位金叉，高位死叉（D参数20、80）
    # df_kdj.loc[(df_kdj['D'] <= 20) & (df_kdj['K'].shift(1) <= df_kdj['D'].shift(1)) & (
    #         df_kdj['K'] > df_kdj['D']), 'signal'] = 1  # 买入信号
    # df_kdj.loc[(df_kdj['D'] >= 80) & (df_kdj['K'].shift(1) >= df_kdj['D'].shift(1)) & (
    #         df_kdj['K'] < df_kdj['D']), 'signal'] = 0  # 卖出信号
    return df_kdj







