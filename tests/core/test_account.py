import pytest
from tests.core.conftest import account, acccount_result, status_ok_result
from lemon.core.account import Account, AccountState


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
