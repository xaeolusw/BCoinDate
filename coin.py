#okex：https://www.okex.com/api/v5/market/ticker?instId=BTC-USD-SWAP

import ssl
import pandas as pd
from urllib.request import urlopen, Request
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# content = urlopen(url=url, timeout=10).read()
# urlopen专门用来获取网页上的相关内容，使用urlopen抓取数据
url = 'https://ok.winder-oz.com/api/v5/market/ticker?instId=BTC-USD-SWAP'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
context = ssl.SSLContext()#protocol=ssl.PROTOCOL_TLS)
content = urlopen(req, context=context, timeout=10).read()

print(content)


"""
获取单个产品行情信息（限速：20次/2s,限速规则：IP）
GET /api/v5/market/ticker

例：https://ok.winder-oz.com/api/v5/market/ticker?instId=BTC-USD-SWAP
{
    "code":"0",
    "msg":"",
    "data":[
        {
        "instType":"SWAP", #产品类型
        "instId":"BTC-USD-SWAP", #产品ID
        "last":"25762.2", #最新成交价
        "lastSz":"196", #最新成交的数量
        "askPx":"25763.4", #卖一价
        "askSz":"1458", #卖一价对应的数量
        "bidPx":"25763.3",  #买一价
        "bidSz":"1251", #买一价对应的数量
        "open24h":"27022.8",    #24小时开盘价
        "high24h":"27022.8",    #24小时最高价
        "low24h":"25379.6", #24小时最低价
        "volCcy24h":"33189.9053",   #24小时成交量，以币为单位
        "vol24h":"8670484", #24小时成交量，以张为单位
        "ts":"1686019500016",   #ticker数据产生时间，Unix时间戳的毫秒数格式，如 1597026383085
        "sodUtc0":"25736",  #UTC 0 时开盘价
        "sodUtc8":"25983.1" #UTC+8 时开盘价
        }
    ]
}


获取指数行情数据（限速：20次/2s，限速规则：IP）
GET /api/v5/market/index-tickers

示例
https://ok.winder-oz.com/api/v5/market/index-tickers?instId=BTC-USDT
请求参数
参数名	        类型	是否必须	 描述
quoteCcy	   String	可选	  指数计价单位， 目前只有 USD/USDT/BTC/USDC为计价单位的指数，quoteCcy和instId必须填写一个
instId	       String	可选	  指数，如 BTC-USD

返回结果
{
    "code": "0",
    "msg": "",
    "data": [
        {
            "instId": "BTC-USDT",   #指数
            "idxPx": "43350",   #最新指数价格
            "high24h": "43649.7",   #24小时指数最高价格
            "sodUtc0": "43444.1",   #UTC 0 时开盘价
            "open24h": "43640.8",   #24小时指数开盘价格
            "low24h": "43261.9",    #24小时指数最低价格
            "sodUtc8": "43328.7",   #UTC+8 时开盘价
            "ts": "1649419644492"   #指数价格更新时间，Unix时间戳的毫秒数格式，如1597026383085
        }
    ]
}
"""

"""
获取K线数据。K线数据按请求的粒度分组返回，K线数据每个粒度最多可获取最近1,440条。(限速：40次/2s,限速规则：IP)
GET /api/v5/market/candles

请求参数
参数名	类型	是否必须	描述
instId	String	是	产品ID，如BTC-USD-190927-5000-C
bar	String	否	时间粒度，默认值1m
如 [1m/3m/5m/15m/30m/1H/2H/4H]
香港时间开盘价k线：[6H/12H/1D/2D/3D/1W/1M/3M]
UTC时间开盘价k线：[/6Hutc/12Hutc/1Dutc/2Dutc/3Dutc/1Wutc/1Mutc/3Mutc]
after	String	否	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
before	String	否	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts
limit	String	否	分页返回的结果集数量，最大为300，不填默认返回100条

https://ok.winder-oz.com/api/v5/market/candles?instId=BTC-USDT

返回结果
{
    "code":"0",
    "msg":"",
    "data":[
        [
            "1686023700000",      #ts,开始时间，Unix时间戳的毫秒数格式，如 1597026383085
            "25722.8",            #o,开盘价格
            "25722.9",            #h,最高价格
            "25718.5",            #l最低价格
            "25718.6",            #c收盘价格
            "0.45880158",         #vol,交易量，以张为单位(如果是衍生品合约，数值为合约的张数。如果是币币/币币杠杆，数值为交易货币的数量。)
            "11801.420740324",    #volCcy,交易量，以币为单位(如果是衍生品合约，数值为交易货币的数量。如果是币币/币币杠杆，数值为计价货币的数量。)
            "11801.420740324",    #volCcyQuote,交易量，以计价货币为单位(如：BTC-USDT 和 BTC-USDT-SWAP, 单位均是 USDT;BTC-USD-SWAP 单位是 USD)
            "0"                   #confirm,K线状态,0 代表 K 线未完结，1 代表 K 线已完结。
            #返回的第一条K线数据可能不是完整周期k线，返回值数组顺序分别为是：[ts,o,h,l,c,vol,volCcy,volCcyQuote,confirm]
            #对于当前周期的K线数据，没有成交时，开高收低默认都取上一周期的收盘价格。
        ],
        [
            "1686023640000",
            "25720",
            "25730",
            "25720",
            "25722.9",
            "1.33493028",
            "34338.110904479",
            "34338.110904479",
            "1"
        ]
    ]
}
"""

