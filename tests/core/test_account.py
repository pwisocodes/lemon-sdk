import pytest
from tests.core.conftest import account, account_result, status_ok_result, placed_order_result
from lemon.core.account import Account, AccountState
from lemon.core.orders import Order
from lemon.common.enums import BANKSTATEMENT_TYPE, ORDERSIDE, ORDERTYPE, VENUE


@pytest.fixture
def withdrawals_result():
    """Sample withdrawal list
    """
    return {
        "time": "2022-04-04T08:42:27.429+00:00",
        "status": "ok",
        "mode": "paper",
        "results": [
            {
                "id": "wtd_qyFjZhh889PJsXFjgK0snMPlNwB6J6ytQa",
                "amount": 100000,
                "created_at": "2022-03-27T20:26:48.547+00:00",
                "date": None,
                "idempotency": None
            },
            {
                "id": "wtd_pyQhdXXDDHsr556LmHJcS4XPR8SDLSw9sb",
                "amount": 1000000,
                "created_at": "2021-12-26T23:18:52.708+00:00",
                "date": "2021-12-26",
                "idempotency": None
            },
            {
                "id": "wtd_pyQhdXXmm0nKfcGNm7zFtNhHdNX4ycKyxc",
                "amount": 1000000,
                "created_at": "2021-12-26T23:18:29.631+00:00",
                "date": "2021-12-26",
                "idempotency": None
            },
            {
                "id": "wtd_pyQgX77666qmmXGC95TmR9XbpbL4LYZczd",
                "amount": 1500000,
                "created_at": "2021-12-25T18:48:46.833+00:00",
                "date": "2021-12-25",
                "idempotency": None
            },
            {
                "id": "wtd_pyQgX77PPG2ZtBlZ5q3zpkLqy4FKKR6Zre",
                "amount": 1000000,
                "created_at": "2021-12-25T18:48:11.235+00:00",
                "date": "2021-12-25",
                "idempotency": None
            }
        ],
        "previous": None,
        "next": None,
        "total": 5,
        "page": 1,
        "pages": 1
    }


@pytest.fixture
def bankstatements_result():
    """Sample withdrawal list
    """
    return {
        "time": "2022-04-04T08:59:14.805+00:00",
        "status": "ok",
        "mode": "paper",
        "results": [
            {
                "id": "bst_qyFkCwwGGylytZwbkcBmWQtCH1Wqk9ZsXa",
                "account_id": "ord_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "type": "eod_balance",
                "date": "2022-03-27",
                "amount": 986000000,
                "isin": None,
                "isin_title": None,
                "created_at": "2022-03-28T01:37:04.271+00:00",
                "quantity": None
            },
            {
                "id": "bst_qyFkCwwGGNBCL1lBLnQbwVMNySmzWVZ86b",
                "account_id": "ord_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "type": "order_buy",
                "date": "2022-03-27",
                "amount": 9171000,
                "isin": "US88160R1014",
                "isin_title": "TESLA INC.",
                "created_at": "2022-03-28T01:37:04.271+00:00",
                "quantity": None
            }
        ],
        "previous": None,
        "next": None,
        "total": 2,
        "page": 1,
        "pages": 1
    }


@pytest.fixture
def apple_orders_result():
    return {
        "time": "2022-04-04T09:29:31.350+00:00",
        "status": "ok",
        "mode": "paper",
        "results": [
            {
                "id": "ord_qyFnZddddy6WQJFxTY6YLS8dJ2RfRtSBFa",
                "isin": "US0378331005",
                "isin_title": "APPLE INC.",
                "expires_at": "2022-04-01T21:59:00.000+00:00",
                "created_at": "2022-03-31T20:23:22.635+00:00",
                "side": "buy",
                "quantity": 1,
                "stop_price": None,
                "limit_price": None,
                "estimated_price": 1582400,
                "estimated_price_total": 1582400,
                "venue": "xmun",
                "status": "expired",
                "type": "market",
                "executed_quantity": 0,
                "executed_price": 0,
                "executed_price_total": 0,
                "activated_at": None,
                "executed_at": None,
                "rejected_at": None,
                "cancelled_at": None,
                "notes": "market",
                "charge": 0,
                "chargeable_at": None,
                "key_creation_id": "ord_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "key_activation_id": None,
                "regulatory_information": {
                    "KIID": "text",
                    "costs_exit": 20000,
                    "costs_entry": 20000,
                    "costs_product": 0.0,
                    "costs_running": 0.0,
                    "costs_exit_pct": "1.26%",
                    "costs_entry_pct": "1.26%",
                    "legal_disclaimer": "text",
                    "costs_product_pct": "0.00%",
                    "costs_running_pct": "0.00%",
                    "yield_reduction_year": 20000,
                    "yield_reduction_year_pct": "1.26%",
                    "yield_reduction_year_exit": 20000,
                    "yield_reduction_year_exit_pct": "1.26%",
                    "yield_reduction_year_following": 0,
                    "estimated_yield_reduction_total": 40000,
                    "estimated_holding_duration_years": "5",
                    "yield_reduction_year_following_pct": "0.00%",
                    "estimated_yield_reduction_total_pct": "2.53%"
                },
                "idempotency": None
            },
            {
                "id": "ord_qyFnZddLLpDK8YTtsN7nWx1HQyPbFqrS0b",
                "isin": "US0378331005",
                "isin_title": "APPLE INC.",
                "expires_at": "2022-04-01T21:59:00.000+00:00",
                "created_at": "2022-03-31T20:23:08.439+00:00",
                "side": "buy",
                "quantity": 1,
                "stop_price": 1500000,
                "limit_price": 1700000,
                "estimated_price": 1700000,
                "estimated_price_total": 1700000,
                "venue": "xmun",
                "status": "expired",
                "type": "stop_limit",
                "executed_quantity": 0,
                "executed_price": 0,
                "executed_price_total": 0,
                "activated_at": None,
                "executed_at": None,
                "rejected_at": None,
                "cancelled_at": None,
                "notes": "limit",
                "charge": 0,
                "chargeable_at": None,
                "key_creation_id": "ord_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "key_activation_id": None,
                "regulatory_information": {
                    "KIID": "text",
                    "costs_exit": 20000,
                    "costs_entry": 20000,
                    "costs_product": 0.0,
                    "costs_running": 0.0,
                    "costs_exit_pct": "1.18%",
                    "costs_entry_pct": "1.18%",
                    "legal_disclaimer": "text",
                    "costs_product_pct": "0.00%",
                    "costs_running_pct": "0.00%",
                    "yield_reduction_year": 20000,
                    "yield_reduction_year_pct": "1.18%",
                    "yield_reduction_year_exit": 20000,
                    "yield_reduction_year_exit_pct": "1.18%",
                    "yield_reduction_year_following": 0,
                    "estimated_yield_reduction_total": 40000,
                    "estimated_holding_duration_years": "5",
                    "yield_reduction_year_following_pct": "0.00%",
                    "estimated_yield_reduction_total_pct": "2.35%"
                },
                "idempotency": None
            }
        ],
        "previous": None,
        "next": None,
        "total": 4,
        "page": 1,
        "pages": 1
    }


