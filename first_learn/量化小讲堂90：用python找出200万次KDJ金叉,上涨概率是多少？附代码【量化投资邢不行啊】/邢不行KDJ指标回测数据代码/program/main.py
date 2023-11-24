"""
本代码由邢不行提供，用于计算KDJ指标。
如有问题，可联系邢不行微信xbx6660
"""

import os
from program.technical import *
from program.function import *

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# 后续计算N日后涨跌幅所需参数
day_list = [1, 5, 10, 20]
# 测试时间段，可根据数据时间更改
start_time = '20070101'
end_time = '20220331'
# 文件夹路径
# index 文件路径分开

# ======= 此处需修改
# 这里填写文件夹的绝对路径。
file_path = r'/Users/xbx/Desktop/邢不行技术指标计算代码/股票数据/'
# 如想回测指数相关内容，请使用下方代码
# file_path = r'/Users/xbx/Desktop/邢不行技术指标计算代码/指数数据/'

# 获取文件夹下的所有csv文件
file_list = os.listdir(file_path)
file_list = [f for f in file_list if '.csv' in f]
# 如需知道某个股票的指标信号和数值，可使用下方代码
# file_list = ['sh600000.csv']


dfs = []
for f in file_list:
    print(f)
    # 加载数据
    df = load_file(file_path, f)

    # 计算你需要的技术指标，具体计算步骤见：technical.py文件
    df = cal_kdj(df)

    # 计算未来表现
    # 计算N日后涨跌幅，统计涨跌幅>0时间段
    for day in day_list:
        df['%s日后涨跌幅' % day] = df['收盘价'].shift(0 - day) / df['收盘价'] - 1
        df['%s日后是否上涨' % day] = df['%s日后涨跌幅' % day] > 0
        df['%s日后是否上涨' % day].fillna(value=False, inplace=True)

    # 选取制定时间范围内的股票
    df = df[df['交易日期'] >= pd.to_datetime(start_time)]
    df = df[df['交易日期'] <= pd.to_datetime(end_time)]
    dfs.append(df)

all_df = pd.concat(dfs, ignore_index=True)

# 分析数据
analysis(all_df, day_list)

# 如需知道某个股票的指标信号和数值，可使用下行代码输出结果文件
# df.to_csv('指标计算.csv', encoding='gbk')

