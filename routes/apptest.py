# from routes import bollinger
# router.testConnection()
from routes.DCAStrategy import *
PAIR = 'BTCUSDT'
STABLE = 'USDT'

def main():
    
    available = get_available_stable_coin(stable=STABLE)
    
    if dca_increment > available:
        logging.info(f'Available balance {available} is less than specified increment, no trade placed')
        return 
    
    qty = SpotOrderFormatter(PAIR, dca_increment).dollar_amount 
    print(qty)
    
    logging.info(f'Sending order for ${qty} on {PAIR}')

    response = session.place_order(
        category = 'linear',
        symbol = PAIR,
        side = 'Buy',
        orderType='Market',
        qty= qty
        )
    
    oid = parse_order_id(response) 
    
    try:
        fil_q, av_p = confirm_order_filled(oid)
        logging.info(f'Order for {fil_q} at average price of {av_p} confirmed')
    except Exception as ex:
        logging.error(f'{ex}')
    
    
   
if __name__ == '__main__':
    # schedule.every().day.at("01:28").do(main)
    schedule.every(1).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)

# client = get_client(testnet=True)
# balance = get_available_stable_coin(STABLE)
# if dca_increment < balance:
#     logging.info(f'Sending order for ${dca_increment} on {PAIR}')
# print(balance)
# print(client.get_coin_info())
# info = session.get_instruments_info(category='linear')
