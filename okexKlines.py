import pandas as pd
import ccxt
import time
import os
from datetime import timedelta

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# =====设定参数
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

binance = ccxt.binance({
    'proxies': proxies
})

def get_binance_klines(symbol, time_interval, start_time, end_time):
    start_time_since = binance.parse8601(start_time) #parse8601（），用于将 ISO 8601 格式的时间字符串转换为 Unix 时间戳
    end_time_since = binance.parse8601(end_time)

    # =====循环获取数据
    df_list = []
    all_kline_data = []

    while True:
        params = {
            'symbol': symbol,
            'interval': time_interval,
            'startTime': start_time_since, #如果未发送 startTime 和 endTime ，默认返回最近的交易。
            'endTime': end_time_since,
            'limit': 1000,
        }  

        kline_data = binance.publicGetKlines(params=params)

        df = pd.DataFrame(kline_data, dtype=float)  # 将数据转换为dataframe #缺少这两行代码
        df_list.append(df)  #缺少这两行代码
        #print(df.shape[0])
        if df.shape[0] > 1:
            start_time_since = kline_data[-1][0]  # 更新since，为下次循环做准备
            all_kline_data += kline_data
        else:
            break

        # 抓取间隔需要暂停2s，防止抓取过于频繁
        time.sleep(2)
  
    # 对数据进行整理
    df = pd.concat(df_list, ignore_index=True)
    df.rename(columns={0: 'MTS', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume',6:'kline_close_time',7:'quote_asset_volume',8:'number_of_trades',9:'taker_buy_base_asset_volume',10:'taker_buy_quote_asset_volume'}, inplace=True)
    df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms') 
    df = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume','kline_close_time','quote_asset_volume','number_of_trades','taker_buy_base_asset_volume','taker_buy_quote_asset_volume']]

    df_group = df.groupby(pd.to_datetime(df['candle_begin_time']).dt.date, as_index=False)
    for day, df in df_group:
        df.drop_duplicates(subset=['candle_begin_time'], keep='last', inplace=True)
        df.sort_values('candle_begin_time', inplace=True)
        df.reset_index(drop=True, inplace=True)
   
        # =====保存数据到文件
        if df.shape[0] > 0:
            # 根目录，确保该路径存在
            path = '/Volumes/USB-DISK/PythonProjects/coin_data'

            # 创建交易所文件夹
            path = os.path.join(path, binance.id)
            if os.path.exists(path) is False:
                os.mkdir(path)
            # 创建spot文件夹
            path = os.path.join(path, 'spot')
            if os.path.exists(path) is False:
                os.mkdir(path)
            # 创建交易对文件夹
            path = os.path.join(path, symbol)
            if os.path.exists(path) is False:
                os.mkdir(path)
            # 创建频次文件夹
            path = os.path.join(path, time_interval)
            if os.path.exists(path) is False:
                os.mkdir(path)

            # 拼接文件目录
            file_name = '_'.join([binance.name, symbol.replace('/', '-'), str(pd.to_datetime(day)).split(' ')[0].replace('-',''),time_interval]) + '.csv'
            path = os.path.join(path, file_name)

            print(path)
            df.to_csv(path, index=False)



# =====设定参数
symbol_list = ['BTCUSDT','ETHUSDT','EOSUSDT','LTCUSDT'] 
time_interval_list = ['5m','15m']  # 其他可以尝试的值：'1m', '5m', '15m', '30m', '1H', '2H', '1D', '1W', '1M', '1Y'

# =====抓取数据开始结束时间
start_time = '2022-12-01 00:00:00'
end_time = '2023-06-08 23:59:00'
# end_time = str(pd.to_datetime(start_time) + timedelta(days=1))

for symbol in symbol_list:
    for time_interval in time_interval_list:
        get_binance_klines(symbol, time_interval, start_time, end_time)


"""
'api': {
                # the API structure below will need 3-layer apidefs
                'sapi': {
                    # IP(api) = 1200 per minute =>(rateLimit = 50)
                    # IP(sapi) request rate limit of 12 000 per minute
                    # 1 IP(sapi) => cost = 0.1
                    # 10 IP(sapi) => cost = 1
                    # UID(sapi) request rate limit of 180 000 per minute
                    # 1 UID(sapi) => cost = 1200 / 180 000 = 0.006667
                    'get': {
                        'system/status': 0.1,
                        # these endpoints require self.apiKey
                        'accountSnapshot': 240,  # Weight(IP): 2400 => cost = 0.1 * 2400 = 240
                        'margin/asset': 1,  # Weight(IP): 10 => cost = 0.1 * 10 = 1
                        'margin/pair': 1,
                        'margin/allAssets': 0.1,
                        'margin/allPairs': 0.1,
                        'margin/priceIndex': 1,
                        # these endpoints require self.apiKey + self.secret
                        'asset/assetDividend': 1,
                        'asset/dribblet': 0.1,
                        'asset/transfer': 0.1,
                        'asset/assetDetail': 0.1,
                        'asset/tradeFee': 0.1,
                        'asset/ledger-transfer/cloud-mining/queryByPage': 4,
                        'asset/convert-transfer/queryByPage': 0.033335,
                        'margin/loan': 1,
                        'margin/repay': 1,
                        'margin/account': 1,
                        'margin/transfer': 0.1,
                        'margin/interestHistory': 0.1,
                        'margin/forceLiquidationRec': 0.1,
                        'margin/order': 1,
                        'margin/openOrders': 1,
                        'margin/allOrders': 20,  # Weight(IP): 200 => cost = 0.1 * 200 = 20
                        'margin/myTrades': 1,
                        'margin/maxBorrowable': 5,  # Weight(IP): 50 => cost = 0.1 * 50 = 5
                        'margin/maxTransferable': 5,
                        'margin/tradeCoeff': 1,
                        'margin/isolated/transfer': 0.1,
                        'margin/isolated/account': 1,
                        'margin/isolated/pair': 1,
                        'margin/isolated/allPairs': 1,
                        'margin/isolated/accountLimit': 0.1,
                        'margin/interestRateHistory': 0.1,
                        'margin/orderList': 1,
                        'margin/allOrderList': 20,  # Weight(IP): 200 => cost = 0.1 * 200 = 20
                        'margin/openOrderList': 1,
                        'margin/crossMarginData': {'cost': 0.1, 'noCoin': 0.5},
                        'margin/isolatedMarginData': {'cost': 0.1, 'noCoin': 1},
                        'margin/isolatedMarginTier': 0.1,
                        'margin/rateLimit/order': 2,
                        'margin/dribblet': 0.1,
                        'margin/crossMarginCollateralRatio': 10,
                        'margin/exchange-small-liability': 0.6667,
                        'margin/exchange-small-liability-history': 0.6667,
                        'margin/next-hourly-interest-rate': 0.6667,
                        'loan/income': 40,  # Weight(UID): 6000 => cost = 0.006667 * 6000 = 40
                        'loan/ongoing/orders': 40,  # Weight(IP): 400 => cost = 0.1 * 400 = 40
                        'loan/ltv/adjustment/history': 40,  # Weight(IP): 400 => cost = 0.1 * 400 = 40
                        'loan/borrow/history': 40,  # Weight(IP): 400 => cost = 0.1 * 400 = 40
                        'loan/repay/history': 40,  # Weight(IP): 400 => cost = 0.1 * 400 = 40
                        'loan/loanable/data': 40,  # Weight(IP): 400 => cost = 0.1 * 400 = 40
                        'loan/collateral/data': 40,  # Weight(IP): 400 => cost = 0.1 * 400 = 40
                        'loan/repay/collateral/rate': 600,  # Weight(IP): 6000 => cost = 0.1 * 6000 = 600
                        'loan/vip/ongoing/orders': 40,  # Weight(IP): 400 => cost = 0.1 * 400 = 40
                        'loan/vip/repay/history': 40,  # Weight(IP): 400 => cost = 0.1 * 400 = 40
                        'loan/vip/collateral/account': 600,  # Weight(IP): 6000 => cost = 0.1 * 6000 = 600
                        'fiat/orders': 600.03,  # Weight(UID): 90000 => cost = 0.006667 * 90000 = 600.03
                        'fiat/payments': 0.1,
                        'futures/transfer': 1,
                        'futures/loan/borrow/history': 1,
                        'futures/loan/repay/history': 1,
                        'futures/loan/wallet': 1,
                        'futures/loan/adjustCollateral/history': 1,
                        'futures/loan/liquidationHistory': 1,
                        'rebate/taxQuery': 20.001,  # Weight(UID): 3000 => cost = 0.006667 * 3000 = 20.001
                        # https://binance-docs.github.io/apidocs/spot/en/#withdraw-sapi
                        'capital/config/getall': 1,  # get networks for withdrawing USDT ERC20 vs USDT Omni
                        'capital/deposit/address': 1,
                        'capital/deposit/hisrec': 0.1,
                        'capital/deposit/subAddress': 0.1,
                        'capital/deposit/subHisrec': 0.1,
                        'capital/withdraw/history': 0.1,
                        'capital/contract/convertible-coins': 4.0002,
                        'convert/tradeFlow': 0.6667,  # Weight(UID): 100 => cost = 0.006667 * 100 = 0.6667
                        'convert/exchangeInfo': 50,
                        'convert/assetInfo': 10,
                        'convert/orderStatus': 0.6667,
                        'account/status': 0.1,
                        'account/apiTradingStatus': 0.1,
                        'account/apiRestrictions/ipRestriction': 0.1,
                        'bnbBurn': 0.1,
                        # 'sub-account/assets': 1,(v3 endpoint)
                        'sub-account/futures/account': 1,
                        'sub-account/futures/accountSummary': 0.1,
                        'sub-account/futures/positionRisk': 1,
                        'sub-account/futures/internalTransfer': 0.1,
                        'sub-account/list': 0.1,
                        'sub-account/margin/account': 1,
                        'sub-account/margin/accountSummary': 1,
                        'sub-account/spotSummary': 0.1,
                        'sub-account/status': 1,
                        'sub-account/sub/transfer/history': 0.1,
                        'sub-account/transfer/subUserHistory': 0.1,
                        'sub-account/universalTransfer': 0.1,
                        'sub-account/apiRestrictions/ipRestriction/thirdPartyList': 1,
                        'sub-account/transaction-tatistics': 0.4,
                        'managed-subaccount/asset': 0.1,
                        'managed-subaccount/accountSnapshot': 240,
                        'managed-subaccount/queryTransLogForInvestor': 0.1,
                        'managed-subaccount/queryTransLogForTradeParent': 0.1,
                        'managed-subaccount/fetch-future-asset': 0.1,
                        'managed-subaccount/marginAsset': 0.1,
                        'managed-subaccount/info': 0.4,
                        'managed-subaccount/deposit/address': 0.1,
                        # lending endpoints
                        'lending/daily/product/list': 0.1,
                        'lending/daily/userLeftQuota': 0.1,
                        'lending/daily/userRedemptionQuota': 0.1,
                        'lending/daily/token/position': 0.1,
                        'lending/union/account': 0.1,
                        'lending/union/purchaseRecord': 0.1,
                        'lending/union/redemptionRecord': 0.1,
                        'lending/union/interestHistory': 0.1,
                        'lending/project/list': 0.1,
                        'lending/project/position/list': 0.1,
                        # mining endpoints
                        'mining/pub/algoList': 0.1,
                        'mining/pub/coinList': 0.1,
                        'mining/worker/detail': 0.5,  # Weight(IP): 5 => cost = 0.1 * 5 = 0.5
                        'mining/worker/list': 0.5,
                        'mining/payment/list': 0.5,
                        'mining/statistics/user/status': 0.5,
                        'mining/statistics/user/list': 0.5,
                        'mining/payment/uid': 0.5,
                        # liquid swap endpoints
                        'bswap/pools': 0.1,
                        'bswap/liquidity': {'cost': 0.1, 'noPoolId': 1},
                        'bswap/liquidityOps': 20.001,  # Weight(UID): 3000 => cost = 0.006667 * 3000 = 20.001
                        'bswap/quote': 1.00005,  # Weight(UID): 150 => cost = 0.006667 * 150 = 1.00005
                        'bswap/swap': 20.001,  # Weight(UID): 3000 => cost = 0.006667 * 3000 = 20.001
                        'bswap/poolConfigure': 1.00005,  # Weight(UID): 150 => cost = 0.006667 * 150 = 1.00005
                        'bswap/addLiquidityPreview': 1.00005,  # Weight(UID): 150 => cost = 0.006667 * 150 = 1.00005
                        'bswap/removeLiquidityPreview': 1.00005,  # Weight(UID): 150 => cost = 0.006667 * 150 = 1.00005
                        'bswap/unclaimedRewards': 6.667,  # Weight(UID): 1000 => cost = 0.006667 * 1000 = 6.667
                        'bswap/claimedHistory': 6.667,  # Weight(UID): 1000 => cost = 0.006667 * 1000 = 6.667
                        # leveraged token endpoints
                        'blvt/tokenInfo': 0.1,
                        'blvt/subscribe/record': 0.1,
                        'blvt/redeem/record': 0.1,
                        'blvt/userLimit': 0.1,
                        # broker api TODO(NOT IN DOCS)
                        'apiReferral/ifNewUser': 1,
                        'apiReferral/customization': 1,
                        'apiReferral/userCustomization': 1,
                        'apiReferral/rebate/recentRecord': 1,
                        'apiReferral/rebate/historicalRecord': 1,
                        'apiReferral/kickback/recentRecord': 1,
                        'apiReferral/kickback/historicalRecord': 1,
                        # brokerage API TODO https://binance-docs.github.io/Brokerage-API/General/ does not state ratelimits
                        'broker/subAccountApi': 1,
                        'broker/subAccount': 1,
                        'broker/subAccountApi/commission/futures': 1,
                        'broker/subAccountApi/commission/coinFutures': 1,
                        'broker/info': 1,
                        'broker/transfer': 1,
                        'broker/transfer/futures': 1,
                        'broker/rebate/recentRecord': 1,
                        'broker/rebate/historicalRecord': 1,
                        'broker/subAccount/bnbBurn/status': 1,
                        'broker/subAccount/depositHist': 1,
                        'broker/subAccount/spotSummary': 1,
                        'broker/subAccount/marginSummary': 1,
                        'broker/subAccount/futuresSummary': 1,
                        'broker/rebate/futures/recentRecord': 1,
                        'broker/subAccountApi/ipRestriction': 1,
                        'broker/universalTransfer': 1,
                        # v2 not supported yet
                        # GET /sapi/v2/broker/subAccount/futuresSummary
                        'account/apiRestrictions': 0.1,
                        # c2c / p2p
                        'c2c/orderMatch/listUserOrderHistory': 0.1,
                        # nft endpoints
                        'nft/history/transactions': 20.001,  # Weight(UID): 3000 => cost = 0.006667 * 3000 = 20.001
                        'nft/history/deposit': 20.001,
                        'nft/history/withdraw': 20.001,
                        'nft/user/getAsset': 20.001,
                        'pay/transactions': 20.001,  # Weight(UID): 3000 => cost = 0.006667 * 3000 = 20.001
                        'giftcard/verify': 0.1,
                        'giftcard/cryptography/rsa-public-key': 0.1,
                        'giftcard/buyCode/token-limit': 0.1,
                        'algo/futures/openOrders': 0.1,
                        'algo/futures/historicalOrders': 0.1,
                        'algo/futures/subOrders': 0.1,
                        'portfolio/account': 0.1,
                        'portfolio/collateralRate': 5,
                        'portfolio/pmLoan': 3.3335,
                        'portfolio/interest-history': 0.6667,
                        'portfolio/interest-rate': 0.6667,
                        # staking
                        'staking/productList': 0.1,
                        'staking/position': 0.1,
                        'staking/stakingRecord': 0.1,
                        'staking/personalLeftQuota': 0.1,
                    },
                    'post': {
                        'asset/dust': 1,
                        'asset/dust-btc': 0.1,
                        'asset/transfer': 0.1,
                        'asset/get-funding-asset': 0.1,
                        'asset/convert-transfer': 0.033335,
                        'account/disableFastWithdrawSwitch': 0.1,
                        'account/enableFastWithdrawSwitch': 0.1,
                        # 'account/apiRestrictions/ipRestriction': 1, discontinued
                        # 'account/apiRestrictions/ipRestriction/ipList': 1, discontinued
                        'capital/withdraw/apply': 4.0002,  # Weight(UID): 600 => cost = 0.006667 * 600 = 4.0002
                        'capital/contract/convertible-coins': 4.0002,
                        'margin/transfer': 1,  # Weight(IP): 600 => cost = 0.1 * 600 = 60
                        'margin/loan': 20.001,  # Weight(UID): 3000 => cost = 0.006667 * 3000 = 20.001
                        'margin/repay': 20.001,
                        'margin/order': 0.040002,  # Weight(UID): 6 => cost = 0.006667 * 6 = 0.040002
                        'margin/order/oco': 0.040002,
                        'margin/exchange-small-liability': 20.001,
                        # 'margin/isolated/create': 1, discontinued
                        'margin/isolated/transfer': 4.0002,  # Weight(UID): 600 => cost = 0.006667 * 600 = 4.0002
                        'margin/isolated/account': 2.0001,  # Weight(UID): 300 => cost = 0.006667 * 300 = 2.0001
                        'bnbBurn': 0.1,
                        'sub-account/virtualSubAccount': 0.1,
                        'sub-account/margin/transfer': 4.0002,  # Weight(UID): 600 => cost =  0.006667 * 600 = 4.0002
                        'sub-account/margin/enable': 0.1,
                        'sub-account/futures/enable': 0.1,
                        'sub-account/futures/transfer': 0.1,
                        'sub-account/futures/internalTransfer': 0.1,
                        'sub-account/transfer/subToSub': 0.1,
                        'sub-account/transfer/subToMaster': 0.1,
                        'sub-account/universalTransfer': 0.1,
                        # v2 not supported yet
                        # 'sub-account/subAccountApi/ipRestriction': 20,
                        'managed-subaccount/deposit': 0.1,
                        'managed-subaccount/withdraw': 0.1,
                        'userDataStream': 0.1,
                        'userDataStream/isolated': 0.1,
                        'futures/transfer': 0.1,
                        # lending
                        'lending/customizedFixed/purchase': 0.1,
                        'lending/daily/purchase': 0.1,
                        'lending/daily/redeem': 0.1,
                        # liquid swap endpoints
                        'bswap/liquidityAdd': 60,  # Weight(UID): 1000 + (Additional: 1 request every 3 seconds =  0.333 requests per second) => cost = ( 1000 / rateLimit ) / 0.333 = 60.0000006
                        'bswap/liquidityRemove': 60,  # Weight(UID): 1000 + (Additional: 1 request every three seconds)
                        'bswap/swap': 60,  # Weight(UID): 1000 + (Additional: 1 request every three seconds)
                        'bswap/claimRewards': 6.667,  # Weight(UID): 1000 => cost = 0.006667 * 1000 = 6.667
                        # leveraged token endpoints
                        'blvt/subscribe': 0.1,
                        'blvt/redeem': 0.1,
                        # brokerage API TODO: NO MENTION OF RATELIMITS IN BROKERAGE DOCS
                        'apiReferral/customization': 1,
                        'apiReferral/userCustomization': 1,
                        'apiReferral/rebate/historicalRecord': 1,
                        'apiReferral/kickback/historicalRecord': 1,
                        'broker/subAccount': 1,
                        'broker/subAccount/margin': 1,
                        'broker/subAccount/futures': 1,
                        'broker/subAccountApi': 1,
                        'broker/subAccountApi/permission': 1,
                        'broker/subAccountApi/commission': 1,
                        'broker/subAccountApi/commission/futures': 1,
                        'broker/subAccountApi/commission/coinFutures': 1,
                        'broker/transfer': 1,
                        'broker/transfer/futures': 1,
                        'broker/rebate/historicalRecord': 1,
                        'broker/subAccount/bnbBurn/spot': 1,
                        'broker/subAccount/bnbBurn/marginInterest': 1,
                        'broker/subAccount/blvt': 1,
                        'broker/subAccountApi/ipRestriction': 1,
                        'broker/subAccountApi/ipRestriction/ipList': 1,
                        'broker/universalTransfer': 1,
                        'broker/subAccountApi/permission/universalTransfer': 1,
                        'broker/subAccountApi/permission/vanillaOptions': 1,
                        #
                        'giftcard/createCode': 0.1,
                        'giftcard/redeemCode': 0.1,
                        'giftcard/buyCode': 0.1,
                        'algo/futures/newOrderVp': 20.001,
                        'algo/futures/newOrderTwap': 20.001,
                        # staking
                        'staking/purchase': 0.1,
                        'staking/redeem': 0.1,
                        'staking/setAutoStaking': 0.1,
                        'portfolio/repay': 20.001,
                        'loan/borrow': 40,  # Weight(UID): 6000 => cost = 0.006667 * 6000 = 40
                        'loan/repay': 40,  # Weight(UID): 6000 => cost = 0.006667 * 6000 = 40
                        'loan/adjust/ltv': 40,  # Weight(UID): 6000 => cost = 0.006667 * 6000 = 40
                        'loan/customize/margin_call': 40,  # Weight(UID): 6000 => cost = 0.006667 * 6000 = 40
                        'loan/vip/repay': 40,  # Weight(UID): 6000 => cost = 0.006667 * 6000 = 40
                        'convert/getQuote': 20.001,
                        'convert/acceptQuote': 3.3335,
                    },
                    'put': {
                        'userDataStream': 0.1,
                        'userDataStream/isolated': 0.1,
                    },
                    'delete': {
                        # 'account/apiRestrictions/ipRestriction/ipList': 1, discontinued
                        'margin/openOrders': 0.1,
                        'margin/order': 0.0066667,  # Weight(UID): 1 => cost = 0.006667
                        'margin/orderList': 0.0066667,
                        'margin/isolated/account': 2.0001,  # Weight(UID): 300 => cost =  0.006667 * 300 = 2.0001
                        'userDataStream': 0.1,
                        'userDataStream/isolated': 0.1,
                        # brokerage API TODO NO MENTION OF RATELIMIT IN BROKERAGE DOCS
                        'broker/subAccountApi': 1,
                        'broker/subAccountApi/ipRestriction/ipList': 1,
                        'algo/futures/order': 0.1,
                    },
                },
                'sapiV2': {
                    'get': {
                        'sub-account/futures/account': 0.1,
                        'sub-account/futures/positionRisk': 0.1,
                    },
                },
                'sapiV3': {
                    'get': {
                        'sub-account/assets': 1,
                    },
                    'post': {
                        'asset/getUserAsset': 0.5,
                    },
                },
                'sapiV4': {
                    'get': {
                        'sub-account/assets': 1,
                    },
                },
                # deprecated
                'wapi': {
                    'post': {
                        'withdraw': 1,
                        'sub-account/transfer': 1,
                    },
                    'get': {
                        'depositHistory': 1,
                        'withdrawHistory': 1,
                        'depositAddress': 1,
                        'accountStatus': 1,
                        'systemStatus': 1,
                        'apiTradingStatus': 1,
                        'userAssetDribbletLog': 1,
                        'tradeFee': 1,
                        'assetDetail': 1,
                        'sub-account/list': 1,
                        'sub-account/transfer/history': 1,
                        'sub-account/assets': 1,
                    },
                },
                'dapiPublic': {
                    'get': {
                        'ping': 1,
                        'time': 1,
                        'exchangeInfo': 1,
                        'depth': {'cost': 2, 'byLimit': [[50, 2], [100, 5], [500, 10], [1000, 20]]},
                        'trades': 5,
                        'historicalTrades': 20,
                        'aggTrades': 20,
                        'premiumIndex': 10,
                        'fundingRate': 1,
                        'klines': {'cost': 1, 'byLimit': [[99, 1], [499, 2], [1000, 5], [10000, 10]]},
                        'continuousKlines': {'cost': 1, 'byLimit': [[99, 1], [499, 2], [1000, 5], [10000, 10]]},
                        'indexPriceKlines': {'cost': 1, 'byLimit': [[99, 1], [499, 2], [1000, 5], [10000, 10]]},
                        'markPriceKlines': {'cost': 1, 'byLimit': [[99, 1], [499, 2], [1000, 5], [10000, 10]]},
                        'ticker/24hr': {'cost': 1, 'noSymbol': 40},
                        'ticker/price': {'cost': 1, 'noSymbol': 2},
                        'ticker/bookTicker': {'cost': 1, 'noSymbol': 2},
                        'openInterest': 1,
                        'pmExchangeInfo': 1,
                    },
                },
                'dapiData': {
                    'get': {
                        'openInterestHist': 1,
                        'topLongShortAccountRatio': 1,
                        'topLongShortPositionRatio': 1,
                        'globalLongShortAccountRatio': 1,
                        'takerBuySellVol': 1,
                        'basis': 1,
                    },
                },
                'dapiPrivate': {
                    'get': {
                        'positionSide/dual': 30,
                        'order': 1,
                        'openOrder': 1,
                        'openOrders': {'cost': 1, 'noSymbol': 5},
                        'allOrders': {'cost': 20, 'noSymbol': 40},
                        'balance': 1,
                        'account': 5,
                        'positionMargin/history': 1,
                        'positionRisk': 1,
                        'userTrades': {'cost': 20, 'noSymbol': 40},
                        'income': 20,
                        'leverageBracket': 1,
                        'forceOrders': {'cost': 20, 'noSymbol': 50},
                        'adlQuantile': 5,
                        'orderAmendment': 1,
                        'pmAccountInfo': 5,
                    },
                    'post': {
                        'positionSide/dual': 1,
                        'order': 4,
                        'batchOrders': 5,
                        'countdownCancelAll': 10,
                        'leverage': 1,
                        'marginType': 1,
                        'positionMargin': 1,
                        'listenKey': 1,
                    },
                    'put': {
                        'listenKey': 1,
                        'order': 1,
                        'batchOrders': 5,
                    },
                    'delete': {
                        'order': 1,
                        'allOpenOrders': 1,
                        'batchOrders': 5,
                        'listenKey': 1,
                    },
                },
                'dapiPrivateV2': {
                    'get': {
                        'leverageBracket': 1,
                    },
                },
                'fapiPublic': {
                    'get': {
                        'ping': 1,
                        'time': 1,
                        'exchangeInfo': 1,
                        'depth': {'cost': 2, 'byLimit': [[50, 2], [100, 5], [500, 10], [1000, 20]]},
                        'trades': 5,
                        'historicalTrades': 20,
                        'aggTrades': 20,
                        'klines': {'cost': 1, 'byLimit': [[99, 1], [499, 2], [1000, 5], [10000, 10]]},
                        'continuousKlines': {'cost': 1, 'byLimit': [[99, 1], [499, 2], [1000, 5], [10000, 10]]},
                        'markPriceKlines': {'cost': 1, 'byLimit': [[99, 1], [499, 2], [1000, 5], [10000, 10]]},
                        'indexPriceKlines': {'cost': 1, 'byLimit': [[99, 1], [499, 2], [1000, 5], [10000, 10]]},
                        'fundingRate': 1,
                        'premiumIndex': 1,
                        'ticker/24hr': {'cost': 1, 'noSymbol': 40},
                        'ticker/price': {'cost': 1, 'noSymbol': 2},
                        'ticker/bookTicker': {'cost': 1, 'noSymbol': 2},
                        'openInterest': 1,
                        'indexInfo': 1,
                        'apiTradingStatus': {'cost': 1, 'noSymbol': 10},
                        'lvtKlines': 1,
                        'pmExchangeInfo': 1,
                    },
                },
                'fapiData': {
                    'get': {
                        'openInterestHist': 1,
                        'topLongShortAccountRatio': 1,
                        'topLongShortPositionRatio': 1,
                        'globalLongShortAccountRatio': 1,
                        'takerlongshortRatio': 1,
                    },
                },
                'fapiPrivate': {
                    'get': {
                        'forceOrders': {'cost': 20, 'noSymbol': 50},
                        'allOrders': 5,
                        'openOrder': 1,
                        'openOrders': 1,
                        'order': 1,
                        'account': 5,
                        'balance': 5,
                        'leverageBracket': 1,
                        'positionMargin/history': 1,
                        'positionRisk': 5,
                        'positionSide/dual': 30,
                        'userTrades': 5,
                        'income': 30,
                        'commissionRate': 20,
                        'apiTradingStatus': 1,
                        'multiAssetsMargin': 30,
                        # broker endpoints
                        'apiReferral/ifNewUser': 1,
                        'apiReferral/customization': 1,
                        'apiReferral/userCustomization': 1,
                        'apiReferral/traderNum': 1,
                        'apiReferral/overview': 1,
                        'apiReferral/tradeVol': 1,
                        'apiReferral/rebateVol': 1,
                        'apiReferral/traderSummary': 1,
                        'adlQuantile': 5,
                        'pmAccountInfo': 5,
                    },
                    'post': {
                        'batchOrders': 5,
                        'positionSide/dual': 1,
                        'positionMargin': 1,
                        'marginType': 1,
                        'order': 4,
                        'leverage': 1,
                        'listenKey': 1,
                        'countdownCancelAll': 10,
                        'multiAssetsMargin': 1,
                        # broker endpoints
                        'apiReferral/customization': 1,
                        'apiReferral/userCustomization': 1,
                    },
                    'put': {
                        'listenKey': 1,
                    },
                    'delete': {
                        'batchOrders': 1,
                        'order': 1,
                        'allOpenOrders': 1,
                        'listenKey': 1,
                    },
                },
                'fapiPrivateV2': {
                    'get': {
                        'account': 1,
                        'balance': 1,
                        'positionRisk': 1,
                    },
                },
                'eapiPublic': {
                    'get': {
                        'ping': 1,
                        'time': 1,
                        'exchangeInfo': 1,
                        'index': 1,
                        'ticker': 5,
                        'mark': 5,
                        'depth': 1,
                        'klines': 1,
                        'trades': 5,
                        'historicalTrades': 20,
                        'exerciseHistory': 3,
                        'openInterest': 3,
                    },
                },
                'eapiPrivate': {
                    'get': {
                        'account': 3,
                        'position': 5,
                        'openOrders': {'cost': 1, 'noSymbol': 40},
                        'historyOrders': 3,
                        'userTrades': 5,
                        'exerciseRecord': 5,
                        'bill': 1,
                        'marginAccount': 3,
                        'mmp': 1,
                        'countdownCancelAll': 1,
                        'order': 1,
                    },
                    'post': {
                        'order': 1,
                        'batchOrders': 5,
                        'listenKey': 1,
                        'mmpSet': 1,
                        'mmpReset': 1,
                        'countdownCancelAll': 1,
                        'countdownCancelAllHeartBeat': 10,
                    },
                    'put': {
                        'listenKey': 1,
                    },
                    'delete': {
                        'order': 1,
                        'batchOrders': 1,
                        'allOpenOrders': 1,
                        'allOpenOrdersByUnderlying': 1,
                        'listenKey': 1,
                    },
                },
                'public': {
                    'get': {
                        'ping': 1,
                        'time': 1,
                        'depth': {'cost': 1, 'byLimit': [[100, 1], [500, 5], [1000, 10], [5000, 50]]},
                        'trades': 1,
                        'aggTrades': 1,
                        'historicalTrades': 5,
                        'klines': 1,
                        'ticker/24hr': {'cost': 1, 'noSymbol': 40},
                        'ticker/price': {'cost': 1, 'noSymbol': 2},
                        'ticker/bookTicker': {'cost': 1, 'noSymbol': 2},
                        'exchangeInfo': 10,
                    },
                    'put': {
                        'userDataStream': 1,
                    },
                    'post': {
                        'userDataStream': 1,
                    },
                    'delete': {
                        'userDataStream': 1,
                    },
                },
                'private': {
                    'get': {
                        'allOrderList': 10,  # oco
                        'openOrderList': 3,  # oco
                        'orderList': 2,  # oco
                        'order': 2,
                        'openOrders': {'cost': 3, 'noSymbol': 40},
                        'allOrders': 10,
                        'account': 10,
                        'myTrades': 10,
                        'rateLimit/order': 20,
                        'myPreventedMatches': 1,
                    },
                    'post': {
                        'order/oco': 1,
                        'order': 1,
                        'order/cancelReplace': 1,
                        'order/test': 1,
                    },
                    'delete': {
                        'openOrders': 1,  # added on 2020-04-25 for canceling all open orders per symbol
                        'orderList': 1,  # oco
                        'order': 1,
                    },
                },
            },
"""