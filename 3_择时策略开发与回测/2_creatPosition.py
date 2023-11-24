import pandas as pd
import os
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


# ===导入数据
if os.name == 'nt':
    df = pd.read_hdf('D:\\PythonProjects\\coin_data\\BTCUSDT_signals.h5', key='df')
elif os.name == 'posix':
    df = pd.read_hdf('/Volumes/USB-DISK/PythonProjects/coin_data/BTCUSDT_signals.h5', key='df')
else:
    print('操作系统不支持')
    exit()

# ===由signal计算出实际的每天持有仓位
# 在产生signal的k线结束的时候，进行买入
df['signal'].fillna(method='ffill', inplace=True)   # 用前面的信号值填充当天的信号值
df['signal'].fillna(value=0, inplace=True)  # 将初始行数的signal补全为0
df['pos'] = df['signal'].shift()
df['pos'].fillna(value=0, inplace=True)  # 将初始行数的pos补全为0


# ===对无法买卖的时候做出相关处理
# 例如：下午4点清算，无法交易；股票、期货当天涨跌停的时候无法买入；股票的t+1交易制度等等。
# 当前周期持仓无法变动的K线
condition = (df['candle_begin_time'].dt.hour == 16) & (df['candle_begin_time'].dt.minute == 0)
df.loc[condition, 'pos'] = None

# pos为空的时，不能买卖，只能和前一周期保持一致。
df['pos'].fillna(method='ffill', inplace=True)


# ===将数据存入hdf文件中
# 删除无关中间变量
df.drop(['signal'], axis=1, inplace=True)

if os.name == 'nt':
    path = 'D:\\PythonProjects\\coin_data\\BTCUSDT_pos.h5'
elif os.name == 'posix':
    path = '/Volumes/USB-DISK/PythonProjects/coin_data/BTCUSDT_pos.h5'
else:
    print('操作系统不支持')
    exit()

df.to_hdf(path, key='df', mode='w')
df.to_csv(path[:-2]+'csv') #将数据存入csv文件中,方便查看
print('生成仓位文件成功，文件名为%s'%path)
