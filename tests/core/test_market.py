import pandas as pd
import pytest
from lemon.core.market import MarketData
from tests.core.conftest import account
from lemon.common.enums import INSTRUMENT_TYPE, VENUE


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
    assert res.at[3, "venues"][0]["mic"].lower() == str(VENUE.GETTEX)
