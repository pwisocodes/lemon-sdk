from urllib.parse import urlencode

import pandas as pd
from lemon.common.requests import ApiRequest
from lemon.core.account import Account




class MarketData(object):

    def search_instrument(self, search: str = None, **kwargs):
        """[summary]

        Args:
            search (str): Could be a ISIN, WKN or stock name.
            kwargs** (optional): optional keyword arguments

        Keyword arguments:
            mic (string):           Enter a Market Identifier Code (MIC) in there. Default is XMUN.
            isin (string):          Specify the ISIN you are interested in. You can also specify multiple ISINs. Maximum 10 ISINs per Request.
            currency (string):      letter abbreviation, e.g. "EUR" or "USD"
            tradeable (boolean):    true or false
            limit (integer):        Needed for pagination, default is 100.
            offset (integer):        Needed for pagination, default is 0.

        Raises:
            ValueError:  Parameter {type} is not a valid parameter!
        """

        payload = {name: kwargs[name]
                   for name in kwargs if kwargs[name] is not None}

        if payload:
            payload = urlencode(payload, doseq=True)
        else:
            payload = ""

        if search != None:
            query_str = urlencode({'search': search}, doseq=True)
        else:
            query_str = ""

        request = ApiRequest(type="data",
                             endpoint="/instruments/?{}".format(
                                 query_str + payload),
                             method="GET",
                             authorization_token=Account().token)

        if request.response['results'] != []:
            df = pd.DataFrame(request.response['results'])
            return df
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

    def ohlc(self, isin: str, timespan: str = ["m", "h", "d"], start: str = None, end: str = None):
        """[summary]

        Args:
            isin (str): [description]
            timespan (str, optional): [description]. Defaults to ["m", "h", "d"].

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
                             endpoint="/ohlc/{}1/?isin={}&from={}&to={}".format(
                                 timespan, isin, start, end),
                             method="GET",
                             authorization_token=Account().token)

        if "results" in request.response.keys():
            if request.response['results'] != []:
                df = pd.DataFrame(request.response['results'])
                return df
            else:
                return "No quotes found!"
        else:
            print("No data found!")

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
