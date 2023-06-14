import pandas as pd
import requests
import time

class BinanceFutureVersusSpot(object):
    def __init__(self,timeout=5):
        self.future_base_url=  'https://dapi.binance.com' # 不翻墙可改为'https://dapi.binancezh.co'
        self.spot_base_url = 'https://api.binance.com'  # 不翻墙可改为'https://api.binancezh.co'
        self.timeout = timeout

    def get_symbol_list(self,url):
        response_data = requests.get(url, timeout=self.timeout).json()
        info = pd.DataFrame(response_data['symbols'])
        return list(info['symbol'])

    def get_price(self, symbol, url, limit=5):
        full_url = url + '?' + "symbol=" + symbol + '&limit=' + str(limit)
        data = requests.get(full_url, timeout=self.timeout).json()
        price = float(data['asks'][0][0])
        return round(price, 2)

    def spot_symbols(self):
        return self.get_symbol_list(url = self.spot_base_url + '/api/v3/exchangeInfo')

    def future_symbols(self):
        return self.get_symbol_list(url=self.future_base_url + '/dapi/v1/exchangeInfo')

    def spot_price(self, symbol):
        return self.get_price(url=self.spot_base_url + '/api/v3/depth',symbol=symbol)

    def future_price(self, symbol):
        return self.get_price(url=self.future_base_url +'/dapi/v1/depth',symbol=symbol)
    
def get_future_price(symbol):
    url = 'https://dapi.binance.com/dapi/v1/depth?symbol=%s&limit=5'%(symbol)
    #print(url)
    prices = requests.get(url).json()
    return prices['asks'][0][0]

def get_spot_price(symbol):
    url = 'https://api.binance.com/api/v3/depth?symbol=%s&limit=5'%(symbol)
    prices = requests.get(url).json()
    return prices['asks'][0][0]

while True: 
    df = pd.DataFrame(requests.get('https://dapi.binance.com/dapi/v1/exchangeInfo').json()['symbols'])
    df = df[['symbol','baseAsset','contractType','contractStatus']]
    df = df[df['contractStatus'] == 'TRADING']  # 只选取交易中的合约
    df = df[df['contractType'] != 'PERPETUAL'].reset_index(drop=True)   # 只选取有交割日期的合约
    #df = df[df['contractType'] == 'CURRENT_QUARTER'].reset_index(drop=True)   # 只选取当季交割日期的合约
    #df = df[df['contractType'] == 'NEXT_QUARTER'].reset_index(drop=True)   # 只选取次季交割日期的合约
    #df = df[['symbol','baseAsset']]

    df = df.rename(columns={'symbol':'future','baseAsset':'spot'})
    df['spot'] = df['spot'] + 'USDT'
    df['future_price'] = df['future'].apply(get_future_price)
    df['future_price'] = df['future_price'].astype(float)
    df['spot_price'] = df['spot'].apply(get_spot_price)
    df['spot_price'] = df['spot_price'].astype(float)
    
    # 计算价差并排序
    df['diff'] = (df['future_price'] - df['spot_price'])/df['spot_price']
    df['diff(%)'] =round(df['diff']*100,2)
    df.sort_values(by='diff(%)', inplace=True,ascending=False)
    #df.set_index('spot',inplace=True)

    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    print('*'*50)
    print(df)

    time.sleep(180)

    # # spot_list = spot_df[spot_df['quoteAsset']== 'USDT']['symbol'].tolist()
    # # print(spot_list)
    # # exit()
    # engine = BinanceFutureVersusSpot() # 启动这个类
    # spot_list = engine.spot_symbols()  # 获取所有的spot交易对
    # future_list= engine.future_symbols() #获取所有的币本位future交易对
    # df = pd.DataFrame()

    # # 传入合约名称列
    # df['future'] = future_list

    # # 将合约名称修改尾缀，改为现货名称的格式，生成现货列
    # spot = future_list.copy()
    # for i in range(0,len(spot)):
    #     new = spot[i].split('_')[0]
    #     spot[i] = new.replace('USD', 'USDT')
    # df['spot'] = spot

    # # 获取合约价格
    # for symbol in future_list:
    #     df.loc[df['future'] ==symbol,'future_price'] = engine.future_price(symbol=symbol)

    # #获取现货价格
    # for symbol in spot_list:  # 选取原始现货币对
    #     if symbol in spot:  # 再选取其同在合约中的币对，这里的spot是前面的future改尾缀生成的
    #         df.loc[df['spot']==symbol,'spot_price'] = engine.spot_price(symbol=symbol)

    # # 计算价差并排序
    # df['diff'] = (df['future_price']-df['spot_price'])/df['spot_price']
    # df['diff(%)'] =round(df['diff']*100,2)
    # df.sort_values(by='diff(%)', inplace=True,ascending=False)
    # df.set_index('spot',inplace=True)

    # print(time.strftime('%Y-%m-%d %H:%M:%S'))
    # print('*'*50)
    # print(df)

    # time.sleep(180)


