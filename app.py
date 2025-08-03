# from routes import bollinger
# router.testConnection()
from routes.beta import *
# import schedule
# import logging

# url = 'https://discordapp.com/api/webhooks/1401468141003083826/080LUZ5EUE5TbTeGWG15TqRYGQQm_c4WTDgDTy-Z3cJnb8Mmrig6_2xve7pSOlD7KYqE'

# webhook = SyncWebhook.from_url(url)

# logging.basicConfig(filename=f"{PAIR}_DCA_logs.log",
#                     format='%(asctime)s %(message)s',
#                     level=logging.INFO)

# def main():
#     logging.info(f'Checking for signal...')
#     messages = generate_discord_message(results=results, tickers=tickers)
#     for text in messages:
#         if text:
#             webhook.send(text)
#         else:
#             pass

# if __name__ == '__main__':
#     # schedule.every().day.at("01:28").do(main)
#     schedule.every(10).minutes.do(main)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)