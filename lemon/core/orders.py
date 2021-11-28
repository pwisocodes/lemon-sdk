import datetime
import json
from lemon.common.requests import ApiRequest
from lemon.core.account import *

class Order():
    space_id:str
    isin:str
    side:str
    quantity:int
    venue:str
    stop_price:int = None
    limit_price:int = None
    notes:str = None
    status:str
    id:str
    regulatory_information:dict = None

    def __init__(self, isin:str, expired_at, side:str, quantity:int, venue:str, space_id:str, stop_price:int = None, limit_price:int = None, notes:str= None) -> None:
        self.space_id = space_id
        self.isin = isin
        self.side = side
        self.quantity = quantity
        self.venue = venue
        self.stop_price = stop_price
        self.limit_price = limit_price
        self.notes = notes
        self.expired_at = expired_at
        self.__create()

    def __create(self):
        if list(filter(lambda x: x._uuid == self.space_id, Account().spaces))[0].trading_type == "paper":
            type="paper"
        else:
            type="money"

        request = ApiRequest(type=type,
                             endpoint="/orders/",
                             method="POST",
                             body=self.__dict__,
                             authorization_token=Account().token
                             )

        if request.response['status'] == "ok":
            self.status = request.response['results']['status']
            self.id = request.response['results']['id']
            self.regulatory_information = request.response['results']['regulatory_information']
            self.estimated_price = request.response['results']['estimated_price']

            return f"Order with id: {self.id} created!"
        return f"Order cant be created!"
        
        
    def activate(self, pin:str=None)->str:
        if list(filter(lambda x: x._uuid == self.space_id, Account().spaces))[0].trading_type == "paper":
            type="paper"
        else:
            type="money"
            data = json.dumps({"pin": pin})


        request = ApiRequest(type=type,
                             endpoint="/orders/{}/activate/".format(self.id),
                             method="POST",
                             body=data if type=="money" else None,
                             authorization_token=Account().token
                             )
        
        return request.response['status']

    def delete(self)->str:
        pass
