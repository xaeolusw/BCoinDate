"""
邢不行-股票量化入门训练营
邢不行微信：xbx9585
Day3：选股策略示例
"""
import ast
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


pd.set_option('expand_frame_repr', False)  # 当列太多时显示不清楚
# ===选股参数设定
select_stock_num = 3  # 参与选Gu前三名需选股数量>=3
c_rate = 1.2 / 10000  # 手续费，手续费>万1.2
t_rate = 1 / 1000  # 印花税


# ===导入数据
if os.path.isfile('供选股数据.pkl'):
    df = pd.read_pickle('供选股数据.pkl')
else:
    df = pd.read_csv('供选股数据.csv', encoding='gbk', parse_dates=['交易日期'], low_memory=False)  # 从csv文件中读取整理好的所有股票数据
    df.to_pickle('供选股数据.pkl')

# 计算月均线并保存
if not 'MA3' in df.columns:
    code_list = list(df[['股票代码']].drop_duplicates()['股票代码'])
    records = []
    for code in code_list:
        tmp = df[df['股票代码'] == code].copy()
        tmp['MA3'] = tmp['收盘价'].rolling(3, min_periods = 1).mean()
        tmp['MA5'] = tmp['收盘价'].rolling(5, min_periods = 1).mean()
        records.append(tmp)
        print('{}/{} {}'.format(len(records), len(code_list), code))
    df = pd.concat(records)
    df.to_pickle('供选股数据.pkl')
# exit()

# ==========只需要修改以下部分代码==========

# ===构建选股因子

# ===对股票数据进行筛选
#df = df[df['上市至今交易天数'] > 250]  # 删除上市不满一年的股票

#df = df[~df['申万一级行业名称'].isin(['纺织服装', '机械设备'])]  # 对所在行业进行筛选
# # '钢铁', '交通运输', '房地产', '公用事业', '化工', '休闲服务', '医药生物', '商业贸易', '食品饮料', '家用电器', '轻工制造', '纺织服装', '综合', '农林牧渔', '有色金属', '采掘', '电子', '银行', '汽车', '非银金融', '机械设备', '传媒', '国防军工', '建筑装饰', '通信', '电气设备', '计算机', '建筑材料'

# df = df[df['bias_20'] < 0]  # 对财务数据进行筛选

def do_calc(df, args):
    df['因子'] = np.power(df['总市值'], args['市值指数']) * df['成交额std_20'] 
    df = df[df['上市至今交易天数'] >= args['上市至今交易天数']]
    df = df[df['振幅_5'] <= args['振幅_5']]
    df = df[df['涨跌幅std_20'] >= args['涨跌幅std_20']]
    df = df[(np.isnan(df['市净率倒数'])) | (df['市净率倒数'] >= args['市净率倒数'])]
    df = df[(df['MA3'] * args['MA3'] >= df['收盘价']) & (df['MA5'] * args['MA5'] >= df['收盘价'])]
    df = df[(df['收盘价'] <= args['最高收盘价']) & (df['收盘价'] >= args['最低收盘价'])]

    # ===选股
    df['排名'] = df.groupby('交易日期')['因子'].rank()  # 根据选股因子对股票进行排名
    df = df[df['排名'] <= select_stock_num]  # 选取排名靠前的股票

    # ==========只需要修改以上部分代码==========

    # ===整理选中股票数据，计算涨跌幅
    # 挑选出选中股票
    df['股票代码'] += ' '
    df['股票名称'] += ' '
    df['下周期每天涨跌幅'] = df['下周期每天涨跌幅'].apply(lambda x: ast.literal_eval(x))
    group = df.groupby('交易日期')
    select_stock = pd.DataFrame()
    select_stock['买入股票代码'] = group['股票代码'].sum()
    select_stock['买入股票名称'] = group['股票名称'].sum()

    # 计算下周期每天的资金曲线
    select_stock['选股下周期每天资金曲线'] = group['下周期每天涨跌幅'].apply(lambda x: np.cumprod(np.array(list(x))+1, axis=1).mean(axis=0))
    # 扣除买入手续费
    select_stock['选股下周期每天资金曲线'] = select_stock['选股下周期每天资金曲线'] * (1 - c_rate)  # 计算有不精准的地方
    # 扣除卖出手续费、印花税。最后一天的资金曲线值，扣除印花税、手续费
    select_stock['选股下周期每天资金曲线'] = select_stock['选股下周期每天资金曲线'].apply(lambda x: list(x[:-1]) + [x[-1] * (1 - c_rate - t_rate)])
    # 计算下周期整体涨跌幅
    select_stock['选股下周期涨跌幅'] = select_stock['选股下周期每天资金曲线'].apply(lambda x: x[-1] - 1)
    del select_stock['选股下周期每天资金曲线']
    # 计算整体资金曲线
    select_stock.reset_index(inplace=True)
    select_stock['资金曲线'] = (select_stock['选股下周期涨跌幅'] + 1).cumprod()
    return select_stock

