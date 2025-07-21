from dotenv import load_dotenv
from pybit.unified_trading import HTTP
import os

# Load environment variables from .env file
load_dotenv()

# key = os.getenv('ACCESS_KEY')
# secret = os.getenv('SECRET_KEY')
testnet_str = os.getenv('TESTNET', 'False')  # Default to False
testnet = testnet_str.lower() in ('true', '1', 'yes')

# session = HTTP(api_key=key, api_secret=secret, testnet=testnet)

# Test API connection
def get_client(testnet: bool) -> HTTP:
    if testnet:
        api_key = os.getenv("ACCESS_KEY")
        api_secret = os.getenv("SECRET_KEY")
    else:
        api_key = os.getenv("BYBIT_LIVE_API_KEY")
        api_secret = os.getenv("BYBIT_LIVE_API_SECRET")

    client = HTTP(api_key=api_key, api_secret=api_secret, testnet=testnet, recv_window=10000)
    try:
        response = client.get_account_info()
        # print("✅ API keys are working!")
        # print("Account Info:", response.get("retMsg"))
        return client
    except Exception as e:
        print("❌ Failed to authenticate. Please check your API keys.")
        print("Error:", e)
        return client