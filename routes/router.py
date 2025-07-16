from helpers.get_bybit_http import get_client
import pandas as pd
import numpy as np
import datetime as dt 
import time
import mplfinance as mpf
import matplotlib.pyplot as plt


# For Demo trading
client = get_client(testnet=True)

# print(client)
# For Live Trading
# client = get_client(testnet=False)
# result = client.get_tickers(category='linear')

# tickers = result.get('result', {}).get('list', [])

# ticker_df = pd.DataFrame(tickers)

# print(ticker_df.head())
response = client.get_kline(category='linear', 
                            symbol='ETHUSDT', 
                            interval='D').get('result', {}).get('list', [])

def format_data(data_list) -> pd.DataFrame:

    if not data_list:
        return pd.DataFrame()
    
    data = pd.DataFrame(data_list,
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
    data.index = pd.to_datetime(data.timestamp.astype(np.int64), unit='ms', utc=True)
    return data[::-1].apply(pd.to_numeric)

df = format_data(response)

# print(df)
def get_last_timestamp(df):
    return int(df.timestamp[-1:].values[0])

start = int(dt.datetime(2022, 1, 1, tzinfo=dt.timezone.utc).timestamp()* 1000)

interval = 15
symbol = 'BTCUSDT'
# df = pd.DataFrame()

# while True:
#     response = client.get_kline(category='linear', 
#                                 symbol=symbol, 
#                                 start=start,
#                                 interval=interval, limit=1000)
    
#     latest = format_data(response.get('result', {}).get('list',[]))
#     start = get_last_timestamp(latest)
#     time.sleep(0.01)
#     df = pd.concat([df, latest])
#     print(f'Collecting data starting {dt.datetime.fromtimestamp(start/1000)}')
#     if len(latest) == 1: break


# df.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)


days_look_back = 3 * 24* 4 # 4 15 mins in 1 hour, 24 hours in 1 day , plot 7 days

ohlc_df = df[['open', 'high', 'low', 'close', 'volume']][-days_look_back:]
# ## save the data to csv
# df.to_csv('data/BTCUSDT_15min.csv', index=False)
# Plot with style
df = pd.read_csv('data/BTCUSDT_15min.csv')
df.index = pd.to_datetime(df.timestamp, unit='ms', utc=True)
df.sort_index(inplace=True)

# mpf.plot(
#     ohlc_df,
#     type='candle',
#     volume=True,
#     style='binance',
#     ylabel='Price (USDT)',
#     figratio=(6, 6),
#     figscale=1.2,
#     tight_layout=True
# )

VALID_RESAMPLE_INTERVALS = ["1min", "5min", "15min", "30min", "h", "D", "W"]


def resample_bybit_ohlc(df: pd.DataFrame, new_interval: str) -> pd.DataFrame:
    if new_interval not in VALID_RESAMPLE_INTERVALS:
        raise ValueError(
            f"'{new_interval}' is not a valid interval. Must be one of {VALID_RESAMPLE_INTERVALS}."
        )
    resampled_list = []
    agg_dict = {
        "open": "first",  # take the first price for new open
        "high": "max",  # take the max price for new high
        "low": "min",  # take the min price for new low
        "close": "last",  # take the last price for new close
        "volume": "sum",  # take sum over interval for new volume
        "turnover": "sum",  # take sum over interval for new turnover
    }
    return df.resample(new_interval).agg(agg_dict)

hourly = resample_bybit_ohlc(df=df, new_interval='h')
daily = resample_bybit_ohlc(df=df, new_interval='D')

# print(daily.tail())

# Resample the data
hourly = resample_bybit_ohlc(df=df, new_interval='h').tail(24*7)  # last 7 days of hourly
daily = resample_bybit_ohlc(df=df, new_interval='D').tail(30)     # last 30 daily candles

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4), dpi=100) 

# Plot hourly data
# mpf.plot(
#     hourly,
#     type='candle',
#     ax=ax1,
#     style='binance',
#     ylabel='Hourly Price (USDT)',
#     tight_layout=True,
#     xrotation=15
# )

# # Plot daily data
# mpf.plot(
#     daily,
#     type='candle',
#     ax=ax2,
#     style='binance',
#     ylabel='Daily Price (USDT)',
#     tight_layout=True,
#     xrotation=15
# )

# plt.tight_layout()
# plt.show()

response = client.get_open_interest(
    category="linear",
    symbol="BTCUSDT",
    intervalTime="1h",
    limit=200
).get('result', {}).get('list', [])

def format_bybit_oi(response: list[dict]) -> pd.DataFrame:
    if not response:
        return pd.DataFrame()
    df = pd.DataFrame(response)
    df['timestamp'] = df.timestamp.astype(np.int64)
    df['openInterest'] = df.openInterest.astype(float)
    df.index = pd.to_datetime(df.timestamp, unit='ms', utc=True)
    return df.sort_index()

# oi_data = format_bybit_oi(response=response)
# print(oi_data.head())

def increment_oi_timestamp(
    start_ts: int, unit: str, n_units: int
) -> int:
    increments = {
        "1min": 60 * 1000,
        "5min": 5 * 60 * 1000,
        "15min": 15 * 60 * 100,
        "30min": 30 * 60 * 1000,
        "1h": 60 * 60 * 1000,
        "4h": 4 * 60 * 60 * 100,
        "D": 24 * 60 * 60 * 1000,
    }
    new_ts = increments[unit] * n_units + start_ts
    return new_ts



start = int(dt.datetime(2022, 1, 1, tzinfo=dt.timezone.utc).timestamp()* 1000)

interval = "15min"
symbol = 'BTCUSDT'
all_oi = pd.DataFrame()
end = increment_oi_timestamp(start_ts=start, unit=interval, n_units=199)
while True:
    response = client.get_open_interest(category='linear', 
                                symbol=symbol, 
                                startTime=start,
                                endTime=end,
                                intervalTime=interval, limit=200)
    
    latest = format_bybit_oi(response.get('result', {}).get('list',[]))
    start = get_last_timestamp(latest)
    end = increment_oi_timestamp(start_ts=start, unit=interval, n_units=199)
    time.sleep(0.01)
    all_oi = pd.concat([all_oi, latest])
    print(f'Collecting data starting {dt.datetime.fromtimestamp(start/1000)}')
    if len(latest) == 1: break


all_oi.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)
all_oi.to_csv('data/BTC_USDT_OI_15min.csv', index=False)
all_oi['openInterest'].plot()
plt.xlabel('Date')
plt.ylabel('BTC Open Contracts (BTC units)')