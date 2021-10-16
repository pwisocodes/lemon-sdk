import logging

BASE_AUTH_API_URL = "https://auth.lemon.markets/oauth2/token"
BASE_PAPER_TRADING_API_URL = "https://paper-trading.lemon.markets/rest/v1"
BASE_PAPER_MARKET_DATA_API_URL = "https://paper-data.lemon.markets/v1"



logging.basicConfig(format='%(asctime)s %(levelname)s %(threadName)s: %(message)s', filename='example.log', filemode='w',level=logging.DEBUG)