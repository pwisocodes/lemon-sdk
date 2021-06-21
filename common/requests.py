
import json
from typing import Dict, Union

import requests
from common.settings import BASE_REST_API_URL, BASE_AUTH_API_URL




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


class ApiOauth2:
    url: str = BASE_AUTH_API_URL
    method: str = "POST"
    _data: dict
    _kwargs = dict
    _response = ApiResponse

    def __init__(self, credentials: dict, **kwargs ) -> None:
        self._data = credentials
        self._kwargs = kwargs
        self._auth()


    def _auth(self):
        try:
            response = requests.post(self.url, data=self._data)
            self._response = ApiResponse(content=response.content, status=response.status_code, is_success=response.ok)
        except Exception as e:
            raise e

    @property
    def response(self):
        if self._response.content:
            return json.loads(self._response.content)
        return self._response.content


class ApiRequest:
    url: str
    method: str = "GET"
    body: dict
    authorization_token: str
    _account: "Account" = None
    _kwargs: dict
    _response: ApiResponse

    def __init__(self, endpoint: str, method: str = "GET", body: dict = None,
                 authorization_token: str = None, url_params: dict = None, **kwargs):
        if authorization_token:
            # do not double check with if above as this if should override the previous one
            self.authorization_token = str(authorization_token)

        self.url_params = url_params
        self._kwargs = kwargs
        self.method = method.lower()
        self.body = body
        self._build_url(endpoint)

        self._perform_request()

    def _build_url(self, endpoint: str):
        self.url = BASE_REST_API_URL + endpoint

    def _perform_request(self):
        headers = {
            "Authorization": "Bearer {}".format(self.authorization_token)
        }
        try:
            if self.method == "post":
                response = requests.post(self.url, data=self.body, headers=headers, params=self.url_params)
            elif self.method == "delete":
                response = requests.delete(self.url, headers=headers, params=self.url_params)
            elif self.method == "patch":
                response = requests.patch(self.url, data=self.body, headers=headers, params=self.url_params)
            else:  # get
                response = requests.get(self.url, headers=headers, params=self.url_params)
                # response_org = requests.get("https://paper.lemon.markets/rest/v1/spaces/",
                #        headers=headers)
                # print(response_org.content)
                # print(response.content)
            self._response = ApiResponse(content=response.content, status=response.status_code, is_success=response.ok)
        except Exception as e:
            raise e

    @property
    def response(self):
        if self._response.content:
            return json.loads(self._response.content)
        return self._response.content
