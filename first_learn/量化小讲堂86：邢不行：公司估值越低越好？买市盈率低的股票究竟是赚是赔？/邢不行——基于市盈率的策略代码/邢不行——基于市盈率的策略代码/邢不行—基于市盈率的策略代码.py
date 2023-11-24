"""
本代码由邢不行提供。
相关视频请看：
公司估值越低越好？买市盈率低的股票究竟是赚是赔？python量化给你答案。【量化投资邢不行啊】
https://www.bilibili.com/video/BV12S4y1P76y?spm_id_from=333.999.0.0
获取更多量化知识或有量化相关疑问，请联系邢不行个人微信：xbx719
"""

import matplotlib.pyplot as plt
import pandas as pd

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# 读取文件
# 输入不同csv文件名，查看不同策略结果
equity = pd.read_csv(r'低市盈率策略—分行业.csv', encoding='gbk', parse_dates=['交易日期'])
equity.set_index(['交易日期'], inplace=True)

print(equity)
# 可使用print功能观察数据

# 画图
equity[['策略净值', '沪深300指数']].plot(figsize=(16, 9), grid=False, fontsize=20)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.savefig(r'基于市盈率的策略净值.png')
plt.show()

