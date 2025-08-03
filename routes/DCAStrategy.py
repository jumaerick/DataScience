from pybit.unified_trading import HTTP
from helpers.get_bybit_http import get_client
import pandas as pd
# import pandas_ta as ta
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import json
import time
import warnings
import schedule
import logging
warnings.filterwarnings("ignore", message="pkg_resources is deprecated as an API")

"""
Dollar Cost Averaging a strategy that involves investing a fixed amount of fiat  currency into crypo at regular basis 
regardless of the current market price of the crypto.
Idea is spread your investment over a large period of time and avoid investing a larger sum at one point in time.
Effective for long-term investors.
"""

PAIR = 'BTCUSDT'
STABLE = 'USDT'

session = get_client(testnet=True)

logging.basicConfig(filename=f"{PAIR}_DCA_logs.log",
                    format='%(asctime)s %(message)s',
                    level=logging.INFO)

dca_increment = 0.002

class SpotOrderFormatter:
    
    def __init__(self, symbol, dollar_amount):
        self.symbol = symbol 
        self.info = self.get_coin_info()
        self.dollar_amount = self.get_order_qty_precision(dollar_amount)

    def get_coin_info(self):
        ticker = session.get_instruments_info(category='linear', symbol=self.symbol).get('result').get('list') 
        sym_info = [x for x in ticker if x['symbol'] == self.symbol][0]
        return sym_info 
    
    def get_order_qty_precision(self, dollar_amount):
        # print(self.info.get('lotSizeFilter')[-1])
        decimals =  len(self.info.get('lotSizeFilter').get('qtyStep').split('.')[-1])
        print(round(dollar_amount, decimals))
        return str(round(dollar_amount, decimals))
    

       
def get_available_stable_coin(stable):
    balance = session.get_wallet_balance(accountType='Unified')
    result = balance.get('result').get('list')[0].get('coin')[0]['walletBalance']
    return float(result)
    # return float(result.get('free'))


def parse_order_id(json_resp):
    result = json_resp.get('result')
    oid = result.get('orderId')
    return oid


def confirm_order_filled(oid):
    response = session.get_order_history(category='linear',
                                         orderId=oid)

    order = response.get('result').get('list')[0]
    filled_qty = order.get('cumExecQty')
    avg_price = order.get('avgPrice')
    return filled_qty, avg_price
    
# print(session.get_account_info())
