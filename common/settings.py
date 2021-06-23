import logging

BASE_AUTH_API_URL = "https://auth.lemon.markets/oauth2/token"
BASE_REST_API_URL = "https://paper.lemon.markets/rest/v1"


logging.basicConfig(format='%(asctime)s %(levelname)s %(threadName)s: %(message)s', filename='example.log', filemode='w',level=logging.DEBUG)