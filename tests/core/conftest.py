import pytest
from lemon.core.account import Account


@pytest.fixture
def status_ok_result():
    """fixture with data of an activated order
    """
    return {
        "time": "2022-04-02T19:36:35.086+00:00",
        "mode": "paper",
        "status": "ok"
    }


@pytest.fixture
def acccount_result():
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
def account(mocker):
    def mock_fetch_state(self):
        return
    mocker.patch(
        'lemon.core.account.AccountState.fetch_state',
        mock_fetch_state
    )
    acc = Account("123")

    return acc
