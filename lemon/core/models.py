from datetime import datetime
import logging
import signal
import threading
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

from lemon.common.requests import ApiOauth2, ApiRequest

from lemon.core.strategy import Strategy


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
                signal.signal(signal.SIGALRM, self.__timeout_handler)
                signal.alarm(self._time_to_expire)

        except Exception as e:
            raise e

    def __timeout_handler(self, signal, frame):
        logging.info("Session token expired, refreshing..")
        self.refresh
        logging.info("Token refreshed.")

    @property
    def refresh(self):
        self.__auth_api()
        return True

    @property
    def token(self):
        return self._token


class Space(Session):
    """Every Account has multiple spaces which will run themsselfs a specific trading strategy. 
    So each Space has his own balance and cash_to_invest.
    """
    # session: Session
    name: str = None
    # _uuid: str = None
    balance: float = 0.0
    cash_to_invest: float = 0.0
    type: str

    def __init__(self, credentials: dict, s: Strategy = None) -> None:
        self.__cred = credentials
        self._strategy = s
        self.__start_session()
        self.__fetch_space_state()
        logging.debug(f"Space created: {self.name}")

    def __repr__(self):
        return f'Space(Name: {self.name}, Balance: {self.balance}, Cash: {self.cash_to_invest})'

    def __hash__(self):
        return hash(self.name)

    def __start_session(self):
        self.session = Session(self.__cred)

    def __fetch_space_state(self):
        request = ApiRequest(type="trading",
                             endpoint="/spaces/",
                             method="GET",
                             authorization_token=self.session.token)
        self._uuid = request.response[0]['uuid']
        self.name = request.response[0]['name']
        self.balance = request.response[0]['state']['balance']
        self.cash_to_invest = request.response[0]['state']['cash_to_invest']
        self.type = request.response[0]['type']

    def portfolio(self) -> dict:
        """lists all portfolio transactions that affect the cash amount available for your space

        Returns:
            dict: [description]
        """
        request = ApiRequest(type="trading",
                             endpoint="/spaces/{}/portfolio/".format(
                                 self._uuid),
                             method="GET",
                             authorization_token=self.session.token)
        return request.response

    def portfolio_tranactions(self) -> dict:
        """Requesting which positions were added to your portfolio through which transaction.
        Returns:
            dict: [description]
        """
        request = ApiRequest(type="trading", endpoint="/spaces/{}/portfolio/transactions/".format(self._uuid),
                             method="GET",
                             authorization_token=self.session.token)
        return request.response

    def transactions(self, **kwargs) -> dict:
        """Requesting all transactions that are related to this space

        Returns:
            dict: returns the api response as a dict
        """
        payload = {name: kwargs[name]
                   for name in kwargs if kwargs[name] is not None}

        if sum(payload.values()) is not 0:
            payload = "?=" + urlencode(payload, doseq=True)
        else:
            payload = ""

        request = ApiRequest(type="trading", endpoint="/spaces/{}/transactions/{}".format(self._uuid, payload),
                             method="GET",
                             authorization_token=self.session.token)
        return request.response

    def transaction_by_id(self, t_uuid) -> dict:
        """Requesting a specific transaction that is related to this space

        Args:
            t_uuid ([type]): Basic unique transaction identifier 

        Returns:
            dict: returns the api response as a dict
        """
        request = ApiRequest(type="trading", endpoint="/spaces/{}/transactions/{}/".format(self._uuid, t_uuid),
                             method="GET",
                             authorization_token=self.session.token)
        return request.response

    def orders(self, **kwargs) -> dict:
        """Requesting all orders that are related to this space

        Returns:
            dict:  api response as a dict

        """
        payload = {name: kwargs[name]
                   for name in kwargs if kwargs[name] is not None}

        if sum(payload.values()) is not 0:
            payload = "?=" + urlencode(payload, doseq=True)
        else:
            payload = ""

        request = ApiRequest(type="trading", endpoint="/spaces/{}/orders/{}".format(self._uuid, payload),
                             method="GET",
                             authorization_token=self.session.token)
        return request.response

    def order_by_id(self, order_uuid: str) -> dict:
        """Requesting a specific order that is related to this space

        Args:
            order_uuid (str): Basic unique identifier 

        Returns:
            dict: returns the api response as a dict
        """
        request = ApiRequest(type="trading", endpoint="/spaces/{}/orders/{}/".format(self._uuid, order_uuid),
                             method="GET",
                             authorization_token=self.session.token)
        return request.response

    def create_order(self, isin: str, valid_until: datetime.timestamp, side: str, quantity: int, stop_price: int = None, limit_price: int = None):
        """Create an inactive order within this space

        Args:
            isin (str): Insturment ID
            valid_until (datetime.timestamp): Datetime, until the order will be vaild and inactive
            side (str): "buy" or "sell2
            quantity (int): Number of positions traded
            stop_price (int, optional):  Defaults to None.
            limit_price (int, optional): Defaults to None.

            Market Order:	    The order is immediately executed at the next possible price.
            Stop Market Order:	Once the stop price is met, the order is converted into a market order. After that, the order is executed immediately at the next possible price.
            Limit Order:	    The order is executed once the limit price is reached.
            Stop Limit Order:   Once the stop price is met, the order is converted into a limit order. Then, the order is executed once the limit price is met. 

        Returns:
            [type]: [description]
        """
        data = locals()
        del data['self']  # delete self argument from dict

        request = ApiRequest(type="trading", endpoint="/spaces/{}/orders/".format(self._uuid),
                             method="POST",
                             body=data,
                             authorization_token=self.session.token)

        return request.response, request.response['uuid']

    def place_order(self, order_uuid: str) -> dict:
        """Activates a pervious created order and set its state to activated

        Args:
            order_uuid (str): Order ID

        Returns:
            dict: status -> activated
        """
        request = ApiRequest(type="trading", endpoint="/spaces/{}/orders/{}".format(self._uuid, order_uuid),
                             method="PUT",
                             authorization_token=self.session.token)
        return request.response

    def delete_order(self, order_uuid: str) -> int:
        """Deleting a order

        Args:
            order_uuid (str): Order ID

        Returns:
            int: Request status code
        """

        request = ApiRequest(type="trading", endpoint="/spaces/{}/orders/{}".format(self._uuid, order_uuid),
                             method="delete",
                             authorization_token=self.session.token)
        return request.status

    @property
    def strategy(self) -> Strategy:
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """
        return self._strategy if self._strategy != None else None

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        """Replace Strategie wihle running 

        Args:
            strategy (Strategy): [description]
        """
        self._strategy = strategy

    def run(self) -> None:
        """
        The Context delegates some work to the Strategy object instead of
        implementing multiple versions of the algorithm on its own.
        """
        if self.strategy is not None:
            t1 = threading.Thread(
                target=self.strategy.do_algorithm, name=self.name)
            t1.start()
            logging.debug(f"Strategy from {self.name} started!")
        else:
            logging.warning(
                f"Space {self.name} has no actual strategy! Nothing to do!")
