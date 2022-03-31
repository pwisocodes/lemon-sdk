import datetime
import json
from multiprocessing.sharedctypes import Value
from lemon.common.enums import VENUE
from lemon.common.requests import ApiRequest
from lemon.core.account import *


class Order():
    """Represents an Order.

    Attributes:
        isin: Internation Security Identification Number of the instrument you wish to buy or sell
        expires_at: ISO String date (YYYY-MM-DD). Order expires at the end of the specified day. Maximum expiration date is 30 days in the future.
        side: With this you can define whether you want to buy ('buy') or sell ('sell') a specific instrument
        quantity: The amount of shares you want to buy. Limited to 25,000€ estimated order price per request.
        venue: Market Identifier Code of Stock exchange you want to address. Default value is 'XMUN'.
        stop_price: Stop Market Order. Once the stop price is met, the order is converted into a market order. After that, the order is executed immediately at the next possible price. (Can be combined with limit_price)
        limit_price: Limit Order. The order is executed at the specified price or better (Buy Order: limit price or lower, Sell Order: limit price or higher). (Can be combined with stop_price)
        notes: Personal notes to the order
        status: Status the Order is currently in ORDERSTATUS: INACTIVE, ACTIVATED, OPEN (Real Money only), IN_PROGRESS, CANCELING, EXECUTED, CANCELED or EXPIRED
        id: ID of the order
        regulatory_information: Regulatory information to the order 
        estimated_price: Estimation from our end for what price the Order will be executed

    """

    _isin: str
    _side: ORDERSIDE
    _quantity: int
    _venue: VENUE
    _stop_price: int = None
    _limit_price: int = None
    _notes: str = None
    _expires_at: datetime = None

    _status: ORDERSTATUS = None
    _id: str = None
    _regulatory_information: dict = None
    _estimated_price: int = None

    def __init__(self, isin: str, expires_at, side: ORDERSIDE, quantity: int, venue: VENUE, trading_type: str, stop_price: int = None, limit_price: int = None, notes: str = None, __status="draft") -> None:
        self._trading_type = trading_type
        self._isin = isin
        self._side = side
        self._quantity = quantity
        self._venue = venue
        self._stop_price = stop_price
        self._limit_price = limit_price
        self._notes = notes
        self._expires_at = expires_at

        self._status = __status

    def place(self):
        """ Place the order. It still needs to be activated to get executed.

        Raises:
            LemonMarketError: if lemon.markets returns an error

        Returns:
            str: OrderID 
        """

        if self._status != ORDERSTATUS.INACTIVE:
            # raise OrderStatusError(f"Order {self._id} is already placed")
            return

        # Remove _ from self.__dict__ to make names fit
        body = {k[1:]: v for k, v in self.__dict__.items()}

        request = ApiRequest(type=self._trading_type,
                             endpoint="/orders/",
                             method="POST",
                             body=body,
                             authorization_token=Account().token
                             )

        if request.response['status'] == "ok":

            self._status = request.response['results']['status']
            # Should be "inactive" now
            self._id = request.response['results']['id']
            self._regulatory_information = request.response['results']['regulatory_information']
            self._estimated_price = request.response['results']['estimated_price']

            return self._id
        else:
            raise LemonMarketError(
                request.response['error_code'], request.response['error_message'])

    def activate(self, pin: str = None) -> str:
        """ Activate the Order. After you activated the order, it is routed to the trading venue.

        Arguments:
            pin: PIN to activate a real-money order. Mandatory for real-money trading.

        Raises:
            ValueError: if PIN is missing for real money orders
            OrderStatusError: if called on a order that is not yet activated
            LemonMarketError: if lemon.markets returns an error

        """

        if self._status == ORDERSTATUS.DRAFT:
            raise OrderStatusError("Order must first be placed")

        if self._trading_type == "money":
            raise ValueError("Pin must be passed for real money orders.")

        if self._trading_type == "paper":
            type = "paper"
        else:
            type = "money"
            data = json.dumps({"pin": pin})

        request = ApiRequest(type=type,
                             endpoint=f"/orders/{self._id}/activate/",
                             method="POST",
                             body=data if type == "money" else None,
                             authorization_token=Account().token
                             )

        if request.response['status'] == "ok":
            return
        else:
            raise LemonMarketError(
                request.response['error_code'], request.response['error_message'])

    def cancel(self) -> str:
        """Cancel the Order. Available for inactive and active orders, as long as it isn't executed
        """

        if self._status != ORDERSTATUS.DRAFT:
            return Account().cancel_order(self._id)
        else:
            # Do nothing as it's just a local object
            return

    @property
    def isin(self):
        return self._isin

    @isin.setter
    def isin(self, value):
        if self.status != ORDERSTATUS.DRAFT:
            raise OrderStatusError(
                "Can't modify attributes after Order is placed")
        else:
            self._isin = value

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, value):
        if self.status != ORDERSTATUS.DRAFT:
            raise OrderStatusError(
                "Can't modify attributes after Order is placed")
        else:
            self._side = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if self.status != ORDERSTATUS.DRAFT:
            raise OrderStatusError(
                "Can't modify attributes after Order is placed")
        else:
            self._quantity = value

    @property
    def venue(self):
        return self._venue

    @venue.setter
    def venue(self, value):
        if self.status != ORDERSTATUS.DRAFT:
            raise OrderStatusError(
                "Can't modify attributes after Order is placed")
        else:
            self._venue = value

    @property
    def stop_price(self):
        return self._stop_price

    @stop_price.setter
    def stop_price(self, value):
        if self.status != ORDERSTATUS.DRAFT:
            raise OrderStatusError(
                "Can't modify attributes after Order is placed")
        else:
            self._stop_price = value

    @property
    def limit_price(self):
        return self._limit_price

    @limit_price.setter
    def limit_price(self, value):
        if self.status != ORDERSTATUS.DRAFT:
            raise OrderStatusError(
                "Can't modify attributes after Order is placed")
        else:
            self._limit_price = value

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, value):
        if self.status != ORDERSTATUS.DRAFT:
            raise OrderStatusError(
                "Can't modify attributes after Order is placed")
        else:
            self._notes = value

    @property
    def expires_at(self):
        return self._expires_at

    @expires_at.setter
    def expires_at(self, value):
        if self.status != ORDERSTATUS.DRAFT:
            raise OrderStatusError(
                "Can't modify attributes after Order is placed")
        else:
            self._expires_at = value

    # Available after placed

    @property
    def id(self):
        if self.status != ORDERSTATUS.DRAFT:
            return self._id
        else:
            raise AttributeError("Not available until placed")

    @property
    def status(self):
        return self._status

    @property
    def regulatory_information(self):
        if self.status != ORDERSTATUS.DRAFT:
            return self._regulatory_information
        else:
            raise AttributeError("Not available until placed")

    @property
    def estimated_price(self):
        if self.status != ORDERSTATUS.DRAFT:
            return self._estimated_price
        else:
            raise AttributeError("Not available until placed")
