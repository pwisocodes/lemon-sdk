import pytest
from lemon.common.errors import OrderStatusError
from lemon.core.orders import Order
from lemon.common.enums import ORDERSIDE, ORDERSTATUS, ORDERTYPE, VENUE


@pytest.fixture
def executed_order_data():
    """fixture with Data of an executed order"""
    return {
        'isin': 'US0378331005',
        'side': ORDERSIDE.BUY,
        'quantity': 5,
        'venue': VENUE.GETTEX,
        'stop_price': None,
        'limit_price': 1700000,
        'notes': 'Test Order',
        'expires_at': '2022-02-02',
        'idempotency': None,
        'status': ORDERSTATUS.EXECUTED,
        'id': 'ord_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'regulatory_information': {
            'KIID': 'text',
            'costs_exit': 20000,
            'costs_entry': 20000,
            'costs_product': 0.0,
            'costs_running': 0.0,
            'costs_exit_pct': '1.18%',
            'costs_entry_pct': '1.18%',
            'legal_disclaimer': 'text',
            'costs_product_pct': '0.00%',
            'costs_running_pct': '0.00%',
            'yield_reduction_year': 20000,
            'yield_reduction_year_pct': '1.18%',
            'yield_reduction_year_exit': 20000,
            'yield_reduction_year_exit_pct': '1.18%',
            'yield_reduction_year_following': 0,
            'estimated_yield_reduction_total': 40000,
            'estimated_holding_duration_years': '5',
            'yield_reduction_year_following_pct': '0.00%',
            'estimated_yield_reduction_total_pct': '2.35%',
        },
        'estimated_price': 1650000,
        'estimated_price_total': 8000000,
        'created_at': '2022-01-01',
        'charge': 0,
        'chargeable_at': '2022-02-02',
        'isin_title': 'APPLE INC.',
        'type': ORDERTYPE.LIMIT,
        'executed_quantity': 5,
        'executed_price': 1650000,
        'executed_price_total': 8000000,
        'activated_at': '2022-01-01',
        'executed_at': '2022-01-01',
        'rejected_at': None,
        'cancelled_at': None,
        'key_creation_id': 'apk_keykeykeykeykeykeykeykeykeykeykeyk',
        'key_activation_id': 'apk_keykeykeykeykeykeykeykeykeykeykeyk',
    }


def test_from_result(executed_order_data, account):
    result = Order.from_result(executed_order_data)

    assert isinstance(result, Order)


def test_place_order(mocker, placed_order_result, account):
    def mock_perform_request(self):
        self._response = placed_order_result

    mocker.patch('lemon.core.orders.ApiRequest._perform_request', mock_perform_request)
    order = Order('US02079K3059', '2022-04-04', ORDERSIDE.BUY, 1, VENUE.GETTEX)

    order.place()

    assert order.id is not None
    assert order.status == str(ORDERSTATUS.INACTIVE)
    assert order.isin == 'US02079K3059'
    assert order.quantity == 1


def test_activate_paper(mocker, status_ok_result, account):
    def mock_perform_request(self):
        self._response = status_ok_result

    mocker.patch('lemon.core.orders.ApiRequest._perform_request', mock_perform_request)

    order = Order('US02079K3059', '2022-04-04', ORDERSIDE.BUY, 1, VENUE.GETTEX)
    order._id = 'ord_qyGDXNNGGKzJVTMBzbHhxVfkSn3BcSjfK7'
    order._status = ORDERSTATUS.INACTIVE

    try:
        order.activate()
    except Exception as e:
        assert e


def test_activate_draft(account):
    order = Order('US02079K3059', '2022-04-04', ORDERSIDE.BUY, 1, VENUE.GETTEX)

    with pytest.raises(OrderStatusError):
        order.activate()


def test_reload(mocker, placed_order_result, account):
    order = Order('US02079K3059', '2022-04-04', ORDERSIDE.BUY, 1, VENUE.GETTEX)

    def mock_perform_request(self):
        self._response = placed_order_result

    mocker.patch('lemon.core.orders.ApiRequest._perform_request', mock_perform_request)

    order.reload()

    assert order.id == 'ord_abcdefghijklmnopqrstuvwxyz12345678'
    assert order.isin == 'US02079K3059'
    assert order.venue.upper() == VENUE.GETTEX.value


def test_to_dict(account):
    order = Order('US02079K3059', '2022-04-04', ORDERSIDE.BUY, 1, VENUE.GETTEX)

    res = order.to_dict()

    assert res['isin'] == 'US02079K3059'
    assert res['expires_at'] == '2022-04-04'
    assert res['side'] == ORDERSIDE.BUY
    assert res['quantity'] == 1
    assert res['venue'] == VENUE.GETTEX
