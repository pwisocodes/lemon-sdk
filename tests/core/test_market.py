import pandas as pd
import pytest
from lemon.core.market import MarketData
from tests.core.conftest import account
from lemon.common.enums import INSTRUMENT_TYPE, VENUE, TIMESPAN
from datetime import datetime


@pytest.fixture
def search_instrument_result():
    return {
        "time": "2022-04-05T13:45:28.870+00:00",
        "results": [
            {
                "isin": "IE000YDZG487",
                "wkn": "A3C98L",
                "name": "HSBC NASDAQ GL SEMIC.",
                "title": "HSBC NASDAQ GL SEMIC.UC.ETF",
                "symbol": "HNSC",
                "type": "etf",
                "venues": [
                    {
                        "name": "Börse München - Gettex",
                        "title": "Gettex",
                        "mic": "XMUN",
                        "is_open": True,
                        "tradable": True,
                        "currency": "EUR"
                    }
                ]
            },
            {
                "isin": "IE00BDZVHG35",
                "wkn": "A2JDYM",
                "name": "ISIV-NASDAQ US BIOTE. EOD",
                "title": "ISHSIV-NASDAQ US BIOTECH.U.ETF",
                "symbol": "OM3E",
                "type": "etf",
                "venues": [
                    {
                        "name": "Börse München - Gettex",
                        "title": "Gettex",
                        "mic": "XMUN",
                        "is_open": True,
                        "tradable": True,
                        "currency": "EUR"
                    }
                ]
            },
            {
                "isin": "IE00BYMS5W68",
                "wkn": "A2DHWJ",
                "name": "INVESCOMI NASDAQ FINTECH",
                "title": "INVESCOMI NASDAQ FINT ETF",
                "symbol": "KFTK",
                "type": "etf",
                "venues": [
                    {
                        "name": "Börse München - Gettex",
                        "title": "Gettex",
                        "mic": "XMUN",
                        "is_open": True,
                        "tradable": True,
                        "currency": "EUR"
                    }
                ]
            },
            {
                "isin": "IE00B53SZB19",
                "wkn": "A0YEDL",
                "name": "ISHSVII-NASDAQ 100 DL ACC",
                "title": "ISHSVII-NASDAQ 100 UCITS ETF",
                "symbol": "SXRV",
                "type": "etf",
                "venues": [
                    {
                        "name": "Börse München - Gettex",
                        "title": "Gettex",
                        "mic": "XMUN",
                        "is_open": True,
                        "tradable": True,
                        "currency": "EUR"
                    }
                ]
            }
        ],
        "previous": None,
        "next": None,
        "total": 4,
        "page": 1,
        "pages": 1
    }


