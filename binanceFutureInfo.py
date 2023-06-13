"""
测试服务器连通性 PING
GET /dapi/v1/ping

响应:

{}
测试能否联通

权重: 1

参数: NONE

获取服务器时间
响应:

{
  "serverTime": 1499827319559 // 当前的系统时间
}
GET /dapi/v1/time

获取服务器时间

权重: 1

参数: NONE

获取交易规则和交易对
响应:

{
    "exchangeFilters": [],
    "rateLimits": [ // API访问的限制
        {
            "interval": "MINUTE", // 按照分钟计算
            "intervalNum": 1, // 按照1分钟计算
            "limit": 2400, // 上限次数
            "rateLimitType": "REQUEST_WEIGHT" // 按照访问权重来计算
        },
        {
            "interval": "MINUTE",
            "intervalNum": 1,
            "limit": 1200,
            "rateLimitType": "ORDERS" // 按照订单数量来计算
        }
    ],
    "serverTime": 1565613908500, // 请忽略。如果需要获取系统时间，请查询接口 “GET /dapi/v1/time”
    "symbols": [ // 交易对信息
        {
            "filters": [
                {
                    "filterType": "PRICE_FILTER", // 价格限制
                    "maxPrice": "100000", // 价格上限, 最大价格
                    "minPrice": "0.1", // 价格下限, 最小价格
                    "tickSize": "0.1" // 下单最小价格间隔
                },
                {
                    "filterType": "LOT_SIZE", // 数量限制
                    "maxQty": "100000", // 数量上限, 最大数量
                    "minQty": "1", // 数量下限, 最小数量
                    "stepSize": "1" // 下单最小数量间隔
                },
                {
                    "filterType": "MARKET_LOT_SIZE", // 市价订单数量限制
                    "maxQty": "100000", // 数量上限, 最大数量
                    "minQty": "1", // 数量下限, 最小数量
                    "stepSize": "1" // 允许的步进值
                },
                {
                    "filterType": "MAX_NUM_ORDERS", // 最多挂单数限制
                    "limit": 200
                },
                {
                    "filterType": "PERCENT_PRICE", // 价格比限制
                    "multiplierUp": "1.0500", // 价格上限百分比
                    "multiplierDown": "0.9500", // 价格下限百分比
                    "multiplierDecimal": 4
                }
            ],
            "OrderType": [ // 订单类型
                "LIMIT",  // 限价单
                "MARKET",  // 市价单
                "STOP", // 止损单
                "TAKE_PROFIT", // 止盈单
                "TRAILING_STOP_MARKET" // 跟踪止损单
            ],
            "timeInForce": [ // 有效方式
                "GTC", // 成交为止, 一直有效
                "IOC", // 无法立即成交(吃单)的部分就撤销
                "FOK", // 无法全部立即成交就撤销
                "GTX" // 无法成为挂单方就撤销
            ],
            "liquidationFee": "0.010000",   // 强平费率
            "marketTakeBound": "0.30",  // 市价吃单(相对于标记价格)允许可造成的最大价格偏离比例
            "symbol": "BTCUSD_200925", // 交易对
            "pair": "BTCUSD",   // 标的交易对
            "contractType": "CURRENT_QUARTER",   // 合约类型
            "deliveryDate": 1601020800000,
            "onboardDate": 1590739200000,
            "contractStatus": "TRADING", // 交易对状态
            "contractSize": 100,     //
            "quoteAsset": "USD", // 报价币种
            "baseAsset": "BTC",  // 标的物
            "marginAsset": "BTC",   // 保证金币种
            "pricePrecision": 1,   // 价格小数点位数(仅作为系统精度使用，注意同tickSize 区分)
            "quantityPrecision": 0, // 数量小数点位数(仅作为系统精度使用，注意同stepSize 区分)
            "baseAssetPrecision": 8,
            "quotePrecision": 8,
            "equalQtyPrecision": 4,     // 请忽略
            "triggerProtect": "0.0500", // 开启"priceProtect"的条件订单的触发阈值
            "maintMarginPercent": "2.5000", // 请忽略
            "requiredMarginPercent": "5.0000", // 请忽略
            "underlyingType": "COIN",  // 标的类型
            "underlyingSubType": []     // 标的物子类型
        }
    ],
    "timezone": "UTC" // 服务器所用的时间区域
}

GET /dapi/v1/exchangeInfo

获取交易规则和交易对

权重: 1

参数: NONE

深度信息
响应:

{
  "lastUpdateId": 16769853,
  "symbol": "BTCUSD_PERP", // 交易对
  "pair": "BTCUSD",      // 标的交易对
  "E": 1591250106370,   // 消息时间
  "T": 1591250106368,   // 撮合时间
  "bids": [              // 买单
    [
      "9638.0",         // 价格
      "431"             // 数量
    ]
  ],
  "asks": [             // 卖单
    [
      "9638.2",         // 价格
      "12"              // 数量
    ]
  ]
}
GET /dapi/v1/depth

权重:

limit	权重
5, 10, 20, 50	2
100	5
500	10
1000	20
参数:

名称	类型	是否必需	描述
symbol	STRING	YES	交易对
limit	INT	NO	默认 500; 可选值:[5, 10, 20, 50, 100, 500, 1000]
近期成交
响应:

[
  {
    "id": 28457,                // 成交ID
    "price": "9635.0",          // 成交价格
    "qty": "1",                 // 成交量(张数)
    "baseQty": "0.01037883",    // 成交额(标的数量)
    "time": 1591250192508,      // 时间
    "isBuyerMaker": true        // 买方是否为挂单方
  }
]
GET /dapi/v1/trades

获取近期订单簿成交

权重: 5

参数:

名称	类型	是否必需	描述
symbol	STRING	YES	交易对
limit	INT	NO	默认值:500 最大值:1000.
仅返回订单簿成交，即不会返回保险基金和自动减仓(ADL)成交
查询历史成交 (MARKET_DATA)
响应:

[
  {
    "id": 595103,               // 成交ID
    "price": "9642.2",          // 成交价格
    "qty": "1",                 // 成交量(张数)
    "baseQty": "0.01037108",    // 成交额(标的物数量)
    "time": 1499865549590,      // 时间
    "isBuyerMaker": true        // 买方是否为挂单方
  }
]
GET /dapi/v1/historicalTrades

查询订单簿历史成交

权重: 20

参数:

名称	类型	是否必需	描述
symbol	STRING	YES	交易对
limit	INT	NO	默认值:500 最大值:1000.
fromId	LONG	NO	从哪一条成交id开始返回. 缺省返回最近的成交记录
仅返回订单簿成交，即不会返回保险基金和自动减仓(ADL)成交
近期成交(归集)
响应:

[
  {
    "a": 416690,            // 归集成交ID
    "p": "9642.4",          // 成交价
    "q": "3",               // 成交量
    "f": 595259,            // 被归集的首个成交ID
    "l": 595259,            // 被归集的末个成交ID
    "T": 1591250548649,     // 成交时间
    "m": true,              // 是否为主动卖出单
  }
]
GET /dapi/v1/aggTrades

归集交易与逐笔交易的区别在于,同一价格、同一方向、同一时间(100ms计算)的订单簿trade会被聚合为一条

权重: 20

参数:

名称	类型	是否必需	描述
symbol	STRING	YES	交易对
fromId	LONG	NO	从包含fromID的成交开始返回结果
startTime	LONG	NO	从该时刻之后的成交记录开始返回结果
endTime	LONG	NO	返回该时刻为止的成交记录
limit	INT	NO	默认 500; 最大 1000.
如果同时发送startTime和endTime，间隔必须小于一小时
如果没有发送任何筛选参数(fromId, startTime, endTime),默认返回最近的成交记录
保险基金和自动减仓(ADL)成交不属于订单簿成交，故不会被归并聚合
同时发送startTime/endTime和fromId可能导致请求超时，建议仅发送fromId或仅发送startTime和endTime
最新现货指数价格和Mark Price
响应:

[
    {
        "symbol": "BTCUSD_PERP",    // 交易对
        "pair": "BTCUSD",           // 基础标的
        "markPrice": "11029.69574559",  // 标记价格
        "indexPrice": "10979.14437500", // 指数价格
        "estimatedSettlePrice": "10981.74168236",  // 预估结算价,仅在交割开始前最后一小时有意义
        "lastFundingRate": "0.00071003",      // 最近更新的资金费率,只对永续合约有效，其他合约返回""
        "interestRate": "0.00010000",       // 标的资产基础利率,只对永续合约有效，其他合约返回""
        "nextFundingTime": 1596096000000,    // 下次资金费时间，只对永续合约有效，其他合约返回0
        "time": 1596094042000   // 更新时间
    },
    {
        "symbol": "BTCUSD_200925",  
        "pair": "BTCUSD",
        "markPrice": "12077.01343750",
        "indexPrice": "10979.10312500",
        "estimatedSettlePrice": "10981.74168236",
        "lastFundingRate": "",
        "interestRate": "",
        "nextFundingTime": 0,
        "time": 1596094042000
    }
]
GET /dapi/v1/premiumIndex

权重: 10

参数:

名称	类型	是否必需	描述
symbol	STRING	NO	交易对
pair	STRING	NO	标的交易对
查询永续合约资金费率历史
响应:

[
    {
        "symbol": "BTCUSD_PERP",    // 交易对
        "fundingTime": 1596038400000,   // 资金费时间
        "fundingRate": "-0.00300000"    // 资金费率
    },
    {
        "symbol": "BTCUSD_PERP",
        "fundingTime": 1596067200000,
        "fundingRate": "-0.00300000"
    }
]
GET /dapi/v1/fundingRate

权重: 1

参数:

名称	类型	是否必需	描述
symbol	STRING	YES	交易对
startTime	LONG	NO	起始时间
endTime	LONG	NO	结束时间
limit	INT	NO	默认值:100 最大值:1000
对非永续合约，将返回空列表
K线数据
响应:

[
  [
    1591258320000,      // 开盘时间
    "9640.7",           // 开盘价
    "9642.4",           // 最高价
    "9640.6",           // 最低价
    "9642.0",           // 收盘价(当前K线未结束的即为最新价)
    "206",              // 成交量
    1591258379999,      // 收盘时间
    "2.13660389",       // 成交额(标的数量)
    48,                 // 成交笔数
    "119",              // 主动买入成交量
    "1.23424865",       // 主动买入成交额(标的数量)
    "0"                 // 请忽略该参数
  ]
]
GET /dapi/v1/klines 每根K线的开盘时间可视为唯一ID

权重: 取决于请求中的LIMIT参数

LIMIT参数	权重
[1,100)	1
[100, 500)	2
[500, 1000]	5
> 1000	10
参数:

名称	类型	是否必需	描述
symbol	STRING	YES	交易对
interval	ENUM	YES	时间间隔
startTime	LONG	NO	起始时间
endTime	LONG	NO	结束时间
limit	INT	NO	默认值:500 最大值:1500
startTime 与 endTime 之间最多只可以相差200天
默认返回 startTime 与 endTime 之间最接近 endTime的 limit 条数据:

startTime, endTime 均未提供的, 将会使用当前时间为 endTime, 200天前为 startTime
仅提供 startTime 的, 将会使用 startTime 之后200天作为默认 endTime (至多为当前时间)
仅提供 endTime 的, 将会使用endTime 之前200天作为默认 startTime
订阅Kline需要提供间隔参数,最短为分钟线,最长为月线。支持以下间隔:
m -> 分钟; h -> 小时; d -> 天; w -> 周; M -> 月

1m
3m
5m
15m
30m
1h
2h
4h
6h
8h
12h
1d
3d
1w
1M
连续合约K线数据
响应:

[
  [
    1591258320000,      // 开盘时间
    "9640.7",           // 开盘价
    "9642.4",           // 最高价
    "9640.6",           // 最低价
    "9642.0",           // 收盘价(当前K线未结束的即为最新价)
    "206",              // 成交量
    1591258379999,      // 收盘时间
    "2.13660389",       // 成交额(标的数量)
    48,                 // 成交笔数
    "119",              // 主动买入成交量
    "1.23424865",       // 主动买入成交额(标的数量)
    "0"                 // 请忽略该参数
  ]
]
GET /dapi/v1/continuousKlines 每根K线的开盘时间可视为唯一ID

权重: 取决于请求中的LIMIT参数

LIMIT参数	权重
[1,100)	1
[100, 500)	2
[500, 1000]	5
> 1000	10
参数:

名称	类型	是否必需	描述
pair	STRING	YES	标的交易对
contractType	ENUM	YES	合约类型
interval	ENUM	YES	时间间隔
startTime	LONG	NO	起始时间
endTime	LONG	NO	结束时间
limit	INT	NO	默认值:500 最大值:1500
startTime 与 endTime 之间最多只可以相差200天
默认返回 startTime 与 endTime 之间最接近 endTime的 limit 条数据:

startTime, endTime 均未提供的, 将会使用当前时间为 endTime, 200天前为 startTime
仅提供 startTime 的, 将会使用 startTime 之后200天作为默认 endTime (至多为当前时间)
仅提供 endTime 的, 将会使用endTime 之前200天作为默认 startTime
合约类型:

PERPETUAL 永续合约
CURRENT_QUARTER 当季交割合约
NEXT_QUARTER 次季交割合约
价格指数K线数据
响应:

[
  [
    1591256400000,          // 开盘时间
    "9653.69440000",        // 开盘价
    "9653.69640000",        // 最高价
    "9651.38600000",        // 最低价
    "9651.55200000",        // 收盘价(当前K线未结束的即为最新价)
    "0  ",                  // 请忽略
    1591256459999,          // 收盘时间
    "0",                    // 请忽略
    60,                     // 构成记录数
    "0",                    // 请忽略
    "0",                    // 请忽略
    "0"                     // 请忽略
  ]
]
GET /dapi/v1/indexPriceKlines

每根K线的开盘时间可视为唯一ID

权重: 取决于请求中的LIMIT参数

LIMIT参数	权重
[1,100)	1
[100, 500)	2
[500, 1000]	5
> 1000	10
参数:

名称	类型	是否必需	描述
pair	STRING	YES	标的交易对
interval	ENUM	YES	时间间隔
startTime	LONG	NO	起始时间
endTime	LONG	NO	结束时间
limit	INT	NO	默认值:500 最大值:1500
startTime 与 endTime 之间最多只可以相差200天
默认返回 startTime 与 endTime 之间最接近 endTime的 limit 条数据:
startTime, endTime 均未提供的, 将会使用当前时间为 endTime, 200天前为 startTime
仅提供 startTime 的, 将会使用 startTime 之后200天作为默认 endTime (至多为当前时间)
仅提供 endTime 的, 将会使用endTime 之前200天作为默认 startTime
标记价格K线数据
响应:

[
  [
    1591256400000,          // 开盘时间
    "9653.69440000",        // 开盘价
    "9653.69640000",        // 最高价
    "9651.38600000",        // 最低价
    "9651.55200000",        // 收盘价(当前K线未结束的即为最新价)
    "0  ",                  // 请忽略
    1591256459999,          // 收盘时间
    "0",                    // 请忽略
    60,                     // 构成记录数
    "0",                    // 请忽略
    "0",                    // 请忽略
    "0"                     // 请忽略
  ]
]
GET /dapi/v1/markPriceKlines 每根K线的开盘时间可视为唯一ID

权重: 取决于请求中的LIMIT参数

LIMIT参数	权重
[1,100)	1
[100, 500)	2
[500, 1000]	5
> 1000	10
参数:

名称	类型	是否必需	描述
symbol	STRING	YES	交易对
interval	ENUM	YES	时间间隔
startTime	LONG	NO	起始时间
endTime	LONG	NO	结束时间
limit	INT	NO	默认值:500 最大值:1500
startTime 与 endTime 之间最多只可以相差200天
默认返回 startTime 与 endTime 之间最接近 endTime的 limit 条数据:
startTime, endTime 均未提供的, 将会使用当前时间为 endTime, 200天前为 startTime
仅提供 startTime 的, 将会使用 startTime 之后200天作为默认 endTime (至多为当前时间)
仅提供 endTime 的, 将会使用endTime 之前200天作为默认 startTime
24hr价格变动情况
响应:

[
    {
        "symbol": "BTCUSD_200925",
        "pair": "BTCUSD",
        "priceChange": "136.6",             //24小时价格变动
        "priceChangePercent": "1.436",  //24小时价格变动百分比
        "weightedAvgPrice": "9547.3",       //24小时加权平均价
        "lastPrice": "9651.6",              //最近一次成交价
        "lastQty": "1",                     //最近一次成交量
        "openPrice": "9515.0",              //24小时内第一次成交的价格
        "highPrice": "9687.0",              //24小时最高价
        "lowPrice": "9499.5",               //24小时最低价
        "volume": "494109",                 //24小时成交量
        "baseVolume": "5192.94797687",  //24小时成交额(标的数量)
        "openTime": 1591170300000,          //24小时内,第一笔交易的发生时间
        "closeTime": 1591256718418,     //24小时内,最后一笔交易的发生时间
        "firstId": 600507,                  // 首笔成交id
        "lastId": 697803,                   // 末笔成交id
        "count": 97297                      // 成交笔数     
    }
]
GET /dapi/v1/ticker/24hr

请注意,不携带symbol参数会返回全部交易对数据,不仅数据庞大,而且权重极高

权重:

带symbol为1
不带为40
参数:

名称	类型	是否必需	描述
symbol	STRING	NO	交易对
pair	STRING	NO	标的交易对
symbol 和 pair 不接受同时发送
发送 pair的,返回pair对应所有正在交易的symbol数据
symbol,pair 都没有发送的,返回所有symbol数据
最新价格
响应:

[
    {
        "symbol": "BTCUSD_200626",  // 交易对
        "ps": "BTCUSD",             // 标的交易对
        "price": "9647.8",          // 价格
        "time": 1591257246176       // 时间
    }
]
GET /dapi/v1/ticker/price

返回最近价格

权重:

单交易对1
多交易对2
参数:

名称	类型	是否必需	描述
symbol	STRING	NO	交易对
pair	STRING	NO	标的交易对
symbol 和 pair 不接受同时发送
发送 pair的,返回pair对应所有正在交易的symbol数据
symbol,pair 都没有发送的,返回所有symbol数据
当前最优挂单
响应:

[
    {
        "symbol": "BTCUSD_200626",  // 交易对
        "pair": "BTCUSD",           // 标的交易对
        "bidPrice": "9650.1",       //最优买单价
        "bidQty": "16",             //最优买单挂单量
        "askPrice": "9650.3",       //最优卖单价
        "askQty": "7",              //最优卖单挂单量
        "time": 1591257300345
    }
]
GET /dapi/v1/ticker/bookTicker

返回当前最优的挂单(最高买单,最低卖单)

权重: * 单交易对2
* 无交易对5

参数:

名称	类型	是否必需	描述
symbol	STRING	NO	交易对
pair	STRING	NO	标的交易对
symbol 和 pair 不接受同时发送
发送 pair的,返回pair对应所有正在交易的symbol数据
symbol,pair 都没有发送的,返回所有symbol数据
获取未平仓合约数
响应:

{
    "symbol": "BTCUSD_200626",
    "pair": "BTCUSD",
    "openInterest": "15004",
    "contractType": "CURRENT_QUARTER",
    "time": 1591261042378
}

GET /dapi/v1/openInterest

权重: 1

参数:

名称	类型	是否必需	描述
symbol	STRING	YES	交易对
合约持仓量
响应:

[  
   {
      "pair": "BTCUSD",
      "contractType": "CURRENT_QUARTER",
      "sumOpenInterest": "20403",  //unit: cont
      "sumOpenInterestValue": "176196512.23400000", //unit: base asset
      "timestamp": 1591261042378
   },
   {
     "pair": "BTCUSD",
      "contractType": "CURRENT_QUARTER",
      "sumOpenInterest": "20401",  
      "sumOpenInterestValue": "176178704.98700000", 
      "timestamp": 1583128200000
   }
]
GET /futures/data/openInterestHist

权重: 1

参数:

名称	类型	是否必需	描述
pair	STRING	YES	BTCUSD
contractType	ENUM	YES	ALL, CURRENT_QUARTER, NEXT_QUARTER, PERPETUAL
period	ENUM	YES	"5m","15m","30m","1h","2h","4h","6h","12h","1d"
limit	LONG	NO	Default 30,Max 500
startTime	LONG	NO	
endTime	LONG	NO	
若无 startime 和 endtime 限制， 则默认返回当前时间往前的limit值
仅支持最近30天的数据
大户账户数多空比
响应:

[  
   {
      "pair": "BTCUSD",
      "longShortRatio": "1.8105",
      "longAccount": "0.6442",  //64.42%
      "shortAccount": "0.3558",  //35.58%
      "timestamp": 1591261042378
   },
   {
     "pair": "BTCUSD",
      "longShortRatio": "1.1110",
      "longAccount": "0.5263",  
      "shortAccount": "0.4737",  
      "timestamp": 1592870400000
    }
]
GET /futures/data/topLongShortAccountRatio

权重: 1

参数:

名称	类型	是否必需	描述
pair	STRING	YES	BTCUSD
period	ENUM	YES	"5m","15m","30m","1h","2h","4h","6h","12h","1d"
limit	LONG	NO	Default 30,Max 500
startTime	LONG	NO	
endTime	LONG	NO	
若无 startime 和 endtime 限制， 则默认返回当前时间往前的limit值
仅支持最近30天的数据
大户持仓量多空比
响应:

[  
   {
      "pair": "BTCUSD",
      "longShortRatio": "0.7869",
      "longPosition": "0.6442",  //64.42%
      "shortPosition": "0.4404",  //44.04%
      "timestamp": 1592870400000
   },
   {
     "pair": "BTCUSD",
      "longShortRatio": "1.1231",
      "longPosition": "0.2363",  
      "shortPosition": "0.4537",  
      "timestamp": 1592956800000
    }
]
GET /futures/data/topLongShortPositionRatio

权重: 1

参数:

名称	类型	是否必需	描述
pair	STRING	YES	BTCUSD
period	ENUM	YES	"5m","15m","30m","1h","2h","4h","6h","12h","1d"
limit	LONG	NO	Default 30,Max 500
startTime	LONG	NO	
endTime	LONG	NO	
若无 startime 和 endtime 限制， 则默认返回当前时间往前的limit值
仅支持最近30天的数据
多空持仓人数比
响应:

[  
   {
      "pair": "BTCUSD",
      "longShortRatio": "0.1960",
      "longAccount": "0.6622",  //66.22%
      "shortAccount": "0.3378",  //33.78%
      "timestamp": 1583139600000
   },
   {
     "pair": "BTCUSD",
      "longShortRatio": "1.9559",
      "longAccount": "0.6617",  
      "shortAccount": "0.3382",  
      "timestamp": 1583139900000
    }
]
GET /futures/data/globalLongShortAccountRatio

权重: 1

参数:

名称	类型	是否必需	描述
pair	STRING	YES	BTCUSD
period	ENUM	YES	"5m","15m","30m","1h","2h","4h","6h","12h","1d"
limit	LONG	NO	Default 30,Max 500
startTime	LONG	NO	
endTime	LONG	NO	
若无 startime 和 endtime 限制， 则默认返回当前时间往前的limit值
仅支持最近30天的数据
合约主动买卖量
响应:

[  
   {
      "pair": "BTCUSD",
      "contractType": CURRENT_QUARTER,
      "takerBuyVol": "387",  //unit: cont
      "takerSellVol": "248",  //unit: cont
      "takerBuyVolValue": "2342.1220", //unit: base asset
      "takerSellVolValue": "4213.9800", //unit: base asset
      "timestamp": 1591261042378
   },
   {
     "pair": "BTCUSD",
      "contractType": CURRENT_QUARTER,
      "takerBuyVol": "234",  //unit: cont
      "takerSellVol": "121",  //unit: cont
      "takerBuyVolValue": "4563.1320", //unit: base asset
      "takerSellVolValue": "3313.3940", //unit: base asset
      "timestamp": 1585615200000
   }
]
GET /futures/data/takerBuySellVol

权重: 1

参数:

名称	类型	是否必需	描述
pair	STRING	YES	BTCUSD
contractType	ENUM	YES	ALL, CURRENT_QUARTER, NEXT_QUARTER, PERPETUAL
period	ENUM	YES	"5m","15m","30m","1h","2h","4h","6h","12h","1d"
limit	LONG	NO	Default 30,Max 500
startTime	LONG	NO	
endTime	LONG	NO	
若无 startime 和 endtime 限制， 则默认返回当前时间往前的limit值
仅支持最近30天的数据
基差
响应:

[  
   {
        "indexPrice": "29269.93972727",
        "contractType": "CURRENT_QUARTER",
        "basisRate": "0.0024",
        "futuresPrice": "29341.3",
        "annualizedBasisRate": "0.0283",
        "basis": "71.36027273",
        "pair": "BTCUSD",
        "timestamp": 1653381600000
   }
]
GET /futures/data/basis

权重: 1

参数:

名称	类型	是否必需	描述
pair	STRING	YES	BTCUSD
contractType	ENUM	YES	CURRENT_QUARTER, NEXT_QUARTER, PERPETUAL
period	ENUM	YES	"5m","15m","30m","1h","2h","4h","6h","12h","1d"
limit	LONG	NO	Default 30,Max 500
startTime	LONG	NO	
endTime	LONG	NO	
若无 startime 和 endtime 限制， 则默认返回当前时间往前的limit值
仅支持最近30天的数据
"""