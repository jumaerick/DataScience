from dotenv import load_dotenv
from pybit.unified_trading import HTTP
import os

# Load environment variables from .env file
load_dotenv()

# Get environment variables
key = os.getenv('ACCESS_KEY')
secret = os.getenv('SECRET_KEY')
testnet_str = os.getenv('TESTNET', 'False')  # Default to False

# Convert testnet string to boolean
testnet = testnet_str.lower() in ('true', '1', 'yes')

# Initialize Bybit session
session = HTTP(api_key=key, api_secret=secret, testnet=testnet)

# Test API connection
def testConnection():
    try:
        response = session.get_account_info()
        print("API keys are working!")
        print("Account Info:", response.get('result'))  # 'result' is the usual key
    except Exception as e:
        print("Failed to authenticate. Please check your API keys.")
        print("Error:", e)

# Run the test
testConnection()