@pytest.fixture
def trading_venues_result():
    return {
        "time": "2022-04-05T14:17:41.445+00:00",
        "results": [
            {
                "name": "Börse München - Gettex",
                "title": "Gettex",
                "mic": "XMUN",
                "is_open": True,
                "opening_hours": {
                    "start": "08:00",
                    "end": "22:00",
                    "timezone": "Europe/Berlin"
                },
                "opening_days": [
                    "2022-04-05",
                    "2022-04-06",
                    "2022-04-07",
                    "2022-04-08",
                    "2022-04-11",
                    "2022-04-12",
                    "2022-04-13",
                    "2022-04-14",
                    "2022-04-19",
                    "2022-04-20",
                    "2022-04-21",
                    "2022-04-22",
                    "2022-04-25",
                    "2022-04-26",
                    "2022-04-27",
                    "2022-04-28",
                    "2022-04-29",
                    "2022-05-02",
                    "2022-05-03",
                    "2022-05-04",
                    "2022-05-05",
                    "2022-05-06",
                    "2022-05-09",
                    "2022-05-10",
                    "2022-05-11",
                    "2022-05-12",
                    "2022-05-13",
                    "2022-05-16",
                    "2022-05-17",
                    "2022-05-18",
                    "2022-05-19",
                    "2022-05-20",
                    "2022-05-23",
                    "2022-05-24",
                    "2022-05-25",
                    "2022-05-26",
                    "2022-05-27",
                    "2022-05-30",
                    "2022-05-31",
                    "2022-06-01",
                    "2022-06-02",
                    "2022-06-03",
                    "2022-06-06",
                    "2022-06-07",
                    "2022-06-08",
                    "2022-06-09",
                    "2022-06-10",
                    "2022-06-13",
                    "2022-06-14",
                    "2022-06-15",
                    "2022-06-16",
                    "2022-06-17",
                    "2022-06-20",
                    "2022-06-21",
                    "2022-06-22",
                    "2022-06-23",
                    "2022-06-24",
                    "2022-06-27",
                    "2022-06-28",
                    "2022-06-29",
                    "2022-06-30",
                    "2022-07-01",
                    "2022-07-04",
                    "2022-07-05",
                    "2022-07-06",
                    "2022-07-07",
                    "2022-07-08",
                    "2022-07-11",
                    "2022-07-12",
                    "2022-07-13",
                    "2022-07-14",
                    "2022-07-15",
                    "2022-07-18",
                    "2022-07-19",
                    "2022-07-20",
                    "2022-07-21",
                    "2022-07-22",
                    "2022-07-25",
                    "2022-07-26",
                    "2022-07-27",
                    "2022-07-28",
                    "2022-07-29",
                    "2022-08-01",
                    "2022-08-02",
                    "2022-08-03",
                    "2022-08-04",
                    "2022-08-05",
                    "2022-08-08",
                    "2022-08-09",
                    "2022-08-10",
                    "2022-08-11",
                    "2022-08-12",
                    "2022-08-15",
                    "2022-08-16",
                    "2022-08-17",
                    "2022-08-18",
                    "2022-08-19",
                    "2022-08-22",
                    "2022-08-23",
                    "2022-08-24",
                    "2022-08-25",
                    "2022-08-26",
                    "2022-08-29",
                    "2022-08-30",
                    "2022-08-31",
                    "2022-09-01",
                    "2022-09-02",
                    "2022-09-05",
                    "2022-09-06",
                    "2022-09-07",
                    "2022-09-08",
                    "2022-09-09",
                    "2022-09-12",
                    "2022-09-13",
                    "2022-09-14",
                    "2022-09-15",
                    "2022-09-16",
                    "2022-09-19",
                    "2022-09-20",
                    "2022-09-21",
                    "2022-09-22",
                    "2022-09-23",
                    "2022-09-26",
                    "2022-09-27",
                    "2022-09-28",
                    "2022-09-29",
                    "2022-09-30",
                    "2022-10-03",
                    "2022-10-04",
                    "2022-10-05",
                    "2022-10-06",
                    "2022-10-07",
                    "2022-10-10",
                    "2022-10-11",
                    "2022-10-12",
                    "2022-10-13",
                    "2022-10-14",
                    "2022-10-17",
                    "2022-10-18",
                    "2022-10-19",
                    "2022-10-20",
                    "2022-10-21",
                    "2022-10-24",
                    "2022-10-25",
                    "2022-10-26",
                    "2022-10-27",
                    "2022-10-28",
                    "2022-10-31",
                    "2022-11-01",
                    "2022-11-02",
                    "2022-11-03",
                    "2022-11-04",
                    "2022-11-07",
                    "2022-11-08",
                    "2022-11-09",
                    "2022-11-10",
                    "2022-11-11",
                    "2022-11-14",
                    "2022-11-15",
                    "2022-11-16",
                    "2022-11-17",
                    "2022-11-18",
                    "2022-11-21",
                    "2022-11-22",
                    "2022-11-23",
                    "2022-11-24",
                    "2022-11-25",
                    "2022-11-28",
                    "2022-11-29",
                    "2022-11-30",
                    "2022-12-01",
                    "2022-12-02",
                    "2022-12-05",
                    "2022-12-06",
                    "2022-12-07",
                    "2022-12-08",
                    "2022-12-09",
                    "2022-12-12",
                    "2022-12-13",
                    "2022-12-14",
                    "2022-12-15",
                    "2022-12-16",
                    "2022-12-19",
                    "2022-12-20",
                    "2022-12-21",
                    "2022-12-22",
                    "2022-12-23",
                    "2022-12-27",
                    "2022-12-28",
                    "2022-12-29",
                    "2022-12-30"
                ]
            },
            {
                "name": "Börse München - LM Best Performance",
                "title": "LM Best Performance",
                "mic": "LMBPX",
                "is_open": True,
                "opening_hours": {
                    "start": "08:00",
                    "end": "22:00",
                    "timezone": "Europe/Berlin"
                },
                "opening_days": [
                    "2022-04-05",
                    "2022-04-06",
                    "2022-04-07",
                    "2022-04-08",
                    "2022-04-11",
                    "2022-04-12",
                    "2022-04-13",
                    "2022-04-14",
                    "2022-04-19",
                    "2022-04-20",
                    "2022-04-21",
                    "2022-04-22",
                    "2022-04-25",
                    "2022-04-26",
                    "2022-04-27",
                    "2022-04-28",
                    "2022-04-29",
                    "2022-05-02",
                    "2022-05-03",
                    "2022-05-04",
                    "2022-05-05",
                    "2022-05-06",
                    "2022-05-09",
                    "2022-05-10",
                    "2022-05-11",
                    "2022-05-12",
                    "2022-05-13",
                    "2022-05-16",
                    "2022-05-17",
                    "2022-05-18",
                    "2022-05-19",
                    "2022-05-20",
                    "2022-05-23",
                    "2022-05-24",
                    "2022-05-25",
                    "2022-05-26",
                    "2022-05-27",
                    "2022-05-30",
                    "2022-05-31",
                    "2022-06-01",
                    "2022-06-02",
                    "2022-06-03",
                    "2022-06-06",
                    "2022-06-07",
                    "2022-06-08",
                    "2022-06-09",
                    "2022-06-10",
                    "2022-06-13",
                    "2022-06-14",
                    "2022-06-15",
                    "2022-06-16",
                    "2022-06-17",
                    "2022-06-20",
                    "2022-06-21",
                    "2022-06-22",
                    "2022-06-23",
                    "2022-06-24",
                    "2022-06-27",
                    "2022-06-28",
                    "2022-06-29",
                    "2022-06-30",
                    "2022-07-01",
                    "2022-07-04",
                    "2022-07-05",
                    "2022-07-06",
                    "2022-07-07",
                    "2022-07-08",
                    "2022-07-11",
                    "2022-07-12",
                    "2022-07-13",
                    "2022-07-14",
                    "2022-07-15",
                    "2022-07-18",
                    "2022-07-19",
                    "2022-07-20",
                    "2022-07-21",
                    "2022-07-22",
                    "2022-07-25",
                    "2022-07-26",
                    "2022-07-27",
                    "2022-07-28",
                    "2022-07-29",
                    "2022-08-01",
                    "2022-08-02",
                    "2022-08-03",
                    "2022-08-04",
                    "2022-08-05",
                    "2022-08-08",
                    "2022-08-09",
                    "2022-08-10",
                    "2022-08-11",
                    "2022-08-12",
                    "2022-08-15",
                    "2022-08-16",
                    "2022-08-17",
                    "2022-08-18",
                    "2022-08-19",
                    "2022-08-22",
                    "2022-08-23",
                    "2022-08-24",
                    "2022-08-25",
                    "2022-08-26",
                    "2022-08-29",
                    "2022-08-30",
                    "2022-08-31",
                    "2022-09-01",
                    "2022-09-02",
                    "2022-09-05",
                    "2022-09-06",
                    "2022-09-07",
                    "2022-09-08",
                    "2022-09-09",
                    "2022-09-12",
                    "2022-09-13",
                    "2022-09-14",
                    "2022-09-15",
                    "2022-09-16",
                    "2022-09-19",
                    "2022-09-20",
                    "2022-09-21",
                    "2022-09-22",
                    "2022-09-23",
                    "2022-09-26",
                    "2022-09-27",
                    "2022-09-28",
                    "2022-09-29",
                    "2022-09-30",
                    "2022-10-03",
                    "2022-10-04",
                    "2022-10-05",
                    "2022-10-06",
                    "2022-10-07",
                    "2022-10-10",
                    "2022-10-11",
                    "2022-10-12",
                    "2022-10-13",
                    "2022-10-14",
                    "2022-10-17",
                    "2022-10-18",
                    "2022-10-19",
                    "2022-10-20",
                    "2022-10-21",
                    "2022-10-24",
                    "2022-10-25",
                    "2022-10-26",
                    "2022-10-27",
                    "2022-10-28",
                    "2022-10-31",
                    "2022-11-01",
                    "2022-11-02",
                    "2022-11-03",
                    "2022-11-04",
                    "2022-11-07",
                    "2022-11-08",
                    "2022-11-09",
                    "2022-11-10",
                    "2022-11-11",
                    "2022-11-14",
                    "2022-11-15",
                    "2022-11-16",
                    "2022-11-17",
                    "2022-11-18",
                    "2022-11-21",
                    "2022-11-22",
                    "2022-11-23",
                    "2022-11-24",
                    "2022-11-25",
                    "2022-11-28",
                    "2022-11-29",
                    "2022-11-30",
                    "2022-12-01",
                    "2022-12-02",
                    "2022-12-05",
                    "2022-12-06",
                    "2022-12-07",
                    "2022-12-08",
                    "2022-12-09",
                    "2022-12-12",
                    "2022-12-13",
                    "2022-12-14",
                    "2022-12-15",
                    "2022-12-16",
                    "2022-12-19",
                    "2022-12-20",
                    "2022-12-21",
                    "2022-12-22",
                    "2022-12-23",
                    "2022-12-27",
                    "2022-12-28",
                    "2022-12-29",
                    "2022-12-30"
                ]
            }
        ],
        "previous": None,
        "next": None,
        "total": 2,
        "page": 1,
        "pages": 1
    }


