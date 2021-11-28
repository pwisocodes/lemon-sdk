import logging

BASE_PAPER_TRADING_API_URL = "https://paper-trading.lemon.markets/v1"
BASE_REAL_MONEY_TRADING_API_URL = "https://trading.lemon.markets/v1"
BASE_MARKET_DATA_API_URL = "https://data.lemon.markets/v1"





logging.basicConfig(format='%(asctime)s %(levelname)s %(threadName)s: %(message)s', filename='lemon_markets.log', filemode='w',level=logging.DEBUG)