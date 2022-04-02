import lemon.core.account as acc
from lemon.common.enums import TRADING_TYPE, VENUE, ORDERSIDE, ORDERSTATUS, ORDERTYPE
from lemon.common.errors import LemonMarketError, OrderStatusError
from lemon.common.requests import ApiRequest
from datetime import datetime
import json
from typing import get_type_hints


class Order():
    """Represents an Order.

    Attributes:
        isin: Internation Security Identification Number of the instrument you wish to buy or sell
        expires_at: Order expires at the end of the specified day. Maximum expiration date is 30 days in the future.
        side: With this you can define whether you want to buy ('buy') or sell ('sell') a specific instrument
        quantity: The amount of shares you want to buy. Limited to 25,000€ estimated order price per request.
        venue: Market Identifier Code of Stock exchange you want to address. Default value is 'XMUN'.
        stop_price: Stop Market Order. Once the stop price is met, the order is converted into a market order. After that, the order is executed immediately at the next possible price. (Can be combined with limit_price)
        limit_price: Limit Order. The order is executed at the specified price or better (Buy Order: limit price or lower, Sell Order: limit price or higher). (Can be combined with stop_price)
        notes: Personal notes to the order
        idempotency: This is a unique idempotency key that prevents duplicate operations. 
            Subsequent requests with the same idempotency key will then not go through and throw an error message. This means you cannot place the same order twice.

    Attributes set by API:
        status: Status the Order is currently in ORDERSTATUS: INACTIVE, ACTIVATED, OPEN (Real Money only), IN_PROGRESS, CANCELING, EXECUTED, CANCELED or EXPIRED
        id: ID of the order
        regulatory_information: Regulatory information to the order 
            costs_entry: These are the costs for placing the Order
            costs_entry_pct: These are the costs for placing the Order as percentage value
            costs_running: These are the running costs for the order
            costs_running_pct: These are the running costs for the order as percentage value
            costs_product: These are the product costs for the order
            costs_product_pct: These are the product costs for the order as percentage value
            costs_exit: These are the exit costs for the order
            costs_exit_pct: These are the exit costs for the order as percentage value
            yield_reduction_year: This is the expected yield reduction in the first year
            yield_reduction_year_following: This is the expected yield reduction in the following year
            yield_reduction_year_exit: This is the expected yield reduction in the exit year
            kiid: This is the Key Investors Information Document, only at ETFs
            legal_disclaimer: This is a legal disclaimer for placing the Order
        estimated_price: Estimation from our end for what price the Order will be executed
        estimated_price_total: This is the Estimated Price the Order will be executed at (only for Market Orders), multiplied by the Order quantity
        created_at: The Date the Order was created at
        charge: This is the Charge for placed order
        chargeable_at: Timestamp at which the charge was generated
        isin_title: This is the Title of the instrument bought or sold with this order
        type: Type of the Order: market, stop, limit, stop_limit
        executed_quantity: This is the amount of Instruments to be bought or sold, as specified in the Order
        executed_price: This is the Price the Order was executed at
        executed_price_total: This is the Price the Order was executed at, multiplied by the Order quantity
        activated_at: The Date the Order was activated at
        executed_at: The Date the Order was executed at
        rejected_at: The Date the Order was rejected at
        cancelled_at: The Date the Order was cancelled at
        key_creation_id: This is the API Key the order was created with
        key_activation_id: This is the API Key the order was activated with. 
            When the Order was activated via mobile app, the API will return mobile here. 
            When the Order was activated via Dashboard, the API will return dashboard here

    """
    # Set by constructor / setters
    _isin: str
    _side: ORDERSIDE
    _quantity: int
    _venue: VENUE
    _stop_price: int = None
    _limit_price: int = None
    _notes: str = None
    _expires_at: datetime = None
    _idempotency: str = None

    # Returned by API
    _status: ORDERSTATUS = None
    _id: str = None
    _regulatory_information: dict = None
    _estimated_price: int = None
    _estimated_price_total: int = None
    _created_at: datetime = None
    _charge: int = None
    _chargeable_at: datetime = None
    _isin_title: str = None
    _type: ORDERTYPE = None
    _executed_quantity: int = None
    _executed_price: int = None
    _executed_price_total: int = None
    _activated_at: datetime = None
    _executed_at: datetime = None
    _rejected_at: datetime = None
    _cancelled_at: datetime = None
    _key_creation_id: str = None
    _key_activation_id: str = None

    def __init__(self, isin: str, expires_at: datetime, side: ORDERSIDE, quantity: int, venue: VENUE, trading_type: str = None, stop_price: int = None, limit_price: int = None, notes: str = None, idempotency: str = None, __status=ORDERSTATUS.DRAFT) -> None:
        self._trading_type = trading_type if trading_type is not None else acc.Account().mode
        self._isin = isin
        self._side = side
        self._quantity = quantity
        self._venue = venue
        self._stop_price = stop_price
        self._limit_price = limit_price
        self._notes = notes
        self._expires_at = expires_at
        self._idempotency = idempotency

        self._status = __status

    @staticmethod
    def from_result(res: dict) -> "Order":
        """Creates an Order Object from an API Response.

        Args:
            res: The result of the lemon.markets API, i.e. request.response['results'] of get /orders/:id/

        Returns
            Order: Order Object built from the given dict. 
        """
        order = Order(None, None, None, None, None)
        order._attr_from_response(res)
        return order

    def place(self):
        """ Place the order. It still needs to be activated to get executed.

        Raises:
            LemonMarketError: if lemon.markets returns an error

        """

        if self._status != ORDERSTATUS.DRAFT:
            # raise OrderStatusError(f"Order {self._id} is already placed")
            return

        # Remove _ from self.__dict__ to make names fit
        body = {k[1:]: v for k, v in self.__dict__.items()}

        request = ApiRequest(type=self._trading_type,
                             endpoint="/orders/",
                             method="POST",
                             body=body,
                             authorization_token=acc.Account().token
                             )

        if request.response['status'] == "ok":
            self._attr_from_response(request.response['results'])
            return
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

        if self._trading_type == TRADING_TYPE.MONEY:
            if pin is None:
                raise ValueError("Pin must be passed for real money orders.")
            else:
                type = "money"
                data = json.dumps({"pin": pin})
        elif self._trading_type == TRADING_TYPE.PAPER:
            type = "paper"

        request = ApiRequest(type=type,
                             endpoint=f"/orders/{self._id}/activate/",
                             method="POST",
                             body=data if type == TRADING_TYPE.MONEY else None,
                             authorization_token=acc.Account().token
                             )

        if request.response['status'] == "ok":
            return
        else:
            raise LemonMarketError(
                request.response['error_code'], request.response['error_message'])

    def cancel(self):
        """Cancel the Order. Available for inactive and active orders, as long as it isn't executed
        """

        if self._status in [ORDERSTATUS.INACTIVE, ORDERSTATUS.ACTIVATED, ORDERSTATUS.OPEN]:
            return acc.Account().cancel_order(self._id)
        else:
            return

    def reload(self):
        """Fetches the order again and sets the attributes to the new values."""
        res = acc.Account().get_order(self._id)
        self._attr_from_response(res.to_dict())

    def to_dict(self):
        res = {}
        for k, v in self.__dict__.items():
            # Remove _ from attribute name
            res[k[1:]] = v if not isinstance(
                v, datetime) else v.isoformat()
        return res

    def _attr_from_response(self, res: "Order"):
        """Overrides the attributes of the object based on the specified dict.

        Args:
            dict: Dict with Attributes of the Order. Attribute keys must not start with _ 
        """
        types = get_type_hints(Order)

        if all(atr in res for atr in ["isin", "expires_at", "side", "quantity", "venue"]):
            for k, v in res.items():
                if f"_{k}" in types:
                    # Parse ISO string response to datetime if attribute is annotated as datetime
                    if types[f"_{k}"] == datetime and v is not None:
                        setattr(self, f"_{k}", datetime.fromisoformat(v))
                    else:
                        setattr(self, f"_{k}", v)
        else:
            raise ValueError("Not all mandatory attrributes passed.")

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
