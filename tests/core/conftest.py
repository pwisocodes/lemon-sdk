import pytest
from lemon.core.account import Account


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
def account_result() -> dict:
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


@pytest.fixture
def account(mocker) -> Account:
    def mock_fetch_state(self):
        return account_result
    mocker.patch(
        'lemon.core.account.AccountState.fetch_state',
        mock_fetch_state
    )
    acc = Account("123")

    return acc
