from enum import Enum

class BaseEnum(Enum):
    """Enum that allows accessing the value without .value."""

    def __str__(self):
        """Access the value with ENUM.X instead of ENUM.X.value."""
        return self.value

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        else:
            return False

class SORT(BaseEnum):
	"""Determines how the list is sorted.
	
	Values:
		ASCENDING: Ascending
		DESCENDING: Descending
	"""
	ASCENDING = "asc"
	DESCENDING = "desc"

class TRADING_TYPE(BaseEnum):
	"""Represents the types of trading
	
	Values:
		MONEY: Trade with real money
		PAPER: Trade with fake money
	
	"""
	MONEY = "money"
	PAPER = "paper"


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

class ORDERSIDE(BaseEnum):
    """Indicates wether you want to buy or sell the instrument.

	Values:
		BUY: Buy the instrument
		SELL: Sell the instrument
	"""
    BUY = "buy"
    SELL = "sell"

class ORDERTYPE(BaseEnum):
    """The type of an Order.

    Values:
        MARKET: Market Order. 
			The order is immediately executed at the next possible price. 
			Neither stop_price nor limit_price set.
		STOP: Stop Market Order. 
			Once the stop price is met, the order is converted into a market order. After that, the order is executed immediately at the next possible price.
			Only stop_price set
		LIMIT: Limit Order. 
			The order is executed at the specified price or better.
			Buy Order: limit price or lower, Sell Order: limit price or higher.
			Only limit_price set.
		STOP_LIMIT: Stop Limit Order.
			Once the stop price is met, the order is converted into a limit order. Then, the order is executed at the specified price or better
			Buy Order: limit price or lower, Sell Order: limit price or higher
			Both limit_price and stop_price set
	"""
    MARKET = "market"
    STOP = "stop_price"
    LIMIT = "limit_price"
    STOP_LIMIT = "stop_limit"

class INSTRUMENT_TYPE(BaseEnum):
    """The type of an instrument.
	
	Values:
		STOCK: Stock
		BOND: Bond
		WARRANT: Warrant
		FUND: Fund
		ETF: ETF

    """
    STOCK = "stock"
    BOND = "bond"
    WARRANT = "warrant"
    FUND = "fund"
    ETF = "etf"

class VENUE(BaseEnum):
	"""The available Venues/Stock Exchanges.
	
	Values:
		GETTEX: Börse München - Gettex
		ALLDAY: ONLY PAPER-TRADING! Offers 24/7 order execution.
		LM_BEST_PERFORMANCE: Börse München - LM Best Performance
	"""

	GETTEX = "XMUN"
	ALLDAY = "allday"
	LM_BEST_PERFORMANCE = "LMBPX"

class TIMESPAN(BaseEnum):
	"""Timespan of one OHLC Entry.
	
	Values:
		MINUTE: The data is aggregated on a per-minute basis.
		HOUR: The data is aggregated on an hourly basis.
		DAY: The data is aggregated on a daily basis.
	"""
	MINUTE = "m"
	HOUR = "h"
	DAY = "d"

class BANKSTATEMENT_TYPE(BaseEnum):
	"""Type of the Bankstatement.

	Values:
		PAY_IN: Statement related to new money entering your brokerage account
		PAPY_OUT: Statement related to a withdrawal to your reference account
		ORDER_BUY: Statement related to a buy order
		ORDER_SELL: Statement related to a sell order
		EOD_BALANCE: Your end-of-day balance
		DIVIDEND: Statement related to a paid dividend for one of your positions
	"""
	PAY_IN = "pay_in"
	PAY_OUT = "pay_out"
	ORDER_BUY = "order_buy"
	ORDER_SELL = "order_sell"
	EOD_BALANCE = "eod_balance"
	DIVIDEND = "dividend"