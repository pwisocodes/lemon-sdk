import logging
from typing import Dict, Union

from lemon.common.settings import (BASE_MARKET_DATA_API_URL,
                                   BASE_PAPER_TRADING_API_URL,
                                   BASE_REAL_MONEY_TRADING_API_URL)

import requests


class ApiResponse:
    content: dict = None
    status: int = 0
    _is_success: bool = True

    def __init__(self, content: Union[str, dict], status: int, is_success: bool, raise_error: bool = True):
        self.content = content
        self.status = status
        self._is_success = True
        if raise_error and not is_success:
            raise Exception(content, status)

    @property
    def successful(self):
        return self._is_success

    @property
    def has_errored(self):
        return not self._is_success


class ApiRequest:
    url: str
    method: str = "GET"
    body: dict
    authorization_token: str
    _kwargs: dict
    _response: ApiResponse

    def __init__(self, type: str, endpoint: str, method: str = "GET", body: dict = None,
                 authorization_token: str = None, url_params: dict = None, **kwargs):
        if authorization_token:
            self.authorization_token = str(authorization_token)

        self.url_params = url_params
        self._kwargs = kwargs
        self.method = method.lower()
        self.body = body
        self._build_url(type.lower(), endpoint)

        self._perform_request()

    def _build_url(self, type: str, endpoint: str):
        if type == "paper":
            self.url = BASE_PAPER_TRADING_API_URL + endpoint
        elif type == "money":
            self.url = BASE_REAL_MONEY_TRADING_API_URL + endpoint
        elif type == "data":
            self.url = BASE_MARKET_DATA_API_URL + endpoint
        else:
            raise ValueError("Type is not valid!")

    def _perform_request(self):
        headers = {
            "Authorization": "Bearer {}".format(self.authorization_token)
        }
        try:
            if self.method == "post":
                response = requests.post(
                    self.url, data=self.body, headers=headers, params=self.url_params).json()
                self._response = response
            elif self.method == "put":
                response = requests.put(
                    self.url, data=self.body, headers=headers, params=self.url_params).json()
                self._response = response
            elif self.method == "delete":
                response = requests.delete(
                    self.url, headers=headers, params=self.url_params).json()
                self._response = response
            elif self.method == "patch":
                response = requests.patch(
                    self.url, data=self.body, headers=headers, params=self.url_params).json()
                self._response = response
            else:
                response = requests.get(
                    self.url, headers=headers, params=self.url_params).json()
                # Pagination
                if 'next' in response.keys():
                    if response['next'] != None:
                        # Next available
                        pagination_results = []
                        # Save 100 items from first request
                        pagination_results.append(response['results'])

                        print(f"Collecting {response['total']} results....")
                        # count = 2000 = 20 requsts a 100 (limit)
                        for offset in range(0, response['total'], 100):
                            response = requests.get(
                                url=response['next'], headers=headers, params=self.url_params).json()
                            pagination_results.append(response['results'])

                            if response['next'] == None:
                                break

                        self._response = {"results": [
                            item for sublist in pagination_results for item in sublist]}
                    else:
                        self._response = response
                else:
                    self._response = response

        except Exception as e:
            raise e

    @property
    def response(self):
        if self._response:
            return self._response
        else:
            raise Exception(f"No response available!")
