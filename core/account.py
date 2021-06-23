

from typing import List
from urllib.parse import urlencode

from client.auth import credentials
from common.errors import *
from common.helpers import Singleton
from common.requests import ApiRequest


from core.models import Space


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

    def create_spaces(self):
        for s in credentials():
            self.spaces.append(Space(credentials=s))

    def space_by_name(self, name: str) -> List[Space]:
        return list(filter(lambda x: x.name == name, self.spaces))

    def search_instrument(self, name: str, type: str = ["stock", "bond", "fond", "ETF", "warrant"], **kwargs):
        """[summary]

        Args:
            name (str): [description]
            type (str, optional): [description]. Defaults to ["stock", "bond", "fond", "ETF", "warrant"].

        Raises:
            ValueError: [description]
        """
        if type not in ["stock", "bond", "fond", "ETF", "warrant"]:
            raise ValueError(f"Parameter {type} is not a valid parameter!")

        payload = {name: kwargs[name]
                   for name in kwargs if kwargs[name] is not None}
        if payload is not None:
            payload = "&" + urlencode(payload, doseq=True)

        query_str = urlencode({'name': name, 'type': type}, doseq=True)

        request = ApiRequest(
            endpoint="/instruments/?search={}".format(query_str + payload),
            method="GET",
            authorization_token=self._token)
        return request.response

    def run(self):
        for space in self.spaces:
            space.run()

    @property
    def token(self) -> str:
        self.refresh_token()
        return self._token

    def refresh_token(self):
        self._token = self.spaces[0].session.token
