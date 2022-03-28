
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

    _account_id: str = None
    _firstname: str = None
    _lastname: str = None
    _email: str = None
    _phone: str = None
    _address: str = None
    _billing_address: str = None
    _billing_email: str = None
    _billing_name: str = None
    _billing_vat: str = None
    _mode: str = None
    _deposit_id: str = None
    _client_id: str = None
    _account_number: str = None
    _iban_brokerage: str = None
    _iban_origin: str = None
    _bank_name_origin: str = None
    _balance: int = None
    _cash_to_invest: int = None
    _cash_to_withdraw: int = None
    _amount_bought_intraday: int = None
    _amount_sold_intraday: int = None
    _amount_open_orders: int = None
    _amount_open_withdrawals: int = None
    _amount_estimate_taxes: int = None
    _approved_at: datetime = None
    _trading_plan: str = None
    _data_plan: str = None
    _tax_allowance: int = None
    _tax_allowance_start: datetime = None
    _tax_allowance_end: datetime = None

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

    @property
    def mode(self):
        return self._mode
    
    @mode.setter
    def mode(self, value):
        self._mode = value

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
        else:
            raise Exception(f"Couldn't fetch Account Data: {request.response['error_message']}")


class Account(AccountState, metaclass=Singleton):

    def __init__(self, credentials: str) -> None:
        self._token = credentials
        super().__init__()

    @property
    def token(self) -> str:
        return self._token

    def withdraw(self, amount: int, pin: int, idempotency: str = None):
        """ Withdraw money from your bank account to your lemon.markets account e.g. amount = 1000000 means 100€ (hundreths of a cent). Take a look at: https://docs.lemon.markets/trading/overview#working-with-numbers-in-the-trading-api 

        Args:
            amount (int): amount of money that will be withdrawn, minimum is 1000000 (100 €)

        Returns:
            str: 'ok' if if request was successful
        """
        if amount > 0:

            body = {"amount": amount}
            request = ApiRequest(type=self.mode,
                                 endpoint="/account/withdrawals/",
                                 method="POST",
                                 body=body,
                                 authorization_token=self._token)
            if request.response['status'] == 'error':
                raise ValueError(request.response['error_message'])
            else:
                return request.response['status']
        else:
            raise ValueError(f"Amount if {amount} is not a valid!")


    def documents(self) -> list:
        """ Get information about all documents linked with this account 

        Returns:
            list: arraylist of dicts
        """
        request = ApiRequest(type=self.mode,
                             endpoint="/account/documents/",
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            if request.response['results'] != []:
                return request.response['results']
            else:
                return None
        else:
            raise Exception(f"{request.response['error_code']}: {request.response['error_message']}") # TODO

    def get_doc(self, doc_id: str) -> str:
        """ Download a specific doc by id

        Args:
            doc_id (str): ID of document

        Returns:
            str: status
        """
        request = ApiRequest(type=self.mode,
                             endpoint="/account/documents/{}".format(doc_id),
                             method="GET",
                             authorization_token=self._token)

        return request.response['status']

    def orders(self, isin: str = None, expires_at: str = None, side: str = None, quantity: str = None, venue: str = None):
        """ Get a list of orders on your account.

        Args:
            isin (str): Filter for ISIN
            expires_at (str): Filter for Orders that expire at this date
            side (str): 'buy' or 'sell'
            quantity (int): amount of shares
            venue (str): MIC of Trading Venue

        Returns:
            list: orders
        """
        request = ApiRequest(type=self.mode,
                             endpoint="/orders/",
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            if request.response['results'] != []:
                return request.response['results']
            else:
                return None
        else:
            raise Exception(f"{request.response['error_code']}: {request.response['error_message']}") # TODO

    def get_order(self, order_id: str):
        """ Retrieve information of a specific order.

        Args:
            order_id: ID of the order

        Returns:
            dict: order
        
        """
        
        request = ApiRequest(type=self.mode,
                             endpoint="/orders/{}".format(order_id),
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            # TODO create Order object?
            return request.response['results']
        else:
            raise Exception(f"{request.response['error_code']}: {request.response['error_message']}") # TODO
    
    def cancel_order(self, order_id: str) -> str:
        """ Cancel an order that is placed/inactive or activated (but not executed by the stock exchange)

        Args:
            order_id (str): ID of the order

        Returns:
            str: status
        """

        request = ApiRequest(type=self.mode,
                             endpoint="/orders/{}".format(order_id),
                             method="DELETE",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            return request.response['status']
        else:
            raise Exception(f"{request.response['error_code']}: {request.response['error_message']}") # TODO


    def withdrawals(self):
        """ Get Withdrawals of the account.
        """

        request = ApiRequest(type=self.mode,
                             endpoint="/account/withdrawals/",
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            if request.response['results'] != []:
                return request.response['results']
            else:
                return None
        else:
            raise Exception(f"{request.response['error_code']}: {request.response['error_message']}") # TODO

    def positions(self, isin: str = None):
        """ Get the positions of the account.

        Args:
            isin (str): Filter for position of a specific share

        Returns:
            list: positions
            
        
        """
        if isin is not None:
            query = f"isin={isin}"
        else:
            query = ""

        request = ApiRequest(type=self.mode,
                             endpoint=f"/positions/?{query}",
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            if request.response['results'] != []:
                return request.response['results']
            else:
                return None
        else:
            raise Exception(f"{request.response['error_code']}: {request.response['error_message']}") # TODO