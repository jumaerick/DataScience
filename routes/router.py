from helpers.get_bybit_http import get_client
import pandas as pd
import numpy as np
import datetime as dt 
import time
import mplfinance as mpf
import matplotlib.pyplot as plt
import time


# For Demo trading
client = get_client(testnet=True)
# server_time = client.get_server_time()
# print(client)


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

# hourly = resample_bybit_ohlc(df=df, new_interval='h')
# daily = resample_bybit_ohlc(df=df, new_interval='D')

# print(daily.tail())

# Resample the data
# hourly = resample_bybit_ohlc(df=df, new_interval='h').tail(24*7)  # last 7 days of hourly
# daily = resample_bybit_ohlc(df=df, new_interval='D').tail(30)     # last 30 daily candles

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4), dpi=100) 

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

# response = client.get_open_interest(
#     category="linear",
#     symbol="BTCUSDT",
#     intervalTime="1h",
#     limit=200
# ).get('result', {}).get('list', [])

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

# interval = "15min"
# symbol = 'BTCUSDT'
# all_oi = pd.DataFrame()
# end = increment_oi_timestamp(start_ts=start, unit=interval, n_units=199)
# while True:
#     response = client.get_open_interest(category='linear', 
#                                 symbol=symbol, 
#                                 startTime=start,
#                                 endTime=end,
#                                 intervalTime=interval, limit=200)
    
#     latest = format_bybit_oi(response.get('result', {}).get('list',[]))
#     start = get_last_timestamp(latest)
#     end = increment_oi_timestamp(start_ts=start, unit=interval, n_units=199)
#     time.sleep(0.01)
#     all_oi = pd.concat([all_oi, latest])
#     print(f'Collecting data starting {dt.datetime.fromtimestamp(start/1000)}')
#     if len(latest) == 1: break


# all_oi.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)
# all_oi.to_csv('data/BTC_USDT_OI_15min.csv', index=False)
# all_oi['openInterest'].plot()
# plt.xlabel('Date')
# plt.ylabel('BTC Open Contracts (BTC units)')


# peiod = "30min"
# symbol = 'BTCUSDT'
# end = increment_oi_timestamp(start_ts=start, unit='30min', n_units=199)
# response =client.get_long_short_ratio(category='linear', symbol=symbol, period=interval, limit=500)


# print(response.get('result',{}))

## get all long short ratio 
def format_long_short_ratio(response: list[dict]) -> pd.DataFrame:
    if not response:
        return pd.DataFrame()
    df = pd.DataFrame(response)
    df['buyRatio'] = df.buyRatio.astype(float)
    df['sellRatio'] = df.sellRatio.astype(float)
    df['long_short_ratio'] = df.buyRatio / df.sellRatio
    df['timestamp'] = df.timestamp.astype(np.int64)
    df.index = pd.to_datetime(df.timestamp, unit='ms', utc=True)
    return df.sort_index()


# start = int(dt.datetime(2022, 1, 1, tzinfo=dt.timezone.utc).timestamp()* 1000)
# peiod = "15min"
# symbol = 'BTCUSDT'
# all_long_short = pd.DataFrame()
# end = increment_oi_timestamp(start_ts=start, unit='15min', n_units=199)

# while True:
#     response = client.get_long_short_ratio(category='linear', 
#                                  symbol=symbol, 
#                                  startTime=start,
#                                  endTime=end,
#                                  period=interval, limit=500)
    
#     latest = format_long_short_ratio(response.get('result', {}).get('list',[]))
#     print(latest)
#     start = get_last_timestamp(latest)
#     end = increment_oi_timestamp(start_ts=start, unit=interval, n_units=199)
#     time.sleep(0.01)
#     all_long_short = pd.concat([all_long_short, latest])
#     print(f'Collecting data starting {dt.datetime.fromtimestamp(start/1000)}')
#     if len(latest) == 1: break

    
# all_long_short.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)
# all_long_short.to_csv('data/BTCUSDT_long_short_15min.csv', index=False)

# orderbook = client.get_orderbook(category="linear", symbol="DOGEUSDT")
# best_ask_price = float(orderbook['result']['a'][0][0])

# response = client.place_order(
#     category='linear',
#     symbol='DOGEUSDT',
#     orderType='Limit',
#     side='Buy',
#     qty=40,
#     price=round(best_ask_price * 0.99, 5)  # buy slightly below best ask
# )
# balance = client.get_wallet_balance(accountType='UNIFIED')
# print(balance);
# positions = client.get_positions(category='linear', symbol='DOGEUSDT')
# print(positions)
# orders = client.get_wallet_balance(accountType='UNIFIED')
# print(orders)

# print(response[2][0])
# response = client.place_order(
#     category='linear',
#     symbol = 'DOGEUSDT',
#     orderType = 'Market',
#     side = 'Buy',
#     qty= 40
#     )
# print(response)
# response= client.get_account_info(category='linear',
#                                 symbol='DOGEUSDT',
#                                 openOnly=True)

