from abc import ABC, abstractmethod
from common.helpers import Singleton
from dataclasses import dataclass

from client.auth import credentials
from common.requests import ApiOauth2, ApiRequest

from core.strategy import Strategy


class Session:
    _time_to_expire: int
    _token: str

    def __init__(self, cred: dict) -> None:
        self._cred = cred
        self.refresh

    def __auth_api(self):
        try:
            if self._cred:
                request = ApiOauth2(credentials=self._cred)

                self._token = request.response['access_token']
                self._time_to_expire = int(request.response['expires_in'])
                

        except Exception as e:
            raise e

    @property
    def refresh(self):
        self.__auth_api()
        return True

    @property
    def token(self):
        return self._token


@dataclass
class Space(Session):
    """Every Account has multiple spaces which will run themsselfs a specific trading strategy. 
    So each Space has his own balance and cash_to_invest.
    """
    session: Session
    name: str = None
    _uuid: str = None
    balance: float = 0.0
    cash_to_invest: float = 0.0

    def __init__(self, strategy: Strategy = None, credentials: dict = None) -> None:
        self.__cred = credentials
        self._strategy = strategy
        self._start_session()
        self._fetch_space_state()

    def _start_session(self):
        self.session = Session(self.__cred)

    def _fetch_space_state(self):
        request = ApiRequest(endpoint="/spaces/",
                             method="GET",
                             authorization_token=self.session.token)
        print(f"Space Response: {request.response}, Token: {self.session.token}")

    @property
    def strategy(self) -> Strategy:
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        """Replace Strategie wihle running 

        Args:
            strategy (Strategy): [description]
        """

        self._strategy = strategy

    def run_strategy(self) -> None:
        """
        The Context delegates some work to the Strategy object instead of
        implementing multiple versions of the algorithm on its own.
        """
        pass
