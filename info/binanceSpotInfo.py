"""
测试服务器连通性
响应

{}
GET /api/v3/ping

测试能否联通 Rest API。

权重(IP): 1

参数:

NONE

数据源: 缓存

获取服务器时间
响应

{
  "serverTime": 1499827319559
}
GET /api/v3/time

测试能否联通 Rest API 并 获取服务器时间。

权重(IP): 1

参数:

NONE

数据源: 缓存

交易规范信息
响应

{
    "timezone": "UTC",
    "serverTime": 1565246363776,
    "rateLimits": [
        {
            //这些在"限制种类 (rateLimitType)"下的"枚举定义"部分中定义
            //所有限制都是可选的
        }
    ],
    "exchangeFilters": [
            //这些是"过滤器"部分中定义的过滤器
            //所有限制都是可选的
    ],
    "symbols": [
        {
            "symbol": "ETHBTC",
            "status": "TRADING",
            "baseAsset": "ETH",
            "baseAssetPrecision": 8,
            "quoteAsset": "BTC",
            "quotePrecision": 8,
            "quoteAssetPrecision": 8,
            "orderTypes": [
                "LIMIT",
                "LIMIT_MAKER",
                "MARKET",
                "STOP_LOSS",
                "STOP_LOSS_LIMIT",
                "TAKE_PROFIT",
                "TAKE_PROFIT_LIMIT"
            ],
            "icebergAllowed": true,
            "ocoAllowed": true,
            "quoteOrderQtyMarketAllowed": false,
            "allowTrailingStop": false,
            "isSpotTradingAllowed": true,
            "isMarginTradingAllowed": true,
            "cancelReplaceAllowed": false,
            "filters": [
                //这些在"过滤器"部分中定义
                //所有限制都是可选的
            ],
            "permissions": [
              "SPOT",
              "MARGIN"
            ],
            "defaultSelfTradePreventionMode": "NONE",
            "allowedSelfTradePreventionModes": [
              "NONE"
            ]
        }
    ]
}



GET /api/v3/exchangeInfo

获取交易规则和交易对信息。
权重(IP): 10
参数:

有四种用法

用法	举例
不需要交易对	curl -X GET "https://api.binance.com/api/v3/exchangeInfo"
单个交易对	curl -X GET "https://api.binance.com/api/v3/exchangeInfo?symbol=BNBBTC"
多个交易对	curl -X GET "https://api.binance.com/api/v3/exchangeInfo?symbols=%5B%22BNBBTC%22,%22BTCUSDT%22%5D"

或者

curl -g -X GET 'https://api.binance.com/api/v3/exchangeInfo?symbols=["BTCUSDT","BNBBTC"]'
交易权限	curl -X GET "https://api.binance.com/api/v3/exchangeInfo?permissions=SPOT"

或者

curl -X GET "https://api.binance.com/api/v3/exchangeInfo?permissions=%5B%22MARGIN%22%2C%22LEVERAGED%22%5D"

或者

curl -g -X GET 'https://api.binance.com/api/v3/exchangeInfo?permissions=["MARGIN","LEVERAGED"]'
备注:

如果参数 symbol 或者 symbols 提供的交易对不存在, 系统会返回错误并提示交易对不正确.
所有的参数都是可选的.
permissions 支持单个或者多个值, 比如 SPOT, ["MARGIN","LEVERAGED"].
如果permissions值没有提供, 其默认值为 ["SPOT","MARGIN","LEVERAGED"].
如果想取接口 GET /api/v3/exchangeInfo 的所有交易对, 则需要设置此参数的所有可能交易权限值, 比如 permissions=["SPOT","MARGIN","LEVERAGED","TRD_GRP_002","TRD_GRP_003","TRD_GRP_004","TRD_GRP_005","TRD_GRP_006","TRD_GRP_007","TRD_GRP_008","TRD_GRP_009","TRD_GRP_010","TRD_GRP_011","TRD_GRP_012","TRD_GRP_013"])
数据源: 缓存
{
    'symbol': 'AGIXUSDT', 
    'status': 'TRADING', 
    'baseAsset': 'AGIX', 
    'baseAssetPrecision': 8, 
    'quoteAsset': 'USDT', 
    'quotePrecision': 8, 
    'quoteAssetPrecision': 8, 
    'baseCommissionPrecision': 8, 
    'quoteCommissionPrecision': 8, 
    'orderTypes': 
    [
        'LIMIT', 
        'LIMIT_MAKER', 
        'MARKET', 
        'STOP_LOSS_LIMIT', 
        'TAKE_PROFIT_LIMIT'], 
        'icebergAllowed': True, 
        'ocoAllowed': True, 
        'quoteOrderQtyMarketAllowed': True, 
        'allowTrailingStop': True, 
        'cancelReplaceAllowed': True, 
        'isSpotTradingAllowed': True, 
        'isMarginTradingAllowed': True, 
        'filters': [
            {
                'filterType': 'PRICE_FILTER', 
                'minPrice': '0.00001000', 
                'maxPrice': '1000.00000000', 
                'tickSize': '0.00001000'}, 
            {
                'filterType': 'LOT_SIZE', 
                'minQty': '1.00000000', 
                'maxQty': '92141578.00000000', 
                'stepSize': '1.00000000'},
            {
                'filterType': 'ICEBERG_PARTS', 
                'limit': 10}, 
            {
                'filterType': 'MARKET_LOT_SIZE', 
                'minQty': '0.00000000', 
                'maxQty': '1293030.89027777', 
                'stepSize': '0.00000000'}, 
            {
                'filterType': 'TRAILING_DELTA', 
                'minTrailingAboveDelta': 10, 
                'maxTrailingAboveDelta': 2000, 
                'minTrailingBelowDelta': 10, 
                'maxTrailingBelowDelta': 2000}, 
            {
                'filterType': 'PERCENT_PRICE_BY_SIDE', 
                'bidMultiplierUp': '5', 
                'bidMultiplierDown': '0.2', 
                'askMultiplierUp': '5', 
                'askMultiplierDown': '0.2', 
                'avgPriceMins': 5}, 
            {
                'filterType': 'NOTIONAL', 
                'minNotional': '10.00000000', 
                'applyMinToMarket': True, 
                'maxNotional': '9000000.00000000', 
                'applyMaxToMarket': False, 
                'avgPriceMins': 5}, 
            {
                'filterType': 'MAX_NUM_ORDERS', 
                'maxNumOrders': 200}, 
            {
                'filterType': 'MAX_NUM_ALGO_ORDERS', 
                'maxNumAlgoOrders': 5}
            ], 
        'permissions': ['SPOT', 'MARGIN'], 
        'defaultSelfTradePreventionMode': 'NONE', 
        'allowedSelfTradePreventionModes': ['NONE', 'EXPIRE_TAKER', 'EXPIRE_MAKER', 'EXPIRE_BOTH']
}, 



深度信息
响应

{
  "lastUpdateId": 1027024,
  "bids": [
    [
      "4.00000000",     // 价位
      "431.00000000"    // 挂单量
    ]
  ],
  "asks": [
    [
      "4.00000200",
      "12.00000000"
    ]
  ]
}
GET /api/v3/depth

权重(IP):

基于限制调整:

限制	权重
1-100	1
101-500	5
501-1000	10
1001-5000	50
参数:

名称	类型	是否必需	描述
symbol	STRING	YES	
limit	INT	NO	默认 100; 最大 5000. 可选值:[5, 10, 20, 50, 100, 500, 1000, 5000]

如果 limit > 5000, 最多返回5000条数据.
数据源: 缓存

近期成交列表
响应

[
  {
    "id": 28457,
    "price": "4.00000100",
    "qty": "12.00000000",
    "time": 1499865549590, // 交易成交时间, 和websocket中的T一致.
    "isBuyerMaker": true,
    "isBestMatch": true
  }
]
GET /api/v3/trades

获取近期成交

权重(IP): 1

参数:

名称	类型	是否必需	描述
symbol	STRING	YES	
limit	INT	NO	默认 500; 最大值 1000.
数据源: 缓存

查询历史成交 (MARKET_DATA)
响应

[
  {
    "id": 28457,
    "price": "4.00000100",
    "qty": "12.00000000",
    "quoteQty": "48.000012",
    "time": 1499865549590,
    "isBuyerMaker": true,
    "isBestMatch": true
  }
]
GET /api/v3/historicalTrades

获取历史成交。

权重(IP): 5

参数:

名称	类型	是否必需	描述
symbol	STRING	YES	
limit	INT	NO	默认 500; 最大值 1000.
fromId	LONG	NO	从哪一条成交id开始返回. 缺省返回最近的成交记录。
数据源: 数据库

近期成交(归集)
响应

[
  {
    "a": 26129,         // 归集成交ID
    "p": "0.01633102",  // 成交价
    "q": "4.70443515",  // 成交量
    "f": 27781,         // 被归集的首个成交ID
    "l": 27781,         // 被归集的末个成交ID
    "T": 1498793709153, // 成交时间
    "m": true,          // 是否为主动卖出单
    "M": true           // 是否为最优撮合单(可忽略，目前总为最优撮合)
  }
]
GET /api/v3/aggTrades

归集交易与逐笔交易的区别在于，同一价格、同一方向、同一时间的trade会被聚合为一条

权重(IP): 1

参数:

名称	类型	是否必需	描述
symbol	STRING	YES	
fromId	LONG	NO	从包含fromId的成交id开始返回结果
startTime	LONG	NO	从该时刻之后的成交记录开始返回结果
endTime	LONG	NO	返回该时刻为止的成交记录
limit	INT	NO	默认 500; 最大 1000.
如果没有发送任何筛选参数(fromId, startTime,endTime)，默认返回最近的成交记录
如果一个trade有下面的值，表示这是一个重复的记录，并被标记为无效(invalid):
p = '0' // price
q = '0' // qty
f = -1 // ﬁrst_trade_id
l = -1 // last_trade_id
数据源: 数据库

K线数据
响应

[
  [
    1499040000000,      // k线开盘时间
    "0.01634790",       // 开盘价
    "0.80000000",       // 最高价
    "0.01575800",       // 最低价
    "0.01577100",       // 收盘价(当前K线未结束的即为最新价)
    "148976.11427815",  // 成交量
    1499644799999,      // k线收盘时间
    "2434.19055334",    // 成交额
    308,                // 成交笔数
    "1756.87402397",    // 主动买入成交量
    "28.46694368",      // 主动买入成交额
    "17928899.62484339" // 请忽略该参数
  ]
]
GET /api/v3/klines

每根K线代表一个交易对。
每根K线的开盘时间可视为唯一ID

权重(IP): 1

参数:

名称	类型	是否必需	描述
symbol	STRING	YES	
interval	ENUM	YES	详见枚举定义：K线间隔
startTime	LONG	NO	
endTime	LONG	NO	
limit	INT	NO	默认 500; 最大 1000.
如果未发送 startTime 和 endTime ，默认返回最近的交易。
数据源: 数据库

当前平均价格
响应

{
  "mins": 5,
  "price": "9.35751834"
}
GET /api/v3/avgPrice

权重(IP): 1

参数:

名称	类型	是否必需	描述
symbol	STRING	YES	
数据源: 缓存

UIK线数据
响应

[
  [
    1499040000000,      // k线开盘时间
    "0.01634790",       // 开盘价
    "0.80000000",       // 最高价
    "0.01575800",       // 最低价
    "0.01577100",       // 收盘价(当前K线未结束的即为最新价)
    "148976.11427815",  // 成交量
    1499644799999,      // k线收盘时间
    "2434.19055334",    // 成交额
    308,                // 成交笔数
    "1756.87402397",    // 主动买入成交量
    "28.46694368",      // 主动买入成交额
    "0" // 请忽略该参数
  ]
]
GET /api/v3/uiKlines

请求参数与响应和k线接口相同。

uiKlines 返回修改后的k线数据，针对k线图的呈现进行了优化。

权重(IP): 1

参数:

名称	类型	是否必需	描述
symbol	STRING	YES	
interval	ENUM	YES	
startTime	LONG	NO	
endTime	LONG	NO	
limit	INT	NO	默认 500; 最大 1000.
如果未发送 startTime 和 endTime ，默认返回最近的交易。
数据源: 数据库

24hr 价格变动情况
响应 - FULL

{
  "symbol": "BNBBTC",
  "priceChange": "-94.99999800",
  "priceChangePercent": "-95.960",
  "weightedAvgPrice": "0.29628482",
  "prevClosePrice": "0.10002000",
  "lastPrice": "4.00000200",
  "lastQty": "200.00000000",
  "bidPrice": "4.00000000",
  "bidQty": "100.00000000",
  "askPrice": "4.00000200",
  "askQty": "100.00000000",
  "openPrice": "99.00000000",
  "highPrice": "100.00000000",
  "lowPrice": "0.10000000",
  "volume": "8913.30000000",
  "quoteVolume": "15.30000000",
  "openTime": 1499783499040,
  "closeTime": 1499869899040,
  "firstId": 28385,   // 首笔成交id
  "lastId": 28460,    // 末笔成交id
  "count": 76         // 成交笔数
}
OR

[
  {
    "symbol": "BNBBTC",
    "priceChange": "-94.99999800",
    "priceChangePercent": "-95.960",
    "weightedAvgPrice": "0.29628482",
    "prevClosePrice": "0.10002000",
    "lastPrice": "4.00000200",
    "lastQty": "200.00000000",
    "bidPrice": "4.00000000",
    "bidQty": "100.00000000",
    "askPrice": "4.00000200",
    "askQty": "100.00000000",
    "openPrice": "99.00000000",
    "highPrice": "100.00000000",
    "lowPrice": "0.10000000",
    "volume": "8913.30000000",
    "quoteVolume": "15.30000000",
    "openTime": 1499783499040,
    "closeTime": 1499869899040,
    "firstId": 28385,  
    "lastId": 28460,   
    "count": 76      
  }
]
Response - MINI

{
  "symbol":      "BNBBTC",          // 交易对
  "openPrice":   "99.00000000",     // 间隔开盘价
  "highPrice":   "100.00000000",    // 间隔最高价
  "lowPrice":    "0.10000000",      // 间隔最低价
  "lastPrice":   "4.00000200",      // 间隔收盘价
  "volume":      "8913.30000000",   // 总交易量 (base asset)
  "quoteVolume": "15.30000000",     // 总交易量 (quote asset)
  "openTime":    1499783499040,     // ticker间隔的开始时间
  "closeTime":   1499869899040,     // ticker间隔的结束时间
  "firstId":     28385,             // 统计时间内的第一笔trade id
  "lastId":      28460,             // 统计时间内的最后一笔trade id
  "count":       76                 // 统计时间内交易笔数
}
OR

[
  {
    "symbol": "BNBBTC",
    "openPrice": "99.00000000",
    "highPrice": "100.00000000",
    "lowPrice": "0.10000000",
    "lastPrice": "4.00000200",
    "volume": "8913.30000000",
    "quoteVolume": "15.30000000",
    "openTime": 1499783499040,
    "closeTime": 1499869899040,
    "firstId": 28385,
    "lastId": 28460,
    "count": 76
  },
  {
    "symbol": "LTCBTC",
    "openPrice": "0.07000000",
    "highPrice": "0.07000000",
    "lowPrice": "0.07000000",
    "lastPrice": "0.07000000",
    "volume": "11.00000000",
    "quoteVolume": "0.77000000",
    "openTime": 1656908192899,
    "closeTime": 1656994592899,
    "firstId": 0,
    "lastId": 10,
    "count": 11
  }
]
GET /api/v3/ticker/24hr

24 小时滚动窗口价格变动数据。 请注意，不携带symbol参数会返回全部交易对数据，不仅数据庞大，而且权重极高

权重(IP):

参数	提供Symbol数量	权重
symbol	1	1
不提供symbol	40
symbols	1-20	1
21-100	20
>= 101	40
不提供symbol	40
参数:

名称	类型	是否强制要求	详情
symbol	STRING	NO	参数 `symbol` 和 `symbols` 不可以一起使用

如果都不提供, 所有symbol的ticker数据都会返回.



symbols参数可接受的格式： ["BTCUSDT","BNBUSDT"]

或

%5B%22BTCUSDT%22,%22BNBUSDT%22%5D
symbols	STRING	NO
type	ENUM	NO	可接受的参数: FULL or MINI.

如果不提供, 默认值为 FULL
数据源: 缓存

最新价格
响应

{
  "symbol": "LTCBTC",
  "price": "4.00000200"
}
OR

[
  {
    "symbol": "LTCBTC",
    "price": "4.00000200"
  },
  {
    "symbol": "ETHBTC",
    "price": "0.07946600"
  }
]
GET /api/v3/ticker/price

获取交易对最新价格

权重(IP):

参数	Symbols数量	权重
symbol	1	1
不提供symbol	2
symbols	不限	2
参数:

参数名	类型	是否强制	详情
symbol	STRING	NO	参数 `symbol` 和 `symbols` 不可以一起使用

如果都不提供, 所有symbol的价格数据都会返回.



symbols参数可接受的格式： ["BTCUSDT","BNBUSDT"]

或

%5B%22BTCUSDT%22,%22BNBUSDT%22%5D
symbols	STRING	NO
不发送交易对参数，则会返回所有交易对信息
数据源: 缓存

当前最优挂单
响应

{
  "symbol": "LTCBTC",
  "bidPrice": "4.00000000",
  "bidQty": "431.00000000",
  "askPrice": "4.00000200",
  "askQty": "9.00000000"
}
OR

[
  {
    "symbol": "LTCBTC",
    "bidPrice": "4.00000000",
    "bidQty": "431.00000000",
    "askPrice": "4.00000200",
    "askQty": "9.00000000"
  },
  {
    "symbol": "ETHBTC",
    "bidPrice": "0.07946700",
    "bidQty": "9.00000000",
    "askPrice": "100000.00000000",
    "askQty": "1000.00000000"
  }
]
GET /api/v3/ticker/bookTicker

返回当前最优的挂单(最高买单，最低卖单)

权重(IP):

参数	Symbols数量	权重
symbol	1	1
不提供symbol	2
symbols	不限	2
参数:

参数名	类型	是否强制	详情
symbol	STRING	NO	参数 `symbol` 和 `symbols` 不可以一起使用

如果都不提供, 所有symbol的价格数据都会返回.



symbols参数可接受的格式： ["BTCUSDT","BNBUSDT"]

或

%5B%22BTCUSDT%22,%22BNBUSDT%22%5D
symbols	STRING	NO
数据源: 缓存

滚动窗口价格变动统计
响应 - FULL

{
  "symbol":             "BNBBTC",
  "priceChange":        "-8.00000000",  // 价格变化
  "priceChangePercent": "-88.889",      // 价格变化百分比
  "weightedAvgPrice":   "2.60427807",  
  "openPrice":          "9.00000000",
  "highPrice":          "9.00000000",
  "lowPrice":           "1.00000000",
  "lastPrice":          "1.00000000",
  "volume":             "187.00000000",
  "quoteVolume":        "487.00000000",
  "openTime":           1641859200000,  // ticker的开始时间
  "closeTime":          1642031999999,  // ticker的结束时间
  "firstId":            0,              // 统计时间内的第一笔trade id
  "lastId":             60,
  "count":              61              // 统计时间内交易笔数
}

或者

[
  {
    "symbol": "BTCUSDT",
    "priceChange": "-154.13000000",
    "priceChangePercent": "-0.740",
    "weightedAvgPrice": "20677.46305250",
    "openPrice": "20825.27000000",
    "highPrice": "20972.46000000",
    "lowPrice": "20327.92000000",
    "lastPrice": "20671.14000000",
    "volume": "72.65112300",
    "quoteVolume": "1502240.91155513",
    "openTime": 1655432400000,
    "closeTime": 1655446835460,
    "firstId": 11147809,
    "lastId": 11149775,
    "count": 1967
  },
  {
    "symbol": "BNBBTC",
    "priceChange": "0.00008530",
    "priceChangePercent": "0.823",
    "weightedAvgPrice": "0.01043129",
    "openPrice": "0.01036170",
    "highPrice": "0.01049850",
    "lowPrice": "0.01033870",
    "lastPrice": "0.01044700",
    "volume": "166.67000000",
    "quoteVolume": "1.73858301",
    "openTime": 1655432400000,
    "closeTime": 1655446835460,
    "firstId": 2351674,
    "lastId": 2352034,
    "count": 361
  }
]
响应 - MINI

{
    "symbol": "LTCBTC",
    "openPrice": "0.10000000",
    "highPrice": "2.00000000",
    "lowPrice": "0.10000000",
    "lastPrice": "2.00000000",
    "volume": "39.00000000",
    "quoteVolume": "13.40000000",  // 此k线内所有交易的price(价格) x volume(交易量)的总和
    "openTime": 1656986580000,     // ticker窗口的开始时间
    "closeTime": 1657001016795,    // ticker窗口的结束时间
    "firstId": 0,                  // 首笔成交id
    "lastId": 34,
    "count": 35                    // 统计时间内交易笔数
}
OR

[
    {
        "symbol": "BNBBTC",
        "openPrice": "0.10000000",
        "highPrice": "2.00000000",
        "lowPrice": "0.10000000",
        "lastPrice": "2.00000000",
        "volume": "39.00000000",
        "quoteVolume": "13.40000000", // 此k线内所有交易的price(价格) x volume(交易量)的总和
        "openTime": 1656986880000,    // ticker窗口的开始时间
        "closeTime": 1657001297799,   // ticker窗口的结束时间
        "firstId": 0,                 // 首笔成交id
        "lastId": 34,
        "count": 35                   // 统计时间内交易笔数
    },
    {
        "symbol": "LTCBTC",
        "openPrice": "0.07000000",
        "highPrice": "0.07000000",
        "lowPrice": "0.07000000",
        "lastPrice": "0.07000000",
        "volume": "33.00000000",
        "quoteVolume": "2.31000000",
        "openTime": 1656986880000,
        "closeTime": 1657001297799,
        "firstId": 0,
        "lastId": 32,
        "count": 33
    }
]
GET /api/v3/ticker

注意: 此接口和 GET /api/v3/ticker/24hr 有所不同.

此接口统计的时间范围比请求的windowSize多不超过59999ms.

接口的 openTime 是某一分钟的起始，而结束是当前的时间. 所以实际的统计区间会比请求的时间窗口多不超过59999ms.

比如, 结束时间 closeTime 是 1641287867099 (January 04, 2022 09:17:47:099 UTC) , windowSize 为 1d. 那么开始时间 openTime 则为 1641201420000 (January 3, 2022, 09:17:00 UTC)

权重(IP): 2/交易对.



如果symbols请求的交易对超过50, 上限是100.

参数

Name	Type	Mandatory	Description
symbol	STRING	YES	提供 symbol或者symbols 其中之一

symbols 可以传入的格式:

["BTCUSDT","BNBUSDT"]

or

%5B%22BTCUSDT%22,%22BNBUSDT%22%5D



symbols 允许最多100个交易对
symbols
windowSize	ENUM	NO	默认为 1d

windowSize 支持的值:

如果是分钟: 1m,2m....59m

如果是小时: 1h, 2h....23h

如果是天: 1d...7d



不可以组合使用, 比如1d2h
type	ENUM	NO	可接受的参数: FULL or MINI.

如果不提供, 默认值为 FULL
数据源: 数据库


"""