@pytest.fixture
def positions_result():
    """Sample withdrawal list
    """
    return {
        "time": "2022-04-04T09:20:07.137+00:00",
        "status": "ok",
        "mode": "paper",
        "results": [
            {
                "isin": "US88160R1014",
                "isin_title": "TESLA INC.",
                "quantity": 1,
                "buy_price_avg": 9171000,
                "estimated_price_total": 9935000,
                "estimated_price": 9935000
            },
            {
                "isin": "US02079K3059",
                "isin_title": "ALPHABET INC.",
                "quantity": 1,
                "buy_price_avg": 25450000,
                "estimated_price_total": 25485000,
                "estimated_price": 25485000
            }
        ],
        "previous": None,
        "next": None,
        "total": 2,
        "page": 1,
        "pages": 1
    }


def test_withdraw(mocker, status_ok_result, account):
    def mock_perform_request(self):
        self._response = status_ok_result
    mocker.patch(
        'lemon.core.account.ApiRequest._perform_request',
        mock_perform_request
    )

    account.withdraw(100000, 1234)


def test_withdraw_negative_amount(account):

    with pytest.raises(ValueError):
        account.withdraw(-100000, 1234)


def test_withdrawals(mocker, withdrawals_result, account):
    def mock_perform_request(self):
        self._response = withdrawals_result
    mocker.patch(
        'lemon.core.account.ApiRequest._perform_request',
        mock_perform_request
    )

    withdrawals = account.withdrawals()

    assert len(withdrawals) == 5

    assert withdrawals[0]["amount"] == 100000

    assert withdrawals[1]["id"] == "wtd_pyQhdXXDDHsr556LmHJcS4XPR8SDLSw9sb"


def test_bankstatements(mocker, bankstatements_result, account):
    def mock_perform_request(self):
        self._response = bankstatements_result
    mocker.patch(
        'lemon.core.account.ApiRequest._perform_request',
        mock_perform_request
    )

    bankstatements = account.bankstatements()

    assert len(bankstatements) == 2

    assert bankstatements[0]["id"] == "bst_qyFkCwwGGylytZwbkcBmWQtCH1Wqk9ZsXa"
    assert bankstatements[1]["account_id"] == "ord_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    for bst in bankstatements:
        assert BANKSTATEMENT_TYPE.has_value(bst["type"])

    assert bankstatements[1]["isin_title"] == "TESLA INC."

# TODO: test_documents()

# TODO: test_get_doc()


def test_positions(mocker, positions_result, account):
    def mock_perform_request(self):
        self._response = positions_result
    mocker.patch(
        'lemon.core.account.ApiRequest._perform_request',
        mock_perform_request
    )

    positions = account.positions()

    assert len(positions) == 2

    assert positions.at[0, "isin"] == "US88160R1014"
    assert positions.at[0, "estimated_price"] == 9935000
    assert positions.at[1, "buy_price_avg"] == 25450000


def test_orders(mocker, apple_orders_result, account):
    def mock_perform_request(self):
        self._response = apple_orders_result
    mocker.patch(
        'lemon.core.account.ApiRequest._perform_request',
        mock_perform_request
    )

    orders = account.orders(isin="US0378331005")

    assert isinstance(orders[0], Order)

    for o in orders:
        assert o.isin == "US0378331005"

    assert orders[0].id == "ord_qyFnZddddy6WQJFxTY6YLS8dJ2RfRtSBFa"
    assert orders[0].estimated_price == 1582400


def test_get_order(mocker, placed_order_result, account):
    def mock_perform_request(self):
        self._response = placed_order_result
    mocker.patch(
        'lemon.core.account.ApiRequest._perform_request',
        mock_perform_request
    )

    order = account.get_order("ord_abcdefghijklmnopqrstuvwxyz12345678")

    assert isinstance(order, Order)
    assert order.id == "ord_abcdefghijklmnopqrstuvwxyz12345678"
    assert VENUE.has_value(order.venue)
    assert ORDERSIDE.has_value(order.side)
