import pytest
from tests.core.conftest import account, acccount_result, status_ok_result
from lemon.core.account import Account, AccountState


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


def test_withdraw(mocker, status_ok_result, account):
    def mock_perform_request(self):
        self._response = status_ok_result
    mocker.patch(
        'lemon.core.orders.ApiRequest._perform_request',
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
        'lemon.core.orders.ApiRequest._perform_request',
        mock_perform_request
    )

    withdrawals = account.withdrawals()

    assert len(withdrawals) == 5

    assert withdrawals[0]["amount"] == 100000

    assert withdrawals[1]["id"] == "wtd_pyQhdXXDDHsr556LmHJcS4XPR8SDLSw9sb"
