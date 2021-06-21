

from common.helpers import Singleton
from dataclasses import dataclass
from typing import List

from client.auth import credentials
from common.errors import *
from common.requests import ApiOauth2, ApiRequest

from core.models import Space
from core.strategy import Strategy


class AccountState:
    _balance: float = None
    _cash_accounts: int = None
    _securities_account_number: int = None

    def fetch_account_state(self):
        request = ApiRequest(
            endpoint="/state/",
            method="GET",
            authorization_token=Account.instance().token
        )

        self._balance = request.response['state']['balance']
        self._cash_accounts = request.response['cash_account_number'] if not None else None
        self._cash_accounts_securities_account_number = request.response[
            'securities_account_number'] if not None else None

    @property
    def balance(self) -> float:
        self.fetch_account_state()
        return self._balance

    @property
    def cash_accounts(self) -> int:
        self.fetch_account_state()
        return self._cash_accounts

    @property
    def securities_accounts(self) -> int:
        self.fetch_account_state()
        return self._securities_account_number


@Singleton
class Account(AccountState):
    _token: str

    def __init__(self) -> None:
        super().__init__()
        self.spaces = list()
        self.create_spaces()
        self._token = self.spaces[0].session.token
        self._fetch_spaces_states()

    def create_spaces(self):
        for s in credentials():
            self.spaces.append(Space(credentials=s))

    def _fetch_spaces_states(self):
        request = ApiRequest(endpoint="/spaces/",
                             method="GET",
                             authorization_token=self._token)
        print(f"Account Response: {request.response}, Token: {self._token}")

    @property
    def token(self) -> str:
        self.refresh_token()
        return self._token

    def refresh_token(self):
        self._token = self.spaces[0].session.token
