
import logging
import threading
import pandas as pd
from dataclasses import dataclass
from datetime import datetime
from typing import List
from urllib.parse import urlencode

from lemon.common.errors import *
from lemon.common.helpers import Singleton
from lemon.common.requests import ApiRequest

@dataclass(init=True)
class AccountState():
    """Represents the State/Attributes of an Account.

    Attributes:
        account_id (str): ID of the Acount (read-only)
        firstname (str): First Name of the Account Owner
        lastname (str): Last Name of the Account Owner
        email (str): Email Adress of the Account Owner
        phone (str): Phone Number of the Account Owner
        address (str): Address of the Account Owner
        billing_address (str): Billing Address of the Account Owner
        billing_email (str): Billing Email of the Account Owner
        billing_name (str): Billing Name of the Account Owner
        billing_vat (str): Value-added Tax (GER: MwSt) of the Account Owner
        mode (str): Environment of the account. Either 'paper' or 'money'
        deposit_id (str): Identification Number of your securities account
        client_id (str): The internal client identification number related to the account
        account_number (str): The account reference number
        iban_brokerage (str): IBAN of the brokerage account at our partner bank. This is the IBAN you can transfer money from your referrence account to
        iban_origin (str): IBAN of the reference account.
        bank_name_origin (str): Bank name of your reference account.
        balance (int): Your balance is the money you transferred to your account + the combined profits or losses from your orders. 1€ = 10000
        cash_to_invest (int): How much cash you have left to invest. Your balance minus the sum of orders that were activated but not executed, yet.
        cash_to_withdraw (int): How much cash you have in your account to withdraw to your reference account. Calculated through your last reported balance minus the current sum of buy orders.
        amount_bought_intraday (int):
        amount_sold_intraday (int):
        amount_open_orders (int):
        amount_open_withdrawals (int):
        amount_estimate_taxes (int):
        approved_at (datetime): Timestamp of live trading account approval
        trading_plan (str): subscription plan for trading. Either 'free', 'basic' or 'pro'
        data_plan (str): subscription plan for market data. Either 'free', 'basic' or 'pro'
        tax_allowance (int): Your tax tax allowance - between 0 and 801 €, as specified in your onboarding process
        tax_allowance_start (datetime): Relevant start date for your tax allowance (usually 01/01/ of respective year)
        tax_allowance_end (datetime): Relevant end date for your tax allowance (usually 31/12/ of respective year)

    """

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
        """ Refresh information about this Account.

        Raises:
            LemonMarketError: if lemon.markets returns an error

        """

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
            raise LemonMarketError(request.response['error_code'], request.response['error_message'])


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
            pin (int): his is the personal verification PIN you set during the onboarding. 
            idempotency (str): ou can set your own unique idempotency key to prevent duplicate operations. Subsequent requests with the same idempotency key will then not go through and throw an error message. This means you cannot make the same withdrawal twice.

        Raises:
            LemonMarketError: if lemon.markets returns an error
            ValueError: If the amount is not supported.
        """
        if amount > 0:

            body = {"amount": amount}
            request = ApiRequest(type=self.mode,
                                 endpoint="/account/withdrawals/",
                                 method="POST",
                                 body=body,
                                 authorization_token=self._token)
            
            if request.response['status'] == 'ok':
                return
            else:
                raise LemonMarketError(request.response['error_code'], request.response['error_message'])

        else:
            raise ValueError(f"Can't withdraw negative amount {amount}!")


    def documents(self) -> list:
        """ Get information about all documents linked with this account 

        Returns:
            list: arraylist of dicts

        Raises:
            LemonMarketError: if lemon.markets returns an error
        """
        request = ApiRequest(type=self.mode,
                             endpoint="/account/documents/",
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            return request.response['results']
        else:
            raise LemonMarketError(request.response['error_code'], request.response['error_message'])

    def get_doc(self, doc_id: str) -> str:
        """ Download a specific doc by id

        Args:
            doc_id (str): ID of document

        Raises:
            LemonMarketError: if lemon.markets returns an error
        """
        request = ApiRequest(type=self.mode,
                             endpoint="/account/documents/{}".format(doc_id),
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            # TODO
            return 
        else:
            raise LemonMarketError(request.response['error_code'], request.response['error_message'])


    def orders(self, isin: str = None, status:str = None, side: str = None, start: str = None, end: str = None, type: str = None, key_creation_id: str = None):
        """ Get a list of orders on your account.

        Args:
            isin (str): Filter for specific instrument
            status (str): Filter for status 'inactive', 'activated', 'open' (Real Money only), 'in_progress', 'canceling','executed', 'canceled' or 'expired'
            side (str): Filter for 'buy' or 'sell'
            start (str): Specify an ISO date string (YYYY-MM-DD) to get only orders from a specific date on.
            end (str): Specify an ISO date string (YYYY-MM-DD) to get only orders until a specific date.
            type (str): Filter for different types of orders: market, stop, limit, stop_limit
            key_creation_id (str): Filter for a specific API you created orders with

        Returns:
            pandas.DataFrame: Dataframe containing all orders
                created_at (str): This is the Timestamp for when the order was created.
                id (str): This is the unique Order Identification Number, which you can later use to activate your order.
                status (str):This is the status the Order is currently in: 'inactive', 'activated', 'open' (Real Money only), 'in_progress', 'canceling','executed', 'canceled' or 'expired'
                isin (str): This is the International Securities Identification Number of the instrument specified in that order
                expires_at (str): This is the Timestamp until when the order is valid
                side (str): 'buy' or 'sell'
                quantity (int): This is the amount of instruments specified in the order
                stop_price (int): This is the Stop price for the order. "null" if not specified.
                limit_price (int): This is the Limit price for the order. "null" if not specified.
                venue (str): This is the Market Identifier Code of the trading venue the order was placed at (default is XMUN).
                estimated_price (int): This is an estimation from our end for what price the order will be executed
                charge (int): This is the charge for the placed order
                
                see https://docs.lemon.markets/trading/orders for more

        Raises:
            LemonMarketError: if lemon.markets returns an error
        """
        request = ApiRequest(type=self.mode,
                             endpoint=f"/orders/?isin{isin}&status={status}&side={side}&from={start}&to={end}&type={type}&key_creation_id={key_creation_id}",
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            return pd.DataFrame(request.response['results'])
        else:
            raise LemonMarketError(request.response['error_code'], request.response['error_message'])

    def get_order(self, order_id: str):
        """ Retrieve information of a specific order.

        Args:
            order_id: ID of the order

        Returns:
            dict: order
                created_at (str): This is the Timestamp for when the order was created.
                id (str): This is the unique Order Identification Number, which you can later use to activate your order.
                status (str):This is the status the Order is currently in: 'inactive', 'activated', 'open' (Real Money only), 'in_progress', 'canceling','executed', 'canceled' or 'expired'
                isin (str): This is the International Securities Identification Number of the instrument specified in that order
                expires_at (str): This is the Timestamp until when the order is valid
                side (str): 'buy' or 'sell'
                quantity (int): This is the amount of instruments specified in the order
                stop_price (int): This is the Stop price for the order. "null" if not specified.
                limit_price (int): This is the Limit price for the order. "null" if not specified.
                venue (str): This is the Market Identifier Code of the trading venue the order was placed at (default is XMUN).
                estimated_price (int): This is an estimation from our end for what price the order will be executed
                charge (int): This is the charge for the placed order
                
                see https://docs.lemon.markets/trading/orders for more

        Raises:
            LemonMarketError: if lemon.markets returns an error
        """
        
        request = ApiRequest(type=self.mode,
                             endpoint="/orders/{}".format(order_id),
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            return request.response['results']
        else:
            raise LemonMarketError(request.response['error_code'], request.response['error_message'])
    
    def cancel_order(self, order_id: str) -> str:
        """ Cancel an order that is placed/inactive or activated (but not executed by the stock exchange)

        Args:
            order_id (str): ID of the order

        Raises:
            LemonMarketError: if lemon.markets returns an error
        """

        request = ApiRequest(type=self.mode,
                             endpoint="/orders/{}".format(order_id),
                             method="DELETE",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            return
        else:
            raise LemonMarketError(request.response['error_code'], request.response['error_message'])


    def withdrawals(self):
        """ Get Withdrawals of the account.

        Returns:
            pandas.DataFrame: Withdrawals
                id (str): A unique Identification Number of your withdrawal
                amount (int): The amount that you specified for your withdrawal
                created_at (str): Timestamp at which you created the withdrawal
                date (str): Timestamp at which the withdrawal was processed by our partner bank
                idempotency (str): Your own unique idempotency key that you specified in your POST request to prevent duplicate withdrawals.

        Raises:
            LemonMarketError: if lemon.markets returns an error

        """

        request = ApiRequest(type=self.mode,
                             endpoint="/account/withdrawals/",
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            return pd.DataFrame(request.response['results'])
        else:
            raise LemonMarketError(request.response['error_code'], request.response['error_message'])

    def positions(self, isin: str = None):
        """ Get the positions of the account.

        Args:
            isin (str): Filter for position of a specific share

        Returns:
            pandas.DataFrame: positions
                isin (str): This is the International Securities Identification Number (ISIN) of the position
                isin_title (str): This is the Title of the instrument
                quantity (int): This is the number of positions you currently hold for the respective Instrument
                buy_price_avg (int): This is the average buy-in price of the respective position. If you buy one share for 100€ and a second one for 110€, the average buy-in price would be 105€.
                estimated_price_total (int): This is the current position valuation to the market trading price. So, if you own 3 shares of stock XYZ, and the current market trading price for XYZ is 100€, this attribute would return 300€
                estimated_price (int): This is the current market trading price for the respective position.

        Raises:
            LemonMarketError: if lemon.markets returns an error
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
            return pd.DataFrame(request.response['results'])
        else:
            raise LemonMarketError(request.response['error_code'], request.response['error_message'])
