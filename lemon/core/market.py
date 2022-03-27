from urllib.parse import urlencode, quote

import pandas as pd
import urllib3
from lemon.common.requests import ApiRequest
from lemon.core.account import Account


class MarketData(object):

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
            ValueError:  Keyword <keyword> is not a valid argument!
        """

        payload = {name: kwargs[name]
                   for name in kwargs if kwargs[name] is not None}

        if search != None:
            query = f"search={search}"
        else:
            query = ""

        request = ApiRequest(type="data",
                             endpoint="/instruments/?{}".format(query),
                             url_params=payload,
                             method="GET",
                             authorization_token=Account().token)
        if "results" in request.response.keys():
            if request.response['results'] != []:
                df = pd.DataFrame(request.response['results'])
                return df
            else:
                "No "
        else:
            return "No instrument found!"

    def trading_venues(self, **kwargs):
        """[summary]

        Returns:
            [type]: [description]
        """
        payload = {name: kwargs[name]
                   for name in kwargs if kwargs[name] is not None}

        if payload:
            payload = urlencode(payload, doseq=True)
        else:
            payload = ""

        request = ApiRequest(type="data",
                             endpoint="/venues/?{}".format(payload),
                             method="GET",
                             authorization_token=Account().token)

        if request.response['results'] != []:
            df = pd.DataFrame(request.response['results'])
            return df
        else:
            return "No venues found"

    def quotes(self, isin: str, mic: str = None, **kwargs):
        """[summary]

        Args:
            isin (str): [description]
            mic (str): [description]
        """
        payload = {name: kwargs[name]
                   for name in kwargs if kwargs[name] is not None}

        if payload:
            payload = urlencode(payload, doseq=True)
        else:
            payload = ""

        request = ApiRequest(type="data",
                             endpoint="/quotes/?isin={}&mic={}".format(
                                 isin, mic),
                             method="GET",
                             authorization_token=Account().token)

        if request.response['results'] != []:
            df = pd.DataFrame(request.response['results'])
            return df
        else:
            return "No quotes found!"

    def ohlc(self, isin: str, timespan: str = "d", start: str = None, end: str = None):
        """[summary]

        Args:
            isin (str): [description]
            timespan (str, optional): [description]. Either 'd' (day), 'h' (hour), 'm' (minute). Defaults to "d". 

        Raises:
            ValueError: [description]

        Returns:
            [type]: [description]
        """
        if timespan not in ["m", "h", "d"]:
            raise ValueError(f"Parameter {type} is not a valid parameter!")

        # payload = {name: kwargs[name]
        #            for name in kwargs if kwargs[name] is not None}

        # if payload:
        #     payload = "&" + urlencode(payload, doseq=True)
        # else:
        #     payload = ""

        request = ApiRequest(type="data",
                             endpoint=f"/ohlc/{timespan}1/?isin={isin}&from={start}&to={end}",
                             method="GET",
                             authorization_token=Account().token)

        if "results" in request.response:
            if request.response['results'] != []:
                df = pd.DataFrame(request.response['results'])
                return df
            else:
                return "No quotes found!"
        else:
            raise Exception(f"No data found: {request.response['error_message']}") # TODO

    def trades(self, mic: str, isin: str, **kwargs):
        """[summary]

        Args:
            mic (str): [description]
            isin (str): [description]

        Returns:
            [type]: [description]
        """
        payload = {name: kwargs[name]
                   for name in kwargs if kwargs[name] is not None}

        if payload:
            payload = "&" + urlencode(payload, doseq=True)
        else:
            payload = "&"

        request = ApiRequest(type="market",
                             endpoint="/trades/?isin={}{}/".format(
                                 isin, payload),
                             method="GET",
                             authorization_token=self._token)
        return request.response
