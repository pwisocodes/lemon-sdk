
import logging
import threading
from dataclasses import dataclass
from datetime import datetime
from typing import List
from urllib.parse import urlencode

from lemon.common.errors import *
from lemon.common.helpers import Singleton
from lemon.common.requests import ApiRequest
from lemon.core.strategy import IStrategy

@dataclass(init=True)
class AccountState():
    account_id: str = None
    firstname: str = None
    lastname: str = None
    email: str = None
    phone: str = None
    address: str = None
    billing_email: str = None
    billing_address: str = None
    billing_name: str = None
    billing_vat: str = None
    mode: str = None
    deposit_id: str = None
    client_id: str = None
    account_number: str = None
    iban_brokerage: str = None
    iban_origin: str = None
    bank_name_origin: str = None
    balance: float = None
    cash_to_invest: float = None
    cash_to_withdraw: float = None
    trading_plan: str = None
    data_plan: str = None
    tax_allowance: float = None
    tax_allowance_start: str = None
    tax_allowance_end: str = None

    def __post_init__(self):
        try:
            self.fetch_state()
        except:
            logging.warning("Cant fetch account state")

    def fetch_state(self):
        request = ApiRequest(type="paper",
                             endpoint="/account/",
                             method="GET",
                             authorization_token=self.token
                             )

        if request.response['status'] == "ok":
            self.account_id = request.response['results']['account_id']
            self.firstname = request.response['results']['firstname']
            self.lastname = request.response['results']['lastname']
            self.email = request.response['results']['email']
            self.phone = request.response['results']['phone']
            self.address = request.response['results']['address']
            self.billing_email = request.response['results']['billing_email']
            self.billing_address = request.response['results']['billing_address']
            self.billing_name = request.response['results']['billing_name']
            self.billing_vat = request.response['results']['billing_vat']
            self.mode = request.response['results']['mode']
            self.deposit_id = request.response['results']['deposit_id']
            self.client_id = request.response['results']['client_id']
            self.account_number = request.response['results']['account_number']
            self.iban_brokerage = request.response['results']['iban_brokerage']
            self.iban_origin = request.response['results']['iban_origin']
            self.bank_name_origin = request.response['results']['bank_name_origin']
            self.balance = float(request.response['results']['balance']/10000)
            self.cash_to_invest = float(request.response['results']['cash_to_invest']/10000)
            self.cash_to_withdraw = float(request.response['results']['cash_to_withdraw']/10000)
            self.trading_plan = request.response['results']['trading_plan']
            self.data_plan = request.response['results']['data_plan']
            self.tax_allowance = float(request.response['results']['tax_allowance']/10000)
            self.tax_allowance_start = request.response['results']['tax_allowance_start']
            self.tax_allowance_end = request.response['results']['tax_allowance_end']


class Account(AccountState, metaclass=Singleton):

    def __init__(self, credentials: str) -> None:
        self._token = credentials
        super().__init__()

    @property
    def token(self) -> str:
        return self._token

    def withdrawl(self, type: str, amount: int, pin: int, idempotency: str = None):
        """ Withdraw money from your bank account to your lemon.markets account e.g. amount = 100.0 means 100€ and will be multiplyed by 10000 to get the int value the api handels. Take a look at: https://docs.lemon.markets/trading/overview#working-with-numbers-in-the-trading-api 

        Args:
            amount (float): amount of money that will be withdrawn, minimum is 100.0

        Returns:
            str: 'ok' if if request was successful
        """
        if amount > 0:
            value = amount * 10000

            body = {"amount": int(value)}
            request = ApiRequest(type="paper",
                                 endpoint="/account/withdrawals/",
                                 method="POST",
                                 body=body,
                                 authorization_token=self._token)
            if request.response['status'] == 'error':
                raise ValueError(request.response['error_message'])
        else:
            raise ValueError(f"{amount} is not a valid parameter!")

        return request.response['status']

    def documents(self) -> list:
        """ Get information about all documents linked with this account 

        Returns:
            list: arraylist of dicts
        """
        request = ApiRequest(type="paper",
                             endpoint="/account/documents/",
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            if request.response['results'] != []:
                return request.response['results']
            else:
                return "No documents found!"
        else:
            return request.response['status']

    def get_doc(self, doc_id: str) -> str:
        """ Download a specific doc by id

        Args:
            doc_id (str): ID of document

        Returns:
            str: status
        """
        request = ApiRequest(type="paper",
                             endpoint="/account/documents/{}".format(doc_id),
                             method="GET",
                             authorization_token=self._token)

        return request.response['status']

    def orders(self, type: str):
        request = ApiRequest(type=type,
                             endpoint="/orders/",
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            return request.response['results']
        return request.response['error_message']

    def delete_order(self, order_id: str, type: str) -> str:
        request = ApiRequest(type=type,
                             endpoint="/orders/{}".format(order_id),
                             method="DELETE",
                             authorization_token=self._token)

        return request.response['status']

    def order(self, order_id: str, type: str):
        request = ApiRequest(type=type,
                             endpoint="/orders/{}".format(order_id),
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            return request.response['results']
        return request.response['error_message']

    def withdrawls(self, type: str):
        request = ApiRequest(type=type,
                             endpoint="/account/withdrawals/",
                             method="GET",
                             authorization_token=self._token)
        if request.response['status'] == "ok":
            return request.response['results']
        return request.response['error_message']

    # def withdraw(self, type: str, amount:int, pin:int, idempotency:str = None):
    #     body = {"amount": amount*10000, "pin": str(pin)}
    #     request = ApiRequest(type=type,
    #                          endpoint="/account/withdrawals/",
    #                          method="POST",
    #                          body=body,
    #                          authorization_token=self._token)
    #     if request.response['status'] == "ok":
    #         return request.response['results']
    #     return request.response['error_message']

    def portfolio(self, type: str, **kwargs):
        query = {name: kwargs[name]
                 for name in kwargs if kwargs[name] is not None}
        urlencode(query)

        request = ApiRequest(type=type,
                             endpoint="/portfolio/?{}".format(query),
                             method="GET",
                             authorization_token=self._token)
        if request.response['status'] == "ok":
            return request.response['results']
        return request.response['error_message']
