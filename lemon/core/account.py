
import logging
import threading
import pandas as pd
from dataclasses import dataclass
from datetime import datetime
from typing import List
from urllib.parse import urlencode
from lemon.common.enums import ORDERSIDE, ORDERSTATUS

from lemon.common.errors import *
from lemon.common.helpers import Singleton
from lemon.common.requests import ApiRequest


@dataclass(init=True)
class AccountState():
    """Represents the State/Attributes of an Account.

    Attributes:
        account_id: ID of the Acount (read-only)
        firstname: First Name of the Account Owner
        lastname: Last Name of the Account Owner
        email: Email Adress of the Account Owner
        phone: Phone Number of the Account Owner
        address: Address of the Account Owner
        billing_address: Billing Address of the Account Owner
        billing_email: Billing Email of the Account Owner
        billing_name: Billing Name of the Account Owner
        billing_vat: Value-added Tax (GER: MwSt) of the Account Owner
        mode: Environment of the account. Either 'paper' or 'money'
        deposit_id: Identification Number of your securities account
        client_id: The internal client identification number related to the account
        account_number: The account reference number
        iban_brokerage: IBAN of the brokerage account at our partner bank. This is the IBAN you can transfer money from your referrence account to
        iban_origin: IBAN of the reference account.
        bank_name_origin: Bank name of your reference account.
        balance: Your balance is the money you transferred to your account + the combined profits or losses from your orders. 1€ = 10000
        cash_to_invest: How much cash you have left to invest. Your balance minus the sum of orders that were activated but not executed, yet.
        cash_to_withdraw: How much cash you have in your account to withdraw to your reference account. Calculated through your last reported balance minus the current sum of buy orders.
        amount_bought_intraday:
        amount_sold_intraday:
        amount_open_orders:
        amount_open_withdrawals:
        amount_estimate_taxes:
        approved_at: Timestamp of live trading account approval
        trading_plan: subscription plan for trading. Either 'free', 'basic' or 'pro'
        data_plan: subscription plan for market data. Either 'free', 'basic' or 'pro'
        tax_allowance: Your tax tax allowance - between 0 and 801 €, as specified in your onboarding process
        tax_allowance_start: Relevant start date for your tax allowance (usually 01/01/ of respective year)
        tax_allowance_end: Relevant end date for your tax allowance (usually 31/12/ of respective year)

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
            for k, v in request.response["results"].items():
                setattr(self, f"_{k}", v)
        else:
            raise LemonMarketError(
                request.response['error_code'], request.response['error_message'])


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
            amount: amount of money that will be withdrawn, minimum is 1000000 (100 €)
            pin: his is the personal verification PIN you set during the onboarding. 
            idempotency: ou can set your own unique idempotency key to prevent duplicate operations. Subsequent requests with the same idempotency key will then not go through and throw an error message. This means you cannot make the same withdrawal twice.

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
                raise LemonMarketError(
                    request.response['error_code'], request.response['error_message'])

        else:
            raise ValueError(f"Can't withdraw negative amount {amount}!")

    def documents(self) -> list:
        """ Get information about all documents linked with this account 

        Returns:
            List of Documents as Dict

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
            raise LemonMarketError(
                request.response['error_code'], request.response['error_message'])

    def get_doc(self, doc_id: str) -> str:
        """ Download a specific doc by id

        Args:
            doc_id: ID of document

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
            raise LemonMarketError(
                request.response['error_code'], request.response['error_message'])

    def orders(self, isin: str = None, status: ORDERSTATUS = None, side: ORDERSIDE = None, start: str = None, end: str = None, type: str = None, key_creation_id: str = None):
        """Get a list of orders on your account.

        Args:
            isin: Filter for specific instrument
            status: Filter for status
            side: Filter for 'buy' or 'sell'
            start: Specify an ISO date string (YYYY-MM-DD) to get only orders from a specific date on.
            end: Specify an ISO date string (YYYY-MM-DD) to get only orders until a specific date.
            type: Filter for different types of orders: market, stop, limit, stop_limit
            key_creation_id: Filter for a specific API you created orders with

        Returns:
            pandas.DataFrame: Dataframe containing all orders
                created_at: This is the Timestamp for when the order was created.
                id: This is the unique Order Identification Number, which you can later use to activate your order.
                status: This is the status the Order is currently in.
                isin: This is the International Securities Identification Number of the instrument specified in that order
                expires_at: This is the Timestamp until when the order is valid
                side: 'buy' or 'sell'
                quantity: This is the amount of instruments specified in the order
                stop_price: This is the Stop price for the order. "null" if not specified.
                limit_price: This is the Limit price for the order. "null" if not specified.
                venue: This is the Market Identifier Code of the trading venue the order was placed at (default is XMUN).
                estimated_price: This is an estimation from our end for what price the order will be executed
                charge: This is the charge for the placed order

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
            raise LemonMarketError(
                request.response['error_code'], request.response['error_message'])

    def get_order(self, order_id: str):
        """ Retrieve information of a specific order.

        Args:
            order_id: ID of the order

        Returns:
            dict: order
                created_at: This is the Timestamp for when the order was created.
                id: This is the unique Order Identification Number, which you can later use to activate your order.
                status: This is the status the Order is currently in:
                    inactive: The order was placed, but has not been routed to the Stock Exchange, yet.
                    activated: The order has been routed to the Stock Exchange.
                    open: The stock exchange confirmed to have received the order (Real Money only)
                    canceling: The request to cancel the order is being routed to the stock exchange
                    canceled: The stock exchange successfully canceled the order
                    executed: The order was successfully executed at the stock exchange
                    expired: The order has expired
                isin: This is the International Securities Identification Number of the instrument specified in that order
                expires_at: This is the Timestamp until when the order is valid
                side: 'buy' or 'sell'
                quantity: This is the amount of instruments specified in the order
                stop_price: This is the Stop price for the order. "null" if not specified.
                limit_price: This is the Limit price for the order. "null" if not specified.
                venue: This is the Market Identifier Code of the trading venue the order was placed at (default is XMUN).
                estimated_price: This is an estimation from our end for what price the order will be executed
                charge: This is the charge for the placed order

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
            raise LemonMarketError(
                request.response['error_code'], request.response['error_message'])

    def cancel_order(self, order_id: str) -> str:
        """ Cancel an order that is placed/inactive or activated (but not executed by the stock exchange)

        Args:
            order_id: ID of the order

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
            raise LemonMarketError(
                request.response['error_code'], request.response['error_message'])

    def withdrawals(self):
        """ Get Withdrawals of the account.

        Returns:
            pandas.DataFrame: Withdrawals
                id: A unique Identification Number of your withdrawal
                amount: The amount that you specified for your withdrawal
                created_at: Timestamp at which you created the withdrawal
                date: Timestamp at which the withdrawal was processed by our partner bank
                idempotency: Your own unique idempotency key that you specified in your POST request to prevent duplicate withdrawals.

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
            raise LemonMarketError(
                request.response['error_code'], request.response['error_message'])

    def positions(self, isin: str = None):
        """ Get the positions of the account.

        Args:
            isin: Filter for position of a specific share

        Returns:
            pandas.DataFrame: positions
                isin: This is the International Securities Identification Number (ISIN) of the position
                isin_title: This is the Title of the instrument
                quantity: This is the number of positions you currently hold for the respective Instrument
                buy_price_avg: This is the average buy-in price of the respective position. If you buy one share for 100€ and a second one for 110€, the average buy-in price would be 105€.
                estimated_price_total: This is the current position valuation to the market trading price. So, if you own 3 shares of stock XYZ, and the current market trading price for XYZ is 100€, this attribute would return 300€
                estimated_price: This is the current market trading price for the respective position.

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
            raise LemonMarketError(
                request.response['error_code'], request.response['error_message'])
