from pybit.unified_trading import HTTP
from helpers.get_bybit_http import get_client
import pandas as pd
import pandas_ta as ta
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import json
import time
import warnings
warnings.filterwarnings("ignore", message="pkg_resources is deprecated as an API")

session = get_client(testnet=True)
def get_last_timestamp(df):
    return int(df.timestamp[-1:].values[0])

def format_data(response, interval):
    '''
    

    Parameters
    ----------
    respone : dict
        response from calling get_klines() method from pybit.

    Returns
    -------
    dataframe of ohlc data with date as index

    '''
    data = response.get('list', None)
    
    if not data:
        return 
    
    data = pd.DataFrame(data,
                        columns =[
                            'timestamp',
                            'open',
                            'high',
                            'low',
                            'close',
                            'volume',
                            'turnover'
                            ],
                        )
    
    f = lambda x: dt.datetime.utcfromtimestamp(np.int64(x)/1000)
    data.index = data.timestamp.apply(f)
    return data[::-1].apply(pd.to_numeric)



start = int(dt.datetime(2020, 1, 1).timestamp()* 1000)

interval = 'D'
symbol = 'BTCUSDT'
# df = pd.DataFrame()
# checker = []
# while True:
#     response = session.get_kline(category='linear', 
#                                  symbol=symbol, 
#                                  start=start,
#                                  interval=interval).get('result')
    
#     latest = format_data(response, interval)

    
#     if not isinstance(latest, pd.DataFrame):
#         break
#     start = get_last_timestamp(latest)
#     if(checker):
#         if(checker[-1]==start):
#             break
#     checker.append(start)
    
#     time.sleep(0.1)
    
#     df = pd.concat([df, latest])
    # print(f'Collecting data starting {dt.datetime.fromtimestamp(start/1000)}')
# df.to_csv('df.csv')
# print(df.head())

df = pd.read_csv('df.csv')
# print(df.head(20))
df[['lower_band', 'mid', 'upper_band' ]] = ta.bbands(df.close, length=20, std=2).iloc[:, :3]

# print(df[:20][['lower_band', 'mid','close' , 'upper_band' ]])


df['short_signal'] = np.where(df.close > df.upper_band, 1, 0)
df['long_signal'] = np.where(df.close < df.lower_band, 1, 0)

## lets plot the most recent 100 days
df[['lower_band', 'mid', 'close', 'upper_band']].plot(style=['k--', 'k-', 'b-', 'k--'])

plt.plot(df[df.long_signal==1]['close'], '^g')
plt.plot(df[df.short_signal==1]['close'], 'vr')
plt.title('Bollinger Bands Entries')
plt.ylabel('BTC Price USDT')
plt.show()