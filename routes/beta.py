import pandas as pd
import datetime as dt
from pybit.unified_trading import HTTP
import matplotlib.pyplot as plt
import numpy as np
import time
from scipy.stats import linregress
#Beta of an asset is calculated as a ratio of an asset against a base asset
#if 1.5 for ETH agaist BTC it means by 1% change in BTC the prices of ETC will change by 1.5%
#ETH is more volatile 
#When hedging, you choose to go long on BTC and short on ETH
#You regress the price of an asset against another
#Buy BTC and shorting ETH
session = HTTP(testnet=True)

def format_data(response):
    '''
    

    Parameters
    ----------
    respone : dict
        response from calling get_klines() method from pybit.
    freq : str
        DESCRIPTION.
        interval that has been passed in to get_klines method, used in order
        to round the datetimes, which will be mapped to pandas freq str

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
    
    f = lambda x: dt.datetime.utcfromtimestamp(int(x)/1000)
    data.index = data.timestamp.apply(f)
    return data[::-1].apply(pd.to_numeric)

def get_last_timestamp(df):
    return int(df.timestamp[-1:].values[0])
    
def get_all_data(sym, interval):
    
    start = int(dt.datetime(2020, 1, 1).timestamp()* 1000) 
    df = pd.DataFrame()
    while True:
        response = session.get_kline(category='linear', 
                                     symbol=sym, 
                                     start=start,
                                     interval=interval).get('result')
        
        latest = format_data(response)
        
        if not isinstance(latest, pd.DataFrame):
            break
        
        start = get_last_timestamp(latest)
        
        time.sleep(0.1)
        
        df = pd.concat([df, latest])
        print(f'Collecting data starting {dt.datetime.fromtimestamp(start/1000)}')
        if len(latest) == 1: break
    
    return df

interval   = 'D'
symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT', 'DOGEUSDT', 'MATICUSDT', 'SOLUSDT', 'DOTUSDT',
               'LTCUSDT']

dfs = []

for symbol in symbols:
    data = get_all_data(symbol, interval)
    dfs.append(data)

df = pd.DataFrame(data=dfs[0].close)
print(df.head())

for data in dfs[1:]:
    print(pd.DataFrame(data.close))
    df = pd.merge(df, pd.DataFrame(data.close), left_index=True, right_index=True, suffixes = ['','_right'])
df.to_csv('beta.csv')
# df = pd.read_csv('beta.csv')
df.columns = symbols  
df =df[~df.index.duplicated(keep='last')]
# df.to_csv('beta.csv')


returns = df.pct_change().dropna()
result = linregress(returns.BTCUSDT.values, returns.ETHUSDT.values)

# slope, intercept, r_value, p_value, std_err = linregress(x, y)
print(f'Beta for eth regressed on btc is {result.slope}')
# print(f'Beta for eth regressed on btc is {result.slope}')
beta = result.slope

eth_short = 10_000
btc_long = eth_short*beta
print(f'longing {btc_long} worth of BTC')

strat = (df[(df.index >= dt.datetime(2022, 9, 1)) & (df.index < dt.datetime(2022, 10,1)) ])[['BTCUSDT', 'ETHUSDT']].pct_change().dropna()

strat['eth_strat_returns'] = (strat.ETHUSDT+1).cumprod()
strat['btc_strat_returns'] = (strat.BTCUSDT + 1).cumprod() 
strat['combined_returns'] = ((strat.ETHUSDT*-1)+ (strat.BTCUSDT*beta))
strat['strategy_returns'] = (strat.combined_returns+1).cumprod()
# strat[['eth_strat_returns','btc_strat_returns', 'strategy_returns' ]].plot()
# plt.plot(strat[['eth_strat_returns','btc_strat_returns', 'strategy_returns' ]])
# plt.show()

returns_cov = returns.cov() / np.diag(returns.cov())

returns_cov.to_csv('returns_csv.csv')
for sym in symbols:
    result = linregress(returns.BTCUSDT.values, returns[sym].values)
    print(f'Beta for {sym} regressed on btc is {result.slope}')