"""
获取最近几年的历史k线数据(限速：20次/2s,限速规则：IP)
GET /api/v5/market/history-candles

请求示例
GET /api/v5/market/history-candles?instId=BTC-USD-190927
请求参数
参数名	类型	是否必须	描述
instId	String	是	产品ID，如BTC-USD-200927
after	String	否	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
before	String	否	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts
bar	String	否	时间粒度，默认值1m
如 [1m/3m/5m/15m/30m/1H/2H/4H]
香港时间开盘价k线：[6H/12H/1D/2D/3D/1W/1M/3M]
UTC时间开盘价k线：[6Hutc/12Hutc/1Dutc/2Dutc/3Dutc/1Wutc/1Mutc/3Mutc]
limit	String	否	分页返回的结果集数量，最大为100，不填默认返回100条
返回结果

{
    "code":"0",
    "msg":"",
    "data":[
     [
        "1597026383085",
        "3.721",
        "3.743",
        "3.677",
        "3.708",
        "8422410",
        "22698348.04828491",
        "12698348.04828491",
        "1"
    ],
    [
        "1597026383085",
        "3.731",
        "3.799",
        "3.494",
        "3.72",
        "24912403",
        "67632347.24399722",
        "37632347.24399722",
        "1"
    ]
    ]
}
返回参数
参数名	类型	描述
ts	String	开始时间，Unix时间戳的毫秒数格式，如 1597026383085
o	String	开盘价格
h	String	最高价格
l	String	最低价格
c	String	收盘价格
vol	String	交易量，以张为单位
如果是衍生品合约，数值为合约的张数。
如果是币币/币币杠杆，数值为交易货币的数量。
volCcy	String	交易量，以币为单位
如果是衍生品合约，数值为交易货币的数量。
如果是币币/币币杠杆，数值为计价货币的数量。
volCcyQuote	String	交易量，以计价货币为单位
如：BTC-USDT 和 BTC-USDT-SWAP, 单位均是 USDT；
BTC-USD-SWAP 单位是 USD
confirm	String	K线状态
0 代表 K 线未完结，1 代表 K 线已完结。
 返回值数组顺序分别为是：[ts,o,h,l,c,vol,volCcy,confirm]

 

 获取指数K线数据
指数K线数据每个粒度最多可获取最近1,440条。

限速：20次/2s
限速规则：IP
HTTP请求
GET /api/v5/market/index-candles

请求示例

GET /api/v5/market/index-candles?instId=BTC-USD
请求参数
参数名	类型	是否必须	描述
instId	String	是	现货指数，如BTC-USD
after	String	否	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
before	String	否	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts
bar	String	否	时间粒度，默认值1m
如 [1m/3m/5m/15m/30m/1H/2H/4H]
香港时间开盘价k线：[6H/12H/1D/1W/1M/3M]
UTC时间开盘价k线：[/6Hutc/12Hutc/1Dutc/1Wutc/1Mutc/3Mutc]
limit	String	否	分页返回的结果集数量，最大为100，不填默认返回100条
返回结果

{
    "code":"0",
    "msg":"",
    "data":[
     [
        "1597026383085",
        "3.721",
        "3.743",
        "3.677",
        "3.708",
        "0"
    ],
    [
        "1597026383085",
        "3.731",
        "3.799",
        "3.494",
        "3.72",
        "1"
    ]
    ]
}
返回参数
参数名	类型	描述
ts	String	开始时间，Unix时间戳的毫秒数格式，如 1597026383085
o	String	开盘价格
h	String	最高价格
l	String	最低价格
c	String	收盘价格
confirm	String	K线状态
0 代表 K 线未完结，1 代表 K 线已完结。
 返回的第一条K线数据可能不是完整周期k线，返回值数组顺序分别为是：[ts,o,h,l,c,confirm]
获取指数历史K线数据
获取最近几年的指数K线数据

限速：10次/2s
限速规则：IP
HTTP请求
GET /api/v5/market/history-index-candles

请求示例

GET /api/v5/market/history-index-candles?instId=BTC-USD
请求参数
参数名	类型	是否必须	描述
instId	String	是	现货指数，如BTC-USD
after	String	否	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
before	String	否	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts
bar	String	否	时间粒度，默认值1m
如 [1m/3m/5m/15m/30m/1H/2H/4H]
香港时间开盘价k线：[6H/12H/1D/1W/1M]
UTC时间开盘价k线：[/6Hutc/12Hutc/1Dutc/1Wutc/1Mutc]
limit	String	否	分页返回的结果集数量，最大为100，不填默认返回100条
返回结果

{
    "code":"0",
    "msg":"",
    "data":[
     [
        "1597026383085",
        "3.721",
        "3.743",
        "3.677",
        "3.708",
        "1"
    ],
    [
        "1597026383085",
        "3.731",
        "3.799",
        "3.494",
        "3.72",
        "1"
    ]
    ]
}
返回参数
参数名	类型	描述
ts	String	开始时间，Unix时间戳的毫秒数格式，如 1597026383085
o	String	开盘价格
h	String	最高价格
l	String	最低价格
c	String	收盘价格
confirm	String	K线状态
0 代表 K 线未完结，1 代表 K 线已完结。
 返回值数组顺序分别为是：[ts,o,h,l,c,confirm]


 获取标记价格K线数据
标记价格K线数据每个粒度最多可获取最近1,440条。

限速：20次/2s
限速规则：IP
HTTP请求
GET /api/v5/market/mark-price-candles

请求示例

GET /api/v5/market/mark-price-candles?instId=BTC-USD-SWAP
请求参数
参数名	类型	是否必须	描述
instId	String	是	产品ID，如BTC-USD-SWAP
after	String	否	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
before	String	否	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts
bar	String	否	时间粒度，默认值1m
如 [1m/3m/5m/15m/30m/1H/2H/4H]
香港时间开盘价k线：[6H/12H/1D/1W/1M/3M]
UTC时间开盘价k线：[6Hutc/12Hutc/1Dutc/1Wutc/1Mutc/3Mutc]
limit	String	否	分页返回的结果集数量，最大为100，不填默认返回100条
返回结果

{
    "code":"0",
    "msg":"",
    "data":[
     [
        "1597026383085",
        "3.721",
        "3.743",
        "3.677",
        "3.708",
        "0"
    ],
    [
        "1597026383085",
        "3.731",
        "3.799",
        "3.494",
        "3.72",
        "1"
    ]
    ]
}
返回参数
参数名	类型	描述
ts	String	开始时间，Unix时间戳的毫秒数格式，如 1597026383085
o	String	开盘价格
h	String	最高价格
l	String	最低价格
c	String	收盘价格
confirm	String	K线状态
0 代表 K 线未完结，1 代表 K 线已完结。
 返回的第一条K线数据可能不是完整周期k线，返回值数组顺序分别为是：[ts,o,h,l,c,confirm]
获取标记价格历史K线数据
获取最近几年的标记价格K线数据

限速：10次/2s
限速规则：IP
HTTP请求
GET /api/v5/market/history-mark-price-candles

请求示例

GET /api/v5/market/history-mark-price-candles?instId=BTC-USD-SWAP
请求参数
参数名	类型	是否必须	描述
instId	String	是	产品ID，如BTC-USD-SWAP
after	String	否	请求此时间戳之前（更旧的数据）的分页内容，传的值为对应接口的ts
before	String	否	请求此时间戳之后（更新的数据）的分页内容，传的值为对应接口的ts
bar	String	否	时间粒度，默认值1m
如 [1m/3m/5m/15m/30m/1H/2H/4H]
香港时间开盘价k线：[6H/12H/1D/1W/1M]
UTC时间开盘价k线：[6Hutc/12Hutc/1Dutc/1Wutc/1Mutc]
limit	String	否	分页返回的结果集数量，最大为100，不填默认返回100条
返回结果

{
    "code":"0",
    "msg":"",
    "data":[
     [
        "1597026383085",
        "3.721",
        "3.743",
        "3.677",
        "3.708",
        "1"
    ],
    [
        "1597026383085",
        "3.731",
        "3.799",
        "3.494",
        "3.72",
        "1"
    ]
    ]
}
返回参数
参数名	类型	描述
ts	String	开始时间，Unix时间戳的毫秒数格式，如 1597026383085
o	String	开盘价格
h	String	最高价格
l	String	最低价格
c	String	收盘价格
confirm	String	K线状态
0 代表 K 线未完结，1 代表 K 线已完结。
 返回值数组顺序分别为是：[ts,o,h,l,c,confirm]
获取交易产品公共成交数据
查询市场上的成交信息数据

限速：100次/2s
限速规则：IP
HTTP请求
GET /api/v5/market/trades

请求示例

GET /api/v5/market/trades?instId=BTC-USDT
请求参数
参数名	类型	是否必须	描述
instId	String	是	产品ID，如 BTC-USDT
limit	String	否	分页返回的结果集数量，最大为500，不填默认返回100条
返回结果

{
    "code": "0",
    "msg": "",
    "data": [
        {
            "instId": "BTC-USDT",
            "side": "sell",
            "sz": "0.00001",
            "px": "29963.2",
            "tradeId": "242720720",
            "ts": "1654161646974"
        },
        {
            "instId": "BTC-USDT",
            "side": "sell",
            "sz": "0.00001",
            "px": "29964.1",
            "tradeId": "242720719",
            "ts": "1654161641568"
        }
    ]
}
返回参数
参数名	类型	描述
instId	String	产品ID
tradeId	String	成交ID
px	String	成交价格
sz	String	成交数量
side	String	成交方向
buy：买
sell：卖
ts	String	成交时间，Unix时间戳的毫秒数格式， 如1597026383085
 最多获取最近500条历史公共成交数据
获取交易产品公共历史成交数据
查询市场上的成交信息数据，可以分页获取最近3个月的数据。

限速：10次/2s
限速规则：IP
HTTP请求
GET /api/v5/market/history-trades

请求示例

GET /api/v5/market/history-trades?instId=BTC-USDT
请求参数
参数名	    类型	    是否必须	    描述
instId	    String	是	产品ID，如 BTC-USDT
type	    String	否	分页类型(1：tradeId分页;2：时间戳分页.默认为1：tradeId分页)
after	    String	否	请求此 ID 或 ts 之前的分页内容，传的值为对应接口的 tradeId 或 ts
before	    String	否	请求此ID之后（更新的数据）的分页内容，传的值为对应接口的 tradeId。不支持时间戳分页。
limit	    String	否	分页返回的结果集数量，最大为100，不填默认返回100条

返回结果
{
    "code": "0",
    "msg": "",
    "data": [
        {
            "instId": "BTC-USDT",
            "side": "sell",
            "sz": "0.00001",
            "px": "29963.2",
            "tradeId": "242720720",
            "ts": "1654161646974"
        },
        {
            "instId": "BTC-USDT",
            "side": "sell",
            "sz": "0.00001",
            "px": "29964.1",
            "tradeId": "242720719",
            "ts": "1654161641568"
        }
    ]
}
返回参数
参数名	类型	描述
instId	String	产品ID
tradeId	String	成交ID
px	String	成交价格
sz	String	成交数量
side	String	成交方向
buy：买
sell：卖
ts	String	成交时间，Unix时间戳的毫秒数格式， 如1597026383085
"""

