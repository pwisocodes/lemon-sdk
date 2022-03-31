from urllib.parse import urlencode, quote

import pandas as pd
import urllib3
from lemon.common.errors import LemonMarketError
from lemon.common.requests import ApiRequest
from lemon.core.account import Account


class MarketData(object):
    """Client to fetch Market Data via the lemon.markets API.
    """
    def search_instrument(self, search: str = None, **kwargs):
        """ Searching for instruments on Lang+Schwarz 

        Args:
            search (str): Could be a ISIN, WKN or stock name.
            kwargs** (optional): optional keyword arguments

        Keyword arguments:
            mic (string):           Enter a Market Identifier Code (MIC) in there. Default is XMUN.
            isin (string):          Specify the ISIN you are interested in. You can also specify multiple ISINs. Maximum 10 ISINs per Request.
            currency (string):      letter abbreviation, e.g. "EUR" or "USD"
            tradeable (boolean):    true or false
            type (str):             i.e. type="etf"
            limit (integer):        Needed for pagination, default is 100.
            offset (integer):       Needed for pagination, default is 0.

        Raises:
            LemonMarketError: if lemon.markets returns an error

        """

        payload = {name: kwargs[name]
                   for name in kwargs if kwargs[name] is not None}

        if search != None:
            query = f"search={search}"
        else:
            query = ""

        request = ApiRequest(type="data",
                             endpoint=f"/instruments/?{query}",
                             url_params=payload,
                             method="GET",
                             authorization_token=Account().token)
        if "results" in request.response:
            return pd.DataFrame(request.response['results'])
        else:
            raise LemonMarketError(request.response['error_code'], request.response['error_message'])

    def trading_venues(self, **kwargs):
        """List all available Trading Venues

        Returns:
            list: Trading Venue Object

        Raises:
            LemonMarketError: if lemon.markets returns an error
        """
        payload = {name: kwargs[name]
                   for name in kwargs if kwargs[name] is not None}

        if payload:
            payload = urlencode(payload, doseq=True)
        else:
            payload = ""

        request = ApiRequest(type="data",
                             endpoint=f"/venues/?{payload}",
                             method="GET",
                             authorization_token=Account().token)

        if "results" in request.response:
            return pd.DataFrame(request.response['results'])
        else:
            raise LemonMarketError(request.response['error_code'], request.response['error_message'])

    def quotes(self, isin: str, mic: str = None):
        """Get the latest quote of an instrument.

        Args:
            isin (str): [description]
            mic (str): [description]

        Returns:
            dict: The latest Quote 
                isin: ISIN
                t: timestamp
                mic: Market Identifier Code
                b: bid-price
                a: ask-price
                b_v: bid volume
                a_v: ask_volume
        
        Raises:
            LemonMarketError: if lemon.markets returns an error
                
        """
        request = ApiRequest(type="data",
                             endpoint=f"/quotes/latest?decimals=false&isin={isin}&mic={mic}",
                             method="GET",
                             authorization_token=Account().token)
        if "results" in request.response:
            return request.response['results']
        else:
            raise LemonMarketError(request.response['error_code'], request.response['error_message'])

    def ohlc(self, isin: str, timespan: str = "d", start: str = None, end: str = None):
        """OHLC data of a specific instrument.

        Args:
            isin (str): The International Securities Identification Number of the instrument
            timespan (str, optional): Either 'd' (day), 'h' (hour), 'm' (minute). Defaults to "d". 
            start (str): ISO-Date or Epoch Timestamp.
            end (str): ISO-Date or Epoch Timestamp.

        Raises:
            ValueError: Invalid Parameter specified
            LemonMarketError: if lemon.markets returns an error

        Returns:
            pandas.DataFrame: Dataframe containing OHLC-Data.
                isin: The International Securities Identification Number of the instrument
                o: Open Price in specific time period
                h: Highest Price in specific time period
                l: Lowest Price in specific time period
                c: Close Price in specific time period
                v: Aggegrated volume (Number of trades) of instrument in specific time period
                pbv: Price by Volume (Sum of (quantity * last price)) of instrument in specific time period
                t: Timestamp of time period the OHLC data is based on
                mic: Market Identifier Code of Trading Venue the OHLC data occured at

        """
        if timespan not in ["m", "h", "d"]:
            raise ValueError(f"Parameter {type} is not a valid parameter!")

        request = ApiRequest(type="data",
                             endpoint=f"/ohlc/{timespan}1/?isin={isin}&from={start}&to={end}",
                             method="GET",
                             authorization_token=Account().token)

        if "results" in request.response:
            return pd.DataFrame(request.response['results'])
        else:
            raise LemonMarketError(request.response['error_code'], request.response['error_message'])

    def trades(self, mic: str, isin: str):
        """Latest trade of a specific instrument

        Args:
            mic (str): Market Identifier Code of the trading venue.
            isin (str): The International Securities Identification Number of the instrument

        Returns:
            dict: Information about the trade.
                isin: The International Securities Identification Number of the instrument
                p: Price the trade happened at
                v: Volume for trade (quantity)
                t: Timestamp of time period the trade occured at
                mic: Market Identifier Code of Trading Venue the trade occured at

        """
        if payload:
            payload = "&" + urlencode(payload, doseq=True)
        else:
            payload = "&"

        request = ApiRequest(type="market",
                             endpoint=f"/trades/latest?decimals=false&isin={isin}&mic={mic}/",
                             method="GET",
                             authorization_token=self._token)
        if "results" in request.response:
            return request.response['results']
        else:
            raise LemonMarketError(request.response['error_code'], request.response['error_message'])
