
import logging
import threading
from dataclasses import dataclass
from datetime import datetime
from typing import List
from urllib.parse import urlencode

from lemon.common.errors import *
from lemon.common.helpers import Singleton
from lemon.common.requests import ApiRequest

@dataclass(init=True)
class AccountState():
    _created_at: datetime
    _account_id: str
    _firstname: str
    _lastname: str
    _email: str
    _phone: str
    _address: str
    _billing_address: str
    _billing_email: str
    _billing_name: str
    _billing_vat: str
    _mode: str
    _deposit_id: str
    _client_id: str
    _account_number: str
    _iban_brokerage: str
    _iban_origin: str
    _bank_name_origin: str
    _balance: int
    _cash_to_invest: int
    _cash_to_withdraw: int
    _amount_bought_intraday: int
    _amount_sold_intraday: int
    _amount_open_orders: int
    _amount_open_withdrawals: int
    _amount_estimate_taxes: int
    _approved_at: datetime
    _trading_plan: str
    _data_plan: str
    _tax_allowance: int
    _tax_allowance_start: datetime
    _tax_allowance_end: datetime

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
            # Dynamically set Attributes
            for k,v in request.response["results"].items():
                setattr(self, f"_{k}", v)

    @property
    def created_at(self):
        return self._created_at
        
    @property
    def account_id(self):
        return self._account_id
        
    @property
    def firstname(self):
        return self._firstname
    @property
    def lastname(self):
        return self._lastname

    @property
    def email(self):
        self._email

    @property
    def phone(self):
        self._phone

    @property
    def address(self):
        self._address

    @property
    def billing_address(self):
        return self._billing_address

    @property
    def billing_email(self):
        return self._billing_email

    @property
    def billing_name(self):
        return self._billing_name

    @property
    def billing_vat(self):
        return self._billing_vat

    @property
    def mode(self):
        return self._mode

    @property
    def deposit_id(self):
        return self._deposit_id

    @property
    def client_id(self):
        return self._client_id

    @property
    def iban_brokerage(self):
        return self._iban_brokerage

    @property
    def iban_origin(self):
        return self._iban_origin

    @property
    def bank_name_origin(self):
        return self._bank_name_origin

    @property
    def balance(self):
        self.fetch_state()
        return self._balance

    @property
    def cash_to_withdraw(self):
        self.fetch_state()
        return self._cash_to_withdraw

    @property
    def amount_bought_intraday(self):
        self.fetch_state()
        return self._amount_bought_intraday

    @property
    def amount_sold_intraday(self):
        self.fetch_state()
        return self._amount_sold_intraday

    @property
    def amount_open_orders(self):
        self.fetch_state()
        return self._amount_open_orders

    @property
    def amount_open_withdrawals(self):
        self.fetch_state()
        return self._amount_open_withdrawals

    @property
    def amount_estimate_taxes(self):
        self.fetch_state()
        return self._amount_estimate_taxes

    @property
    def approved_at(self):
        return self._approved_at

    @property
    def trading_plan(self):
        self.fetch_state()
        return self._trading_plan

    @property
    def data_plan(self):
        self.fetch_state()
        return self._data_plan

    @property
    def tax_allowance(self):
        self.fetch_state()
        return self._tax_allowance

    @property
    def tax_allowance_end(self):
        self.fetch_state()
        return self._tax_allowance_end

class Account(AccountState, metaclass=Singleton):

    def __init__(self, credentials: str) -> None:
        self._token = credentials
        super().__init__()

    @property
    def token(self) -> str:
        return self._token

    def withdrawl(self, type: str, amount: int, pin: int, idempotency: str = None):
        """ Withdraw money from your bank account to your lemon.markets account e.g. amount = 1000000 means 100€ (hundreths of a cent). Take a look at: https://docs.lemon.markets/trading/overview#working-with-numbers-in-the-trading-api 

        Args:
            amount (int): amount of money that will be withdrawn, minimum is 1000000 (100 €)

        Returns:
            str: 'ok' if if request was successful
        """
        if amount > 0:

            body = {"amount": amount}
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
