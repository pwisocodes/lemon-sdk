
import logging
import threading
from dataclasses import dataclass
from datetime import datetime
from typing import List
from urllib.parse import urlencode

from lemon.common.errors import *
from lemon.common.helpers import Singleton
from lemon.common.requests import ApiRequest
from lemon.core.strategy import IStrategy


class Space():
    """Every Account has multiple spaces which will run themsselfs a specific trading strategy. 
    So each Space has his own balance and cash_to_invest.
    """

    def __init__(self, init_values: dict = None, name: str = None, type: str = None, risk_limit: str = None, trading_type: str = "paper", s: IStrategy = None) -> None:
        self._strategy = s
        self.name = name
        self.type = type
        self.risk_limit = risk_limit
        self.trading_type = trading_type

        if init_values != None:
            self.name = init_values['name']
            self.description = init_values['description']
            self._uuid = init_values['id']
            self.risk_limit = float(init_values['risk_limit'])
            self.buying_power = float(init_values['buying_power'])
            self.earnings = float(init_values['earnings'])
            self.backfire = float(init_values['backfire'])
            self.created_at = init_values['created_at']
            if trading_type == "money":
                self.linked = init_values['linked']

    def __repr__(self):
        return f'Space(Name: {self.name}, Buying_power: {self.buying_power}, Risk_limit: {self.risk_limit}, Trading_type: {self.trading_type}'

    def __hash__(self):
        return hash(self.name)

    def fetch_space_state(self):
        request = ApiRequest(type="paper",
                             endpoint="/spaces/{}/".format(self._uuid),
                             method="GET",
                             authorization_token=Account().token)
        logging.info(request.keys())
        if request.response['status'] == "ok":
            self.risk_limit = float(request.response['results']['risk_limit'])
            self.buying_power = float(
                request.response['results']['buying_power'])
            self.earnings = float(request.response['results']['earnings'])
            self.backfire = float(request.response['results']['backfire'])
        else:
            raise Exception(request.response['status'])

    @property
    def strategy(self) -> IStrategy:
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """
        return self._strategy if self._strategy != None else None

    @strategy.setter
    def strategy(self, strategy: IStrategy) -> None:
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
                f"Space {self.name} has no actual strategy! Nothing to start here!")

    def backtest(self):
        pass


@dataclass(init=True)
class AccountState():
    account_id: str = None
    firstname: str = None
    lastname: str = None
    email: str = None
    phone: str = None
    address: str = None
    billing_email: str = None
    billing_address: str = None
    billing_name: str = None
    billing_vat: str = None
    mode: str = None
    deposit_id: str = None
    client_id: str = None
    account_number: str = None
    iban_brokerage: str = None
    iban_origin: str = None
    bank_name_origin: str = None
    balance: float = None
    cash_to_invest: float = None
    cash_to_withdraw: float = None
    trading_plan: str = None
    data_plan: str = None
    tax_allowance: float = None
    tax_allowance_start: str = None
    tax_allowance_end: str = None

    def __post_init__(self):
        try:
            self.fetch_state()
        except:
            logging.warning("Cant fetch account state")

    def fetch_state(self):
        request = ApiRequest(type="paper",
                             endpoint="/account/",
                             method="GET",
                             authorization_token=self.token
                             )

        if request.response['status'] == "ok":
            self.account_id = request.response['results']['account_id']
            self.firstname = request.response['results']['firstname']
            self.lastname = request.response['results']['lastname']
            self.email = request.response['results']['email']
            self.phone = request.response['results']['phone']
            self.address = request.response['results']['address']
            self.billing_email = request.response['results']['billing_email']
            self.billing_address = request.response['results']['billing_address']
            self.billing_name = request.response['results']['billing_name']
            self.billing_vat = request.response['results']['billing_vat']
            self.mode = request.response['results']['mode']
            self.deposit_id = request.response['results']['deposit_id']
            self.client_id = request.response['results']['client_id']
            self.account_number = request.response['results']['account_number']
            self.iban_brokerage = request.response['results']['iban_brokerage']
            self.iban_origin = request.response['results']['iban_origin']
            self.bank_name_origin = request.response['results']['bank_name_origin']
            self.balance = float(request.response['results']['balance']/10000)
            self.cash_to_invest = float(request.response['results']['cash_to_invest']/10000)
            self.cash_to_withdraw = float(request.response['results']['cash_to_withdraw']/10000)
            self.trading_plan = request.response['results']['trading_plan']
            self.data_plan = request.response['results']['data_plan']
            self.tax_allowance = float(request.response['results']['tax_allowance']/10000)
            self.tax_allowance_start = request.response['results']['tax_allowance_start']
            self.tax_allowance_end = request.response['results']['tax_allowance_end']


class Account(AccountState, metaclass=Singleton):
    spaces: list

    def __init__(self, credentials: str) -> None:
        self._token = credentials
        self.paper_spaces = []
        self.real_money_spaces = []
        super().__init__()
        self.__get_spaces()

    @property
    def token(self) -> str:
        return self._token

    @property
    def spaces(self):
        return self.paper_spaces + self.real_money_spaces

    def withdrawl(self, type: str, amount: int, pin: int, idempotency: str = None):
        """ Withdraw money from your bank account to your lemon.markets account e.g. amount = 100.0 means 100€ and will be multiplyed by 10000 to get the int value the api handels. Take a look at: https://docs.lemon.markets/trading/overview#working-with-numbers-in-the-trading-api 

        Args:
            amount (float): amount of money that will be withdrawn, minimum is 100.0

        Returns:
            str: 'ok' if if request was successful
        """
        if amount > 0:
            value = amount * 10000

            body = {"amount": int(value)}
            request = ApiRequest(type="paper",
                                 endpoint="/account/withdrawals/",
                                 method="POST",
                                 body=body,
                                 authorization_token=self._token)
            if request.response['status'] == 'error':
                raise ValueError(request.response['error_message'])
        else:
            raise ValueError(f"{amount} is not a valid parameter!")

        return request.response['status']

    def documents(self) -> list:
        """ Get information about all documents linked with this account 

        Returns:
            list: arraylist of dicts
        """
        request = ApiRequest(type="paper",
                             endpoint="/account/documents/",
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            if request.response['results'] != []:
                return request.response['results']
            else:
                return "No documents found!"
        else:
            return request.response['status']

    def get_doc(self, doc_id: str) -> str:
        """ Download a specific doc by id

        Args:
            doc_id (str): ID of document

        Returns:
            str: status
        """
        request = ApiRequest(type="paper",
                             endpoint="/account/documents/{}".format(doc_id),
                             method="GET",
                             authorization_token=self._token)

        return request.response['status']

    def __get_spaces(self):
        """ Creating objects for any spaces dedicated in the credential file
        """
        request = ApiRequest(type="paper",
                             endpoint="/spaces/",
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            for space in request.response['results']:
                print(space)
                self.paper_spaces.append(
                    Space(init_values=space, trading_type="paper"))

        request = ApiRequest(type="money",
                             endpoint="/spaces/",
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            for space in request.response['results']:
                self.real_money_spaces.append(
                    Space(init_values=space, trading_type="money"))

        return request.response['status']

    def new_space(self, type: str, name: str, risk_limit: int, trading_type: str):
        if self.spaces.count() >= 10:
            return "Maximum number of spaces reached!"
        if trading_type == "paper":
            body = {"name": name, "type": type, "risk_limit": str(risk_limit)}
            request = ApiRequest(type="paper",
                                 endpoint="/spaces/",
                                 method="POST",
                                 body=body,
                                 authorization_token=self._token)

            if request.response['status'] == "ok":
                self.paper_spaces.append(
                    Space(init_values=request.response['results'], trading_type=trading_type))
            return request.response['status']
        elif trading_type == "money":
            body = {"name": name, "type": type, "risk_limit": str(risk_limit)}
            request = ApiRequest(type="money",
                                 endpoint="/spaces/",
                                 method="POST",
                                 body=body,
                                 authorization_token=self._token)

            if request.response['status'] == "ok":
                self.real_money_spaces.append(
                    Space(init_values=request.response['results'], trading_type=trading_type))

            return request.response['status']
        else:
            raise ValueError(
                f"Tradingtype {trading_type} is not a vaild type!")

    def edit_space(self, space_id: str, **kwargs) -> str:
        payload = {name: kwargs[name]
                   for name in kwargs if kwargs[name] is not None}

        request = ApiRequest(type="paper",
                             endpoint="/spaces/{}".format(space_id),
                             method="PUT",
                             body=payload,
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            filterd_list = list(
                filter(lambda x: x._uuid == space_id, self.paper_spaces))
            if filterd_list == []:
                filterd_list = list(
                    filter(lambda x: x._uuid == space_id, self.real_money_spaces))
                if filterd_list == []:
                    return f"Cant find spaces with id:{space_id}"
            else:
                if len(filterd_list) < 2:
                    filterd_list[0].name = request.response['results']['name']
                    filterd_list[0].description = request.response['results']['description']
                    filterd_list[0].risk_limit = request.response['results']['risk_limit']
                    if filterd_list[0].trading_type == "money":
                        filterd_list[0].linked = request.response['results']['linked']

        return request.response['status']

    def delete_space(self, space_id: str):
        r_value = False
        request = ApiRequest(type="paper",
                             endpoint="/spaces/{}".format(space_id),
                             method="DELETE",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            filterd_list = list(
                filter(lambda x: x._uuid == space_id, self.paper_spaces))
            if filterd_list == []:
                return f"Cant find spaces with id:{space_id}"
            else:
                self.paper_spaces.remove(filterd_list[0])
                r_value = True

        request = ApiRequest(type="money",
                             endpoint="/spaces/{}".format(space_id),
                             method="DELETE",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            filterd_list = list(
                filter(lambda x: x._uuid == space_id, self.real_money_spaces))
            if filterd_list == []:
                return f"Cant find spaces with id:{space_id}"
            else:
                self.real_money_spaces.remove(filterd_list[0])
                r_value = True

        return "Done" if r_value else "Failed"

    def space_by_name(self, name: str) -> List[Space]:
        """ Filter spaces by name 

        Args:
            name (str): Space name

        Returns:
            List[Space]: [description]
        """
        return list(filter(lambda x: x.name == name, self.spaces))

    def orders(self, type: str):
        request = ApiRequest(type=type,
                             endpoint="/orders/",
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            return request.response['results']
        return request.response['error_message']

    def delete_order(self, order_id: str, type: str) -> str:
        request = ApiRequest(type=type,
                             endpoint="/orders/{}".format(order_id),
                             method="DELETE",
                             authorization_token=self._token)

        return request.response['status']

    def order(self, order_id: str, type: str):
        request = ApiRequest(type=type,
                             endpoint="/orders/{}".format(order_id),
                             method="GET",
                             authorization_token=self._token)

        if request.response['status'] == "ok":
            return request.response['results']
        return request.response['error_message']

    def withdrawls(self, type: str):
        request = ApiRequest(type=type,
                             endpoint="/account/withdrawals/",
                             method="GET",
                             authorization_token=self._token)
        if request.response['status'] == "ok":
            return request.response['results']
        return request.response['error_message']

    # def withdraw(self, type: str, amount:int, pin:int, idempotency:str = None):
    #     body = {"amount": amount*10000, "pin": str(pin)}
    #     request = ApiRequest(type=type,
    #                          endpoint="/account/withdrawals/",
    #                          method="POST",
    #                          body=body,
    #                          authorization_token=self._token)
    #     if request.response['status'] == "ok":
    #         return request.response['results']
    #     return request.response['error_message']

    def portfolio(self, type: str, **kwargs):
        query = {name: kwargs[name]
                 for name in kwargs if kwargs[name] is not None}
        urlencode(query)

        request = ApiRequest(type=type,
                             endpoint="/portfolio/?{}".format(query),
                             method="GET",
                             authorization_token=self._token)
        if request.response['status'] == "ok":
            return request.response['results']
        return request.response['error_message']
