import aiohttp
import asyncio
import pandas as pd
import datetime as dt
from pybit.unified_trading import HTTP
import numpy as np
from discord import SyncWebhook
import logging
import time

url = 'https://discordapp.com/api/webhooks/1401468141003083826/080LUZ5EUE5TbTeGWG15TqRYGQQm_c4WTDgDTy-Z3cJnb8Mmrig6_2xve7pSOlD7KYqE'

webhook = SyncWebhook.from_url(url)
PAIR = 'ETHUSDT'

logging.basicConfig(filename=f"{PAIR}_DCA_logs.log",
                    format='%(asctime)s %(message)s',
                    level=logging.INFO)

bb = HTTP(testnet=True)

result = bb.get_tickers(
    category="linear").get('result')['list']

tickers = [asset['symbol'] for asset in result if asset['symbol'].endswith('USDT')]

# remove stablecoin pairs
for ticker in tickers:
    if ticker[:4] in ['USDC', 'BUSD']:
        tickers.remove(ticker)

def construct_url(category, symbol, interval):
    url = f'https://api.bybit.com/v5/market/kline?category={category}&symbol={symbol}&interval={interval}'
    return url

def add_tasks(session, category, tickers, interval):
    '''

    :param session: aiohttp session for async data retrieval
    :param tickers: list of tickers generated from ticker list
    :param interval: data interval e.g. 60 == 60mins
    :return: tasks to be processed by get_data method
    '''
    tasks = []
    for ticker in tickers:
        url = construct_url(category=category, symbol=ticker, interval=interval)
        tasks.append(asyncio.create_task(session.get(url, ssl=True)))
    return tasks


async def get_data(category, tickers, interval):
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = add_tasks(session=session, category=category, tickers=tickers, interval=interval)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            results.append(await response.json())
    return results

t = time.time()
results = asyncio.run(get_data(category='linear', tickers=tickers, interval=60))
print(time.time() -t)
print(len(results))

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

    if data==None:
        pass

    data = pd.DataFrame(data,
                        columns=[
                            'timestamp',
                            'open',
                            'high',
                            'low',
                            'close',
                            'volume',
                            'turnover'
                        ],
                        )
    # print(data==None)
    f = lambda x: dt.datetime.utcfromtimestamp(np.int64(x) / 1000)
    data.index = data.timestamp.apply(f)
    return data[::-1].apply(pd.to_numeric)

def get_ma_signal_from_data(response):
    data = response.get('result')
    if data==None:
        pass
    df= format_data(data)
    # print(len(df))
    df['ma20'] = df.close.rolling(20).mean()
    df['ma200'] = df.close.rolling(200).mean()
    df['long_signal'] = np.where((df.ma20 > df.ma200) & (df.ma20.shift(1) < df.ma200.shift(1)), 1, 0)
    df['short_signal'] =np.where((df.ma20 < df.ma200) & (df.ma20.shift(1) > df.ma200.shift(1)), -1, 0)
    df['signal'] = df.long_signal + df.short_signal
    if len(df['signal']==0):
        pass
    return [df.signal[-1:].values[0] if len(df['signal'])>0 else '']

def generate_discord_message(results, tickers):

    message = """"""
    messages = []
    for sym, res in zip(tickers,results):
        signal = get_ma_signal_from_data(res)
        if len(message) > 1500:
            messages.append(message)
            message = """"""
        if signal == 0:
            logging.info(f'{sym} has no signal currently')
        elif signal == 1:
            # logging.info(f'{sym} just had a moving average crossover BUY now')
            message += f'\n{sym} just had a moving average crossover BUY now \U0001F911'
        elif signal == -1:
            # logging.info(f'{sym} just had a moving average crossover SELL now')
            message += f'\n{sym} just had a moving average crossover SELL now \U0001F911'

    messages.append(message)
    return messages




# for text in messages:
#     if text:
#         webhook.send(text)
#     else:
#         pass