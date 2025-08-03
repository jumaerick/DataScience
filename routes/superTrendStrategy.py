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

# print(session.get_orderbook(category='linear', symbol='DOGEUSDT')['result']['a'])
"""
Super trend indicators uses MA Aand ATR(Average True Range) to generate Sell and Buy signals.
Two parameters involved period for ATR calculation and Multiplier
ATR value calculated based on High Low and Closing prices and mulplied by the multiplier
Super trend line plotted by adding ATR value to MA for bullish trend and subraction for bearish trend
Prices above super trend consider buying or holding below consider selling
Bullish - Buy ith expectation prices will rise often 20% above recent low  investor confidence, good economic conditions.
Bearish - Sell with expectation prices will fall often 20% from a recent peak. economic uncertainities
Short Sell borrow stock from abroker sell at current price hope prices will fall but at fallen price return the borrowed stock make
profit. Usefull in hedging/
"""

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

interval = 240
symbol = 'BTCUSDT'
df = pd.DataFrame()
checker = []
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
#     print(f'Collecting data starting {dt.datetime.fromtimestamp(start/1000)}')
# df.to_csv('df.csv')

df = pd.read_csv('df.csv')

df[['SUPERT', 'direction', 'long', 'short']] = ta.supertrend(df.high,
                                                             df.low, 
                                                             df.close,
                                                             length=7, 
                                                             multiplier=3)  

# plt.style.use('ggplot')
# df.close.plot(label='close',color='black')
# df.long.dropna().plot(label='long', style='go',  markersize=1)
# df.short.dropna().plot(label='short', style='ro',  markersize=1)
# plt.ylabel('ETHUSDT')
# plt.title('Super Trend Indicator')
# plt.legend()
# # print(df.head())
# plt.show()

"""
Supertrend backtest
"""

df['return'] = df.close.pct_change()
df.dropna(subset=['return'], inplace=True)    
df['strategy'] = df.direction * df['return'].shift(-1)
df.dropna(subset=['strategy'], inplace=True)

(df['strategy']+1).cumprod().plot(label='Super Trend')
(df['close']/ df.close[:1].values[0]).plot(label='Buy and Hold')
plt.title('SuperTrend Backtest')
plt.ylabel('Cumulative Returns')
plt.legend()
plt.show()