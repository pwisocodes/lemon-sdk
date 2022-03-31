from urllib.parse import urlencode, quote

import pandas as pd
import urllib3
from lemon.common.errors import LemonMarketError
from lemon.common.requests import ApiRequest
from lemon.core.account import Account


class MarketData(object):
    """Client to fetch Market Data via the lemon.markets API.
    """

    def search_instrument(self, search: str = None, isin: str = None, type: str = None, mic: str = None, currency: str = None, tradable: bool = None):
        """ Searching for instrument

        Args:
            search (str):           Use this query parameter to search for Name/Title, ISIN, WKN or symbol. You can also perform a partial search by only specifiying the first 4 symbols.
            isin (str):          Specify the ISIN you are interested in. You can also specify multiple ISINs. Maximum 10 ISINs per Request.
            type (str):             Use this query parameter to specify the type of instrument you want to filter for, e.g. "stock" or "etf"
            mic (string):           Enter a Market Identifier Code (MIC) in there. Default is XMUN.
            currency (str):      ISO currency code to see instruments traded in a specific currency
            tradeable (bool):    Filter for tradable or non-tradable Instruments with true or false

        Raises:
            LemonMarketError: if lemon.markets returns an error

        """

        request = ApiRequest(type="data",
                             endpoint=f"/instruments/?search={search}&isin={isin}&type={type}&mic={mic}&currency={currency}&tradable={tradable}",
                             method="GET",
                             authorization_token=Account().token)
        if "results" in request.response:
            return pd.DataFrame(request.response['results'])
        else:
            raise LemonMarketError(
                request.response['error_code'], request.response['error_message'])

    def trading_venues(self, mic: str = None):
        """List all available Trading Venues

        Args:
            mic (str):  Enter a Market Identifier Code (MIC) in there.

        Returns:
            DataFrame:                  DataFrame of all trading venues
                name (str):             This is the Full Name of the Trading Venue
                title (str):            This is the Short Title of the Trading Venue
                mic (str):              This is the Market Identifier Code (MIC) of the Trading Venue
                is_open (boolean):      This indicates if the Trading Venue is currently open
                opening_days (list):    list of days when Trading Venue is open


        Raises:
            LemonMarketError: if lemon.markets returns an error
        """

        request = ApiRequest(type="data",
                             endpoint=f"/venues/?mic={mic}",
                             method="GET",
                             authorization_token=Account().token)

        if "results" in request.response:
            return pd.DataFrame(request.response['results'])
        else:
            raise LemonMarketError(
                request.response['error_code'], request.response['error_message'])

    def latest_quote(self, isin: str, mic: str = None):
        """Get the latest quote of an instrument.

        Args:
            isin (str): The International Securities Identification Number of the instrument
            mic (str): Market Identifier Code of the trading venue.

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
            raise LemonMarketError(
                request.response['error_code'], request.response['error_message'])

    def ohlc(self, isin: str, start: str, end: str, timespan: str, mic: str = None, sorting=None):
        """OHLC data of a specific instrument.

        Args:
            isin (str): The International Securities Identification Number of the instrument
            start (str): ISO-Date or Epoch Timestamp.
            end (str): ISO-Date or Epoch Timestamp.
            timespan (str): Either 'd' (day), 'h' (hour), 'm' (minute).
            mic (str): Market Identifier Code of the trading venue.
            sorting (str): Sort your API response, either ascending (asc) or descending (desc)

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
                             endpoint=f"/ohlc/{timespan}1/?isin={isin}&from={start}&to={end}&mic={mic}",
                             method="GET",
                             authorization_token=Account().token)

        if "results" in request.response:
            return pd.DataFrame(request.response['results'])
        else:
            raise LemonMarketError(
                request.response['error_code'], request.response['error_message'])

    def latest_trade(self, mic: str, isin: str):
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
            raise LemonMarketError(
                request.response['error_code'], request.response['error_message'])
