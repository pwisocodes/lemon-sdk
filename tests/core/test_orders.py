import pytest

import lemon.core.orders
import lemon.core.account

from lemon.common.enums import ORDERSIDE, ORDERSTATUS, ORDERTYPE, VENUE


@pytest.fixture
def executed_order_data():
    """fixture with Data of an executed order
    """
    return {
        "_isin": "US0378331005",
        "_side": ORDERSIDE.BUY,
        "_quantity": 5,
        "_venue":  VENUE.GETTEX,
        "_stop_price": None,
        "_limit_price": 1700000,
        "_notes": "Test Order",
        "_expires_at": "2.02.2222",
        "_idempotency": None,
        "_status": ORDERSTATUS.EXECUTED,
        "_id": "ord_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "_regulatory_information": {
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
        "_estimated_price": 1650000,
        "_estimated_price_total": 8000000,
        "_created_at": "1.01.2222",
        "_charge": 0,
        "_chargeable_at": "2.02.2222",
        "_isin_title": "APPLE INC.",
        "_type": ORDERTYPE.LIMIT,
        "_executed_quantity": 5,
        "_executed_price": 1650000,
        "_executed_price_total": 8000000,
        "_activated_at": "1.01.2222",
        "_executed_at": "1.01.2222",
        "_rejected_at": None,
        "_cancelled_at": None,
        "_key_creation_id": "apk_keykeykeykeykeykeykeykeykeykeykeyk",
        "_key_activation_id": "apk_keykeykeykeykeykeykeykeykeykeykeyk"
    }


def test_from_result(executed_order_data):

    result = lemon.core.orders.Order.from_result(executed_order_data)

    assert isinstance(result, lemon.core.orders.Order)
