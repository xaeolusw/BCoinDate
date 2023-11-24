"""
邢不行-股票量化入门训练营
邢不行微信：xbx9585
Day3：选股策略示例
"""
import ast

import pandas as pd
import numpy as np
#import datetime
import matplotlib.pyplot as plt
import math


pd.set_option('expand_frame_repr', False)  # 当列太多时显示不清楚
# ===选股参数设定
select_stock_num = 3 # 参与选Gu前三名需选股数量>=3
c_rate = 1.2 / 10000  # 手续费，手续费>万1.2
t_rate = 1 / 1000  # 印花税


# ===导入数据
df = pd.read_csv('供选股数据.csv', encoding='gbk', parse_dates=['交易日期'], low_memory=False)  # 从csv文件中读取整理好的所有股票数据
#df.to_pickle("供选股数据.pickle") # csv to pickle, use once;
#df = pd.read_pickle('供选股数据.pickle') # 从pickle文件中读取整理好的所有股票数据
# exit()

# ==========只需要修改以下部分代码==========

# ===构建选股因子
# df['因子'] = df['总市值'] * df['成交额std_10'] #从小到大排，前面加－从大到小排。

# # ===对股票数据进行筛选
# df = df[df['上市至今交易天数'] > 250]  # 删除上市不满一年的股票
# df = df[df['开盘价']<10]

# 3500% :)
df['因子'] = df['总市值'] * df['成交额std_20'] #从小到大排，前面加－从大到小排。
# ===对股票数据进行筛选
df = df[df['上市至今交易天数'] > 540]  # 删除上市不满一年的股票
df = df[df['振幅_5'] < 0.21]  
df = df[df['涨跌幅std_20'] > 0.017]  
df = df[(np.isnan(df['市净率倒数']))|(df['市净率倒数'] > 0.19)]
df = df[df['收盘价'] > 3]
df = df[(df['股票代码'].str.startswith('sh') |  df['股票代码'].str.startswith('sz')) & #沪深，排除北京交易所
        ~df['股票代码'].str.startswith('sz300') &   #排除创业板
        ~df['股票代码'].str.startswith('sh688') &   #排除科创板
        ~df['股票代码'].str.startswith('sz301')]    #排除新三版
#print(datetime.datetime.strptime(df['交易日期'].astype(str),"%y-%m-%d"))
#df = df[pd.to_datetime(df['交易日期'],format='%y-%m-%d') > datetime.datetime(2022, 6, 1)]  #use after 2022.1.1 date
#df = df[df['交易日期'] >= pd.to_datetime('20220101')]
#df = df[df['归母净利润']>0]
# df = df[df['申万一级行业名称'].isin(['医药生物'])]  # 对所在行业进行筛选
# # '钢铁', '交通运输', '房地产', '公用事业', '化工', '休闲服务', '医药生物', '商业贸易', '食品饮料', '家用电器', '轻工制造', '纺织服装', '综合', '农林牧渔', '有色金属', '采掘', '电子', '银行', '汽车', '非银金融', '机械设备', '传媒', '国防军工', '建筑装饰', '通信', '电气设备', '计算机', '建筑材料'

# df = df[df['bias_20'] < 0]  # 对财务数据进行筛选
# 数据指标种类
# '交易日期', '股票代码', '股票名称', '是否交易',
# '开盘价', '最高价', '最低价', '收盘价', 'VWAP', '成交额',
# '涨跌幅', '下周期每天涨跌幅'
# '流通市值', '总市值', '上市至今交易天数', '财报季度', '财报年份',
# '归母净利润', '归母净利润_ttm', '归母净利润_ttm同比',
# '归母净利润_单季', '归母净利润_单季同比', '归母净利润_单季环比',
# '经营活动产生的现金流量净额', '经营活动产生的现金流量净额_ttm', '经营活动产生的现金流量净额_ttm同比',
# '经营活动产生的现金流量净额_单季', '经营活动产生的现金流量净额_单季同比', '经营活动产生的现金流量净额_单季环比',
# '净资产', '涨跌幅_10', '涨跌幅_20', 'bias_5', 'bias_10', 'bias_20',
# '振幅_5', '振幅_10', '振幅_20', '涨跌幅std_5', '涨跌幅std_10', '涨跌幅std_20',
# '成交额std_5', '成交额std_10', '成交额std_20',
# 'K', 'D', 'J', 'DIF', 'DEA', 'MACD', '市盈率倒数', '市净率倒数',
# '申万一级行业名称', '申万二级行业名称', '申万三级行业名称',
# 申万一级行业
# '钢铁', '交通运输', '房地产', '公用事业', '化工', '休闲服务', '医药生物',
# '商业贸易', '食品饮料', '家用电器', '轻工制造', '纺织服装', '综合', '农林牧渔',
# '有色金属', '采掘', '电子', '银行', '汽车', '非银金融', '机械设备', '传媒',
# '国防军工', '建筑装饰', '通信', '电气设备', '计算机', '建筑材料'

# ===选股
df['排名'] = df.groupby('交易日期')['因子'].rank()  # 根据选股因子对股票进行排名
df = df[df['排名'] <= select_stock_num]  # 选取排名靠前的股票


