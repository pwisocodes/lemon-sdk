from lemon.common.enums import INSTRUMENT_TYPE, SORT, VENUE
from lemon.core.market import MarketData
from datetime import datetime

class Instrument:
	"""Represents an Trading instrument.

	Attributes:
		isin: This is the International Securities Identification Number (ISIN) of the instrument
		wkn: This is the German Securities Identification Number of instrument
		name: This is the Instrument name
		title: This is the Instrument Title
		symbol: This is the Symbol of the instrument at the trading venue
		type: This tells you about the type of instrument, e.g. "stock" or "etf"
		venues: Information on which venues the instrument is available
	"""

	_isin: str
	_wkn: str
	_name: str
	_title: str
	_symbol: str
	_type: INSTRUMENT_TYPE
	_venues: dict

	@property
	def isin(self) -> str:
		return self._isin

	@property
	def wkn(self) -> str:
		return self._wkn

	@property
	def name(self) -> str:
		return self._name

	@property
	def title(self) -> str:
		return self._title

	@property
	def symbol(self) -> str:
		return self._symbol

	@property
	def type(self) -> INSTRUMENT_TYPE:
		return self._type

	@property
	def venues(self) -> dict:
		return self._venues

	def __init__(
		self,
		isin: str,
		wkn: str,
		name: str,
		title: str,
		symbol: str,
		type: INSTRUMENT_TYPE,
		venues: dict,
	):
		self._isin = isin
		self._wkn = (wkn,)
		self._name = (name,)
		self._title = (title,)
		self._symbol = (symbol,)
		self._type = type
		self._venues = venues

	def latest_quote(self, venue: VENUE = VENUE.GETTEX):
		"""Returns the latest quote of the instrument

		Args:
			venue: Market Identifier Code of the trading venue.

		Returns:
			dict: The latest Quote
				isin: ISIN
				t: timestamp
				mic: Market Identifier Code
				b: bid-price
				a: ask-price
				b_v: bid volume
				a_v: ask_volume
		"""
		m = MarketData()
		return m.latest_quote(isin=self.isin, venue=venue)

	def latest_trade(self, venue: VENUE = VENUE.GETTEX):
		"""Latest trade of the instrument at the specified venue

		Args:
			venue:  Enter a venue or a Market Identifier Code (MIC) in there.
			
		Returns:
			dict: Information about the trade.
				isin: The International Securities Identification Number of the instrument
				p: Price the trade happened at
				v: Volume for trade (quantity)
				t: Timestamp of time period the trade occured at
				mic: Market Identifier Code of Trading Venue the trade occured at
		"""
		m = MarketData()
		return m.latest_quote(isin=self.isin, venue=venue)

	def ohlc(self, start: datetime, end: datetime, venue: VENUE = VENUE.GETTEX, sorting: SORT = None):
		"""OHLC data of the instrument.

        Args:
            start: Specify an ISO date string (YYYY-MM-DD) to get data from a specific date on.
            end: Specify an ISO date string (YYYY-MM-DD) to get only data until a specific date.
            timespan: Timespan of one OHLC Entry.
            venue:  Enter a venue or a Market Identifier Code (MIC) in there.
            sorting: Sort your API response, either ascending (asc) or descending (desc)

        Raises:
            ValueError: Invalid Parameter specified
            LemonMarketError: if lemon.markets returns an error

        Returns:
            pandas.DataFrame: Dataframe containing OHLC-Data.
                isin: The International Securities Identification Number of the instrument
                o: Open Price in specific time period
                h: Highest Price in specific time period
                l: Lowest Price in specific time period
                c: Close Price in specific time period
                v: Aggegrated volume (Number of trades) of instrument in specific time period
                pbv: Price by Volume (Sum of (quantity * last price)) of instrument in specific time period
                t: Timestamp of time period the OHLC data is based on
                mic: Market Identifier Code of Trading Venue the OHLC data occured at

        """
		m = MarketData()
		return m.latest_quote(isin=self.isin, start=start, end=end, venue=venue, sorting=sorting)

	def to_dict(self):
		res = {}
		for k, v in self.__dict__.items():
			# Remove _ from attribute name
			res[k[1:]] = v
		return res