# response = client.place_order(
#     category='linear',
#     symbol = 'DOGEUSDT',
#     orderType = 'Market',
#     side = 'Buy',
#     qty= 40,
#     takeProfit='0.1',
#     stopLoss = '0.05'
#     )
# print(response)


price = float(client.get_orderbook(category="linear", symbol="DOGEUSDT")['result']['a'][0][0])
# Minimum order value in USDT
min_usdt = 5

# Calculate minimum quantity needed
min_qty = min_usdt / price
min_qty = np.ceil(min_qty)

take_profit = round(price * 1.05, 5)  # 5% above
stop_loss = round(price * 0.95, 5)    # 5% below

# order = client.place_order(
#     category='linear',
#     symbol='DOGEUSDT',
#     orderType='Market',
#     side='Buy',
#     qty=min_qty,
#     takeProfit=str(take_profit),
#     stopLoss=str(stop_loss)
# )



#Get open positions
# print(client.get_positions(category='linear', symbol='DOGEUSDT'))
#print order history
# order = client.get_order_history(category='linear', symbol='DOGEUSDT')
response = client.get_orderbook(
    category="linear",
    symbol="DOGEUSDT",
    limit=50).get('result')

def format_order_book(response):
    asks = response['a']
    bids = response['b']
    return bids, asks
# bids, asks = format_order_book(response)

# for bid in bids[:10]:
#     print(f'Bid price - {bid[0]} , quantity = {bid[1]}')

#GTC order
# price = 0.07849
# min_qty = np.ceil(5/price)
# order = client.place_order(
#     category='linear',
#     symbol = 'DOGEUSDT',
#     orderType = 'Limit',
#     timeInForce='GTC',
#     side = 'Buy',
#     qty= min_qty,
#     price = price
#     )

#IOC order
# price = 0.07849
# min_qty = np.ceil(5/price)
# order2 = client.place_order(
#     category='linear',
#     symbol = 'DOGEUSDT',
#     orderType = 'Limit',
#     timeInForce='IOC',
#     side = 'Buy',
#     qty= min_qty,
#     price = price
#     )
# print(order2)

#FOK order
# price = 0.08
# min_qty = np.ceil(5/price)
# order3 = client.place_order(
#     category='linear',
#     symbol = 'DOGEUSDT',
#     orderType = 'Limit',
#     timeInForce='FOK',
#     side = 'Buy',
#     qty= min_qty,
#     price = price
#     )

# print(order3)

#PostOnly
# price = 0.08
# min_qty = np.ceil(5/price)
# order4 = client.place_order(
#     category='linear',
#     symbol = 'DOGEUSDT',
#     orderType = 'Limit',
#     timeInForce='PostOnly',
#     side = 'Buy',
#     qty= min_qty,
#     price = price
#     )
# print(order4)

price = 0.1
min_qty = np.ceil(5/price)

# buy = client.place_order(
#     category='linear',
#     symbol='DOGEUSDT',
#     orderType='Market',
#     side='Buy',
#     qty=min_qty,
#     triggerDirection=2,         # 2 = price falling
#     triggerPrice='0.1',         # Will trigger when price <= 0.1
#     timeInForce='GoodTillCancel'
# )


# trigger to sell DOGE if the price crosses above $0.35
# price = 0.35
# min_qty = np.ceil(5/price)

# sell = client.place_order(
#     category='linear',
#     symbol = 'DOGEUSDT',
#     orderType = 'Market',
#     triggerDirection = 1,
#     side= 'Sell',
#     qty= min_qty,
#     triggerPrice=price
#     )
# print(sell)

# trigger order to place a sell limit order if the price should dip below $0.05

# price = 0.05
# min_qty = np.ceil(5/price)
# order = client.place_order(
#     category='linear',
#     symbol = 'DOGEUSDT',
#     orderType = 'Limit',
#     triggerDirection = 2,
#     triggerPrice = '0.049',
#     side= 'Sell',
#     qty= min_qty,
#     price=price
#     )
# print(order)

#cancelling all orders
# client.cancel_all_orders(category='linear',
#                                 symbol='DOGEUSDT')

def parse_order_id(response):
    results = response.get('result')
    order_id = results.get('orderId')
    return order_id

price = 0.07
min_qty = np.ceil(5/price)
# order = client.place_order(
#     category='linear',
#     symbol = 'DOGEUSDT',
#     orderType = 'Limit',
#     timeInForce='GTC',
#     side = 'Buy',
#     qty= min_qty,
#     price = price
#     )

# order_id = parse_order_id(order)
oid = '30ba9601-6296-42a2-b59b-de867407dbf7'
time.sleep(20)
# try:
#     client.cancel_order(category='linear',
#                         symbol='DOGEUSDT',
#                         orderId=oid)
#     print(f'order {oid} successfully cancelled')
# except:
#     print (f"order {oid} not found")


info = client.get_instruments_info(category='linear')

symbols = info.get('result').get('list')


def get_symbol_info(symbol, symbols):
    
    info = [x for x in symbols if x['symbol'] == symbol]
    if info:
        return info[0]

    raise Exception(f'Information for symbol = {symbol} not found')
    
    


print(get_symbol_info('ETHUSDT', symbols))