# ==========只需要修改以上部分代码==========


# ===整理选中股票数据，计算涨跌幅
# 挑选出选中股票
# df['股票代码'] += ' '
# df['股票名称'] += ' '
# df['下周期每天涨跌幅'] = df['下周期每天涨跌幅'].apply(lambda x: ast.literal_eval(x))
# group = df.groupby('交易日期')
# select_stock = pd.DataFrame()
# select_stock['买入股票代码'] = group['股票代码'].sum()
# select_stock['买入股票名称'] = group['股票名称'].sum()

# # 计算下周期每天的资金曲线
# select_stock['选股下周期每天资金曲线'] = group['下周期每天涨跌幅'].apply(lambda x: np.cumprod(np.array(list(x))+1, axis=1).mean(axis=0))
# # 扣除买入手续费
# select_stock['选股下周期每天资金曲线'] = select_stock['选股下周期每天资金曲线'] * (1 - c_rate)  # 计算有不精准的地方
# # 扣除卖出手续费、印花税。最后一天的资金曲线值，扣除印花税、手续费
# select_stock['选股下周期每天资金曲线'] = select_stock['选股下周期每天资金曲线'].apply(lambda x: list(x[:-1]) + [x[-1] * (1 - c_rate - t_rate)])
# # 计算下周期整体涨跌幅
# select_stock['选股下周期涨跌幅'] = select_stock['选股下周期每天资金曲线'].apply(lambda x: x[-1] - 1)
# del select_stock['选股下周期每天资金曲线']
# # 计算整体资金曲线
# select_stock.reset_index(inplace=True)
# select_stock['资金曲线'] = (select_stock['选股下周期涨跌幅'] + 1).cumprod()
# print(select_stock)


# # ===画图
# select_stock.set_index('交易日期', inplace=True)
# plt.plot(select_stock['资金曲线'])
# plt.show()



# ==========只需要修改以上部分代码==========
# ===整理选中股票数据，计算涨跌幅
# 挑选出选中股票
from datetime import datetime
df['股票代码'] += ' '
df['股票名称'] += ' '
df['下周期每天涨跌幅'] = df['下周期每天涨跌幅'].apply(lambda x: ast.literal_eval(x))
group = df.groupby('交易日期')
select_stock = pd.DataFrame()
select_stock['买入股票代码'] = group['股票代码'].sum()
select_stock['买入股票名称'] = group['股票名称'].sum()

# 计算下周期每天的资金曲线
select_stock['选股下周期每天资金曲线'] = group['下周期每天涨跌幅'].apply(
    lambda x: np.cumprod(np.array(list(x))+1, axis=1).mean(axis=0))
# 扣除买入手续费
select_stock['选股下周期每天资金曲线'] = select_stock['选股下周期每天资金曲线'] * \
    (1 - c_rate)  # 计算有不精准的地方
# 扣除卖出手续费、印花税。最后一天的资金曲线值，扣除印花税、手续费
select_stock['选股下周期每天资金曲线'] = select_stock['选股下周期每天资金曲线'].apply(
    lambda x: list(x[:-1]) + [x[-1] * (1 - c_rate - t_rate)])
# 计算下周期整体涨跌幅
select_stock['选股下周期涨跌幅'] = select_stock['选股下周期每天资金曲线'].apply(
    lambda x: x[-1] - 1)
del select_stock['选股下周期每天资金曲线']
# 计算整体资金曲线
select_stock.reset_index(inplace=True)
select_stock['资金曲线'] = (select_stock['选股下周期涨跌幅'] + 1).cumprod()
# kesa_取个对数试试看
select_stock['资金曲线对数'] = select_stock['资金曲线'].apply(lambda x: math.log(x, 10))
# kesa_取5日均线
select_stock['ma_5'] = select_stock['资金曲线'].rolling(window=5).mean()
# kesa_取 signal: 根据价格是否大于5日均线做出 signal
select_stock['signal'] = (select_stock['资金曲线'] >
                          select_stock['ma_5']).astype(int)
# 将前4天的 signal 列设置为1
select_stock.loc[0:3, 'signal'] = 1
# kesa_将 pos 值设为上一行的 signal 值
select_stock['pos'] = select_stock['signal'].shift(1)
# kesa_将第一天的 pos 值设为1
select_stock.loc[0:0, 'pos'] = 1
# kesa_实际涨跌: 资金
select_stock["实际下周期涨跌"] = select_stock["选股下周期涨跌幅"] * select_stock['signal']
select_stock['实际资金曲线'] = (select_stock['实际下周期涨跌'] + 1).cumprod()


print(select_stock)  # 打印一下资金曲线表

# 将当前日期格式化为yyyymmdd的字符串并输出
dataMark = datetime.today().strftime("%Y%m%d%H%M%S")
print(dataMark)
path = '/'
select_stock.to_csv('{}{}.csv'.format(path, dataMark), index=False)

# ===画图
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
select_stock.set_index('交易日期', inplace=True)
plt.plot(select_stock['资金曲线'])
plt.show()
plt.plot(select_stock['ma_5'])
plt.show()
plt.plot(select_stock['实际资金曲线'])
plt.show()