"""
获取所有可交易产品的信息列表。(限速：20次/2s,限速规则：IP +instType)
GET /api/v5/public/instruments

请求示例
GET /api/v5/public/instruments?instType=SPOT

请求参数
参数名	        类型	是否必须	描述
instType       String	是	     产品类型
                SPOT：币币
                MARGIN：币币杠杆
                SWAP：永续合约
                FUTURES：交割合约
                OPTION：期权
uly	           String	可选	 标的指数，仅适用于交割/永续/期权，期权必填
instFamily	   String	否	     交易品种，仅适用于交割/永续/期权
instId	       String	否	     产品ID

返回结果
{
    "code":"0",
    "data":[
        {
            "alias":"",                                         #合约日期别名(this_week：本周;next_week：次周;quarter：季度;next_quarter：次季度.仅适用于交割)
            "baseCcy":"BTC",                                    #交易货币币种，如 BTC-USDT 中的 BTC ，仅适用于币币/币币杠杆
            "category":"1",                                     #币种类别，注意：此参数已废弃
            "ctMult":"",                                        #合约乘数，仅适用于交割/永续/期权
            "ctType":"",                                        #linear：正向合约;inverse：反向合约;仅适用于交割/永续
            "ctVal":"",                                         #合约面值，仅适用于交割/永续/期权
            "ctValCcy":"",                                      #合约面值计价币种，仅适用于交割/永续/期权
            "expTime":"",                                       #交割/行权日期，仅适用于交割 和 期权
            "instFamily":"",                                    #交易品种，如 BTC-USD，仅适用于交割/永续/期权
            "instId":"BTC-USDT",                                #产品id
            "instType":"SPOT",                                  #产品类型
            "lever":"10",                                       #该instId支持的最大杠杆倍数，不适用于币币、期权
            "listTime":"1548133413000",                         #上线日期
            "lotSz":"0.00000001",                               #下单数量精度，如 BTC-USDT-SWAP：1
            "maxIcebergSz":"9999999999.0000000000000000",       #合约或现货冰山委托的单笔最大委托数量,合约的数量单位是“张”，现货的数量单位是“交易货币”
            "maxLmtSz":"9999999999",                            #合约或现货限价单的单笔最大委托数量,合约的数量单位是“张”，现货的数量单位是“交易货币”
            "maxMktSz":"1000000",                               #合约或现货市价单的单笔最大委托数量,合约的数量单位是“张”，现货的数量单位是“USDT”
            "maxStopSz":"1000000",                              #合约或现货止盈止损市价委托的单笔最大委托数量,合约的数量单位是“张”，现货的数量单位是“USDT”
            "maxTriggerSz":"9999999999.0000000000000000",       #合约或现货计划委托委托的单笔最大委托数量,合约的数量单位是“张”，现货的数量单位是“交易货币”
            "maxTwapSz":"9999999999.0000000000000000",          #合约或现货时间加权单的单笔最大委托数量,合约的数量单位是“张”，现货的数量单位是“交易货币”
            "minSz":"0.00001",                                  #最小下单数量,合约的数量单位是“张”，现货的数量单位是“交易货币”
            "optType":"",                                       #期权类型，C或P 仅适用于期权
            "quoteCcy":"USDT",                                  #计价货币币种，如 BTC-USDT 中的 USDT ，仅适用于币币/币币杠杆
            "settleCcy":"",                                     #交割/行权货币币种，如 BTC-USD 中的 USD，仅适用于交割/期权
            "state":"live",                                     #产品状态(live：交易中;suspend：暂停中;preopen：预上线，如：交割和期权的新合约在 live 之前，会有 preopen 状态;test：测试中（测试产品，不可交易）
            "stk":"",                                           #行权价格，仅适用于期权
            "tickSz":"0.1",                                     #下单价格精度，如 0.0001,对于期权来说，是梯度中的最小下单价格精度，如果想要获取期权价格梯度，请使用"获取期权价格梯度"接口
            "uly":""                                            #标的指数，如 BTC-USD，仅适用于交割/永续/期权
            #合约的数量单位是“张”，现货的数量单位是“USDT”
            #当合约预上线时，状态变更为预上线（即新生成一个合约，新合约会处于预上线状态）； 当产品下线的时候（如交割合约被交割的时候，期权合约被行权的时候），查询不到该产品
        },
        {
            "alias":"",
            "baseCcy":"ETH",
            "category":"1",
            "ctMult":"",
            "ctType":"",
            "ctVal":"",
            "ctValCcy":"",
            "expTime":"",
            "instFamily":"",
            "instId":"ETH-USDT",
            "instType":"SPOT",
            "lever":"10",
            "listTime":"1548133413000",
            "lotSz":"0.000001",
            "maxIcebergSz":"999999999999.0000000000000000",
            "maxLmtSz":"999999999999",
            "maxMktSz":"1000000",
            "maxStopSz":"1000000",
            "maxTriggerSz":"999999999999.0000000000000000",
            "maxTwapSz":"999999999999.0000000000000000",
            "minSz":"0.0001",
            "optType":"",
            "quoteCcy":"USDT",
            "settleCcy":"",
            "state":"live",
            "stk":"",
            "tickSz":"0.01",
            "uly":""
        }
    ],
    "msg":""
}
"""
# 火币：https://api.huobi.pro/market/detail/merged?symbol=btcusdt
# 返回结果示例：{"status":"ok","ch":"market.btcusdt.detail.merged","ts":1583810974164,"tick":{"amount":71311.94804854663,"open":8082.13,"close":7890.19,"high":8082.14,"id":210146022322,"count":561789,"low":7638.0,"version":210146022322,"ask":[7890.98,0.58188],"vol":5.587285592033827E8,"bid":[7888.83,0.061314]}}

# 币安：https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT