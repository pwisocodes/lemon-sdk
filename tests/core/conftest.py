import pytest
from lemon.core.account import Account
from lemon.common.enums import ORDERSIDE, ORDERSTATUS, ORDERTYPE, VENUE


@pytest.fixture
def status_ok_result() -> dict:
    """fixture with data of an activated order
    """
    return {
        "time": "2022-04-02T19:36:35.086+00:00",
        "mode": "paper",
        "status": "ok"
    }


@pytest.fixture
def acccount_result() -> dict:
    return {
        "time": "2022-04-02T19:46:48.942+00:00",
        "mode": "paper",
        "status": "ok",
        "results": {
            "created_at": "2021-12-21T10:28:32.188+00:00",
            "account_id": "acc_abcdefghijklmnopqrstuvwxyz12345678",
            "firstname": "Jane",
            "lastname": "Doe",
            "email": "email@example.com",
            "phone": None,
            "address": None,
            "billing_address": None,
            "billing_email": None,
            "billing_name": None,
            "billing_vat": None,
            "mode": "paper",
            "deposit_id": None,
            "client_id": None,
            "account_number": None,
            "iban_brokerage": None,
            "iban_origin": None,
            "bank_name_origin": None,
            "balance": 985900000,
            "cash_to_invest": 957965500,
            "cash_to_withdraw": 957965500,
            "amount_bought_intraday": 0,
            "amount_sold_intraday": 0,
            "amount_open_orders": 27934500,
            "amount_open_withdrawals": 100000,
            "amount_estimate_taxes": 0,
            "approved_at": None,
            "trading_plan": "free",
            "data_plan": "free",
            "tax_allowance": None,
            "tax_allowance_start": None,
            "tax_allowance_end": None
        }
    }


@pytest.fixture
def executed_order_result():
    """fixture with Data of an executed order
    """
    return {
        "isin": "US0378331005",
        "side": ORDERSIDE.BUY,
        "quantity": 5,
        "venue":  VENUE.GETTEX,
        "stop_price": None,
        "limit_price": 1700000,
        "notes": "Test Order",
        "expires_at": "2022-02-02",
        "idempotency": None,
        "status": ORDERSTATUS.EXECUTED,
        "id": "ord_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
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
        "estimated_price": 1650000,
        "estimated_price_total": 8000000,
        "created_at": "2022-01-01",
        "charge": 0,
        "chargeable_at": "2022-02-02",
        "isin_title": "APPLE INC.",
        "type": ORDERTYPE.LIMIT,
        "executed_quantity": 5,
        "executed_price": 1650000,
        "executed_price_total": 8000000,
        "activated_at": "2022-01-01",
        "executed_at": "2022-01-01",
        "rejected_at": None,
        "cancelled_at": None,
        "key_creation_id": "apk_keykeykeykeykeykeykeykeykeykeykeyk",
        "key_activation_id": "apk_keykeykeykeykeykeykeykeykeykeykeyk"
    }


@pytest.fixture
def account(mocker) -> Account:
    def mock_fetch_state(self):
        return
    mocker.patch(
        'lemon.core.account.AccountState.fetch_state',
        mock_fetch_state
    )
    acc = Account("123")

    return acc