@pytest.fixture
def latest_quote_result():
    return {
        "time": "2022-04-05T14:28:21.241+00:00",
        "results": [
            {
                "isin": "US30303M1027",
                "b_v": 298,
                "a_v": 298,
                "b": 2121000,
                "a": 2121500,
                "t": "2022-04-05T14:28:20.325+00:00",
                "mic": "XMUN"
            }
        ],
        "previous": None,
        "next": None,
        "total": 1,
        "page": 1,
        "pages": 1
    }


@pytest.fixture
def latest_trade_result():
    return {
        "time": "2022-04-05T14:37:36.983+00:00",
        "results": [
            {
                "isin": "DE0006231004",
                "p": 291100,
                "pbv": 3202100,
                "v": 11,
                "t": "2022-04-05T14:37:13.766+00:00",
                "mic": "XMUN"
            }
        ],
        "previous": None,
        "next": None,
        "total": 1,
        "page": 1,
        "pages": 1
    }


@pytest.fixture
def ohlc_result():
    # TODO: Shouldn't be only one entry
    return {
        "time": "2022-04-05T14:59:00.559+00:00",
        "results": [
            {
                "isin": "IE00B3RBWM25",
                "o": 1078000,
                "h": 1079000,
                "l": 1071400,
                "c": 1075400,
                "v": 3799,
                "pbv": 4089026399,
                "t": "2022-04-05T00:00:00.000+00:00",
                "mic": "XMUN"
            }
        ],
        "previous": None,
        "next": None,
        "total": 1,
        "page": 1,
        "pages": 1
    }


