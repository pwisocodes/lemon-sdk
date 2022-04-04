import pytest
from lemon.common.errors import OrderStatusError
from lemon.core.orders import Order
from lemon.common.enums import ORDERSIDE, ORDERSTATUS, ORDERTYPE, VENUE
from tests.core.conftest import account, status_ok_result, executed_order_result


@pytest.fixture
def placed_order_result():
    """fixture with data of an placed order
    """
    return {
        "time": "2022-04-02T18:10:54.688+00:00",
        "mode": "paper",
        "status": "ok",
        "results": {
            "created_at": "2022-04-02T18:10:54.613+00:00",
            "id": "ord_abcdefghijklmnopqrstuvwxyz12345678",
            "status": "inactive",
            "regulatory_information": {
                "costs_entry": 0,
                "costs_entry_pct": "0.00%",
                "costs_running": 0,
                "costs_running_pct": "0.00%",
                "costs_product": 0,
                "costs_product_pct": "0.00%",
                "costs_exit": 0,
                "costs_exit_pct": "0.00%",
                "yield_reduction_year": 0,
                "yield_reduction_year_pct": "0.00%",
                "yield_reduction_year_following": 0,
                "yield_reduction_year_following_pct": "0.00%",
                "yield_reduction_year_exit": 0,
                "yield_reduction_year_exit_pct": "0.00%",
                "estimated_holding_duration_years": "5",
                "estimated_yield_reduction_total": 0,
                "estimated_yield_reduction_total_pct": "0.00%",
                "KIID": "text",
                "legal_disclaimer": "text"
            },
            "isin": "US02079K3059",
            "expires_at": "2022-04-04T21:59:00.000+00:00",
            "side": "buy",
            "quantity": 1,
            "stop_price": None,
            "limit_price": None,
            "venue": "xmun",
            "estimated_price": 25395000,
            "estimated_price_total": 25395000,
            "notes": None,
            "charge": 0,
            "chargeable_at": None,
            "key_creation_id": "apk_keykeykeykeykeykeykeykeykeykeykeyk",
            "idempotency": None
        }
    }


def test_from_result(executed_order_result, account):
    result = Order.from_result(executed_order_result)

    assert isinstance(result, Order)


def test_place_order(mocker, placed_order_result, account):
    def mock_perform_request(self):
        self._response = placed_order_result
    mocker.patch(
        'lemon.core.orders.ApiRequest._perform_request',
        mock_perform_request
    )
    order = Order("US02079K3059", "2022-04-04", ORDERSIDE.BUY, 1, VENUE.GETTEX)

    order.place()

    assert order.id is not None
    assert order.status == str(ORDERSTATUS.INACTIVE)
    assert order.isin == "US02079K3059"
    assert order.quantity == 1


def test_activate_paper(mocker, status_ok_result, account):
    def mock_perform_request(self):
        self._response = status_ok_result
    mocker.patch(
        'lemon.core.orders.ApiRequest._perform_request',
        mock_perform_request
    )

    order = Order("US02079K3059", "2022-04-04", ORDERSIDE.BUY, 1, VENUE.GETTEX)
    order._id = "ord_qyGDXNNGGKzJVTMBzbHhxVfkSn3BcSjfK7"
    order._status = ORDERSTATUS.INACTIVE

    try:
        order.activate()
    except:
        assert False


def test_activate_draft(account):
    order = Order("US02079K3059", "2022-04-04", ORDERSIDE.BUY, 1, VENUE.GETTEX)

    with pytest.raises(OrderStatusError):
        order.activate()


def test_reload(mocker, placed_order_result, account):
    order = Order("US02079K3059", "2022-04-04", ORDERSIDE.BUY, 1, VENUE.GETTEX)

    def mock_perform_request(self):
        self._response = placed_order_result
    mocker.patch(
        'lemon.core.orders.ApiRequest._perform_request',
        mock_perform_request
    )

    order.reload()

    assert order.id == "ord_abcdefghijklmnopqrstuvwxyz12345678"
    assert order.isin == "US02079K3059"
    assert order.venue == VENUE.GETTEX.value


def test_to_dict(account):
    order = Order("US02079K3059", "2022-04-04", ORDERSIDE.BUY, 1, VENUE.GETTEX)

    res = order.to_dict()

    assert res["isin"] == "US02079K3059"
    assert res["expires_at"] == "2022-04-04"
    assert res["side"] == ORDERSIDE.BUY
    assert res["quantity"] == 1
    assert res["venue"] == VENUE.GETTEX
