from enum import Enum


class BaseEnum(Enum):
    """Enum that allows accessing the value without .value."""

    def __str__(self):
        """Access the value with ENUM.X instead of ENUM.X.value."""
        return self.value


class ORDERSTATUS(BaseEnum):
    """Represents the status of an order.

	Values:
		INACTIVE: The order was placed, but has not been routed to the Stock Exchange, yet
		ACTIVATED: The order has been routed to the Stock Exchange.
		OPEN: The stock exchange confirmed to have received the order (Real Money only)
		CANCELING: The request to cancel the order is being routed to the stock exchange
		CANCELED: The stock exchange successfully canceled the order
		EXECUTED: The order was successfully executed at the stock exchange
		EXPIRED: The order has expired
		DRAFT: The order object has been created locally, but not sent to the api
    """

    INACTIVE = "inactive"
    ACTIVATED = "activated"
    OPEN = "open"
    CANCELING = "canceling"
    CANCELED = "canceled"
    EXECUTED = "executed"
    EXPIRED = "expired"
    DRAFT = "draft"