def test_search_instrument(account, mocker, search_instrument_result):
    def mock_perform_request(self):
        self._response = search_instrument_result
    mocker.patch(
        'lemon.core.market.ApiRequest._perform_request',
        mock_perform_request
    )
    m = MarketData()
    res = m.search_instrument(
        search="nasdaq", currency="EUR", venue=VENUE.GETTEX, tradable=True, type=INSTRUMENT_TYPE.ETF)

    assert isinstance(res, pd.DataFrame)
    assert len(res) == 4
    assert res.at[0, "isin"] == "IE000YDZG487"
    assert res.at[3, "type"] == str(INSTRUMENT_TYPE.ETF)
    assert res.at[3, "venues"][0]["mic"] == str(VENUE.GETTEX)


def test_trading_venues(account, mocker, trading_venues_result):
    def mock_perform_request(self):
        self._response = trading_venues_result
    mocker.patch(
        'lemon.core.market.ApiRequest._perform_request',
        mock_perform_request
    )

    m = MarketData()
    venues = m.trading_venues()

    assert isinstance(venues, pd.DataFrame)
    assert len(venues) == 2
    assert venues.at[0, "title"] == "Gettex"
    assert venues.at[1, "mic"] == str(VENUE.LM_BEST_PERFORMANCE)


def test_latest_quote(account, mocker, latest_quote_result):
    def mock_perform_request(self):
        self._response = latest_quote_result
    mocker.patch(
        'lemon.core.market.ApiRequest._perform_request',
        mock_perform_request
    )

    m = MarketData()
    quote = m.latest_quote(isin="US30303M1027", venue=VENUE.GETTEX)

    assert quote["isin"] == "US30303M1027"
    assert quote["b"] == 2121000
    assert quote["mic"] == str(VENUE.GETTEX)


def test_latest_trade(account, mocker, latest_trade_result):
    def mock_perform_request(self):
        self._response = latest_trade_result
    mocker.patch(
        'lemon.core.market.ApiRequest._perform_request',
        mock_perform_request
    )

    m = MarketData()
    trade = m.latest_trade(isin="DE0006231004", venue=VENUE.GETTEX)

    assert trade["isin"] == "DE0006231004"
    assert trade["mic"] == str(VENUE.GETTEX)
    assert trade["p"] == 291100
    assert trade["v"] == 11


def test_ohlc(account, mocker, ohlc_result):
    def mock_perform_request(self):
        self._response = ohlc_result
    mocker.patch(
        'lemon.core.market.ApiRequest._perform_request',
        mock_perform_request
    )
    m = MarketData()
    ohlc = m.ohlc(timespan=TIMESPAN.DAY, start=datetime.fromisoformat("2022-04-05"), end=datetime.fromisoformat("2022-04-05"),
                  isin="IE00B3RBWM25", venue=VENUE.GETTEX)

    assert isinstance(ohlc, pd.DataFrame)
    assert ohlc.at[0, "o"] == 1078000
    assert ohlc.at[0, "v"] == 3799
    assert ohlc.at[0, "mic"] == str(VENUE.GETTEX)
