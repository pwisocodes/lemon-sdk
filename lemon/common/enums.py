from enum import Enum


class BaseEnum(Enum):
    """Enum that allows accessing the value without .value and supports Documentation."""

    def __new__(cls, value, doc=None):
        """Support accessing the documentation by .__doc__"""

        self = object.__new__(cls)
        self._value_ = value
        if doc is not None:
            self.__doc__ = doc
        return self

    def __str__(self):
        """Access the value with ENUM.X instead of ENUM.X.value."""
        return self.value


class ORDERSTATUS(BaseEnum):
    """Represents the status of an order.
    """
    INACTIVE = "inactive", "The order was placed, but has not been routed to the Stock Exchange, yet."
    ACTIVATED = "activated", "The order has been routed to the Stock Exchange."
    OPEN = "open", "The stock exchange confirmed to have received the order (Real Money only)"
    CANCELING = "canceling", "The request to cancel the order is being routed to the stock exchange"
    CANCELED = "canceled", "The stock exchange successfully canceled the order"
    EXECUTED = "executed", "The order was successfully executed at the stock exchange"
    EXPIRED = "expired", "The order has expired"
    DRAFT = "draft", "The order object has been created locally, but not sent to the api."