# 可变参数调节区间和步长
args_dict = {
    '市值指数': {'最小值': 1, '最大值': 2, '步长': 0.1, '初始': 1.5},
    '上市至今交易天数': {'最小值': 530, '最大值': 560, '步长': 10, '初始': 550},
    '振幅_5': {'最小值': 0.18, '最大值': 0.22, '步长': 0.01, '初始': 0.2},
    '涨跌幅std_20': {'最小值': 0.015, '最大值': 0.020, '步长': 0.001, '初始': 0.017},
    '市净率倒数': {'最小值': 0.17, '最大值': 0.22, '步长': 0.01, '初始': 0.2},
    'MA3': {'最小值': 1.00, '最大值': 1.30, '步长': 0.05, '初始': 1.15},
    'MA5': {'最小值': 1.10, '最大值': 1.40, '步长': 0.05, '初始': 1.25},
    '最低收盘价': {'最小值': 2.0, '最大值': 8.0, '步长': 0.5, '初始': 3},
    '最高收盘价': {'最小值': 20, '最大值': 40.0, '步长': 2, '初始': 30},
}

# 最大倍数: 11847.583220980756 最佳参数: {'市值指数': 1.3, '上市至今交易天数': 560, '振幅_5': 0.2, '涨跌幅std_20': 0.017, '市净率倒数': 0.19000000000000003, 'MA3': 1.2000000000000002, 'MA5': 1.25, '最低收盘价': 3, '最高收盘价': 34}

'''
args_dict = {
    '上市至今交易天数': {'最小值': 200, '最大值': 700, '步长': 50, '初始': 500},
    '振幅_5': {'最小值': 0.10, '最大值': 0.50, '步长': 0.02, '初始': 0.2},
    '涨跌幅std_20': {'最小值': 0.005, '最大值': 0.030, '步长': 0.001, '初始': 0.02},
    '市净率倒数': {'最小值': 0.05, '最大值': 0.30, '步长': 0.01, '初始': 0.2},
    'MA3': {'最小值': 1.00, '最大值': 2.00, '步长': 0.05, '初始': 1.15},
    'MA5': {'最小值': 1.00, '最大值': 3.00, '步长': 0.05, '初始': 1.55},
}
'''

# 运行参数
res_dict = {
    '最大倍数': 0,
    '最大倍数参数': None,
    '本轮最大倍数': 0,
    '本轮最大倍数参数': None
}

# 初始化运行参数
args = {}
for code, dt in args_dict.items():
    args[code] = dt['初始']

for i in range(3):
    for code in args.keys():
        curr_arg = args_dict[code]['最小值']
        while curr_arg <= args_dict[code]['最大值']:
            args[code] = curr_arg
            print('参数集: ' + str(args))
            select_stock = do_calc(df.copy(), args)
            v = list(select_stock['资金曲线'])[-1]
            if v > res_dict['本轮最大倍数']:
                print('新记录: {}倍'.format(v))
                res_dict['本轮最大倍数']= v
                res_dict['本轮最大倍数参数']= args.copy()
            curr_arg += args_dict[code]['步长']
        if res_dict['本轮最大倍数'] > res_dict['最大倍数']:
            res_dict['最大倍数'] = res_dict['本轮最大倍数']
            res_dict['最大倍数参数'] = res_dict['本轮最大倍数参数']
        args[code] = res_dict['最大倍数参数'][code]

print('最大倍数: {} 最佳参数: {}'.format(res_dict['最大倍数'], str(res_dict['最大倍数参数'])))

select_stock = do_calc(df.copy(), res_dict['最大倍数参数'])

select_stock.to_csv('回测结果.csv', encoding = 'gbk')

# ===画图
select_stock.set_index('交易日期', inplace=True)
plt.plot(select_stock['资金曲线'])
plt.show()
