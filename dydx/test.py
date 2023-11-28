from dydx3 import Client
import pandas as pd
# from web3 import Web3

#
# Access public API endpoints.
#

public_client = Client(
    host='https://api.dydx.exchange',
    # web3=Web3('...'),
    # stark_private_key='01234abcd...',
)

markets = public_client.public.get_markets().data['markets']
markets_pd = pd.DataFrame.from_dict(markets, orient='index')
print(markets_pd)
exit()
"""
{'CELO-USD':{
    'market': 'CELO-USD', 
    'status': 'ONLINE', 
    'baseAsset': 'CELO', 
    'quoteAsset': 'USD', 
    'stepSize': '1', 
    'tickSize': '0.001', 
    'indexPrice': '0.5060', 
    'oraclePrice': '0.5060', 
    'priceChange24H': '-0.018829', 
    'nextFundingRate': '0.0000151179', 
    'nextFundingAt': '2023-11-28T06:00:00.000Z', 
    'minOrderSize': '10', 
    'type': 'PERPETUAL', 
    'initialMarginFraction': '0.50', 
    'maintenanceMarginFraction': '0.05', 
    'transferMarginFraction': '0.019237', 
    'volume24H': '2711188.233000', 
    'trades24H': '3090', 
    'openInterest': '520119', 
    'incrementalInitialMarginFraction': '0.02', 
    'incrementalPositionSize': '17700', 
    'maxPositionSize': '355000', 
    'baselinePositionSize': '35500', 
    'assetResolution': '1000000', 
    'syntheticAssetId': '0x43454c4f2d36000000000000000000'
}
"""
