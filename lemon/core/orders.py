import datetime
import json
from lemon.common.requests import ApiRequest
from lemon.core.account import *

class Order():
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

    def __init__(self, isin:str, expired_at, side:str, quantity:int, venue:str, trading_type:str, stop_price:int = None, limit_price:int = None, notes:str= None) -> None:
        self.trading_type = trading_type
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

        request = ApiRequest(type=self.trading_type,
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
        if self.trading_type == "paper":
            type="paper"
        else:
            type="money"
            data = json.dumps({"pin": pin})


        request = ApiRequest(type=type,
                             endpoint=f"/orders/{self.id}/activate/",
                             method="POST",
                             body=data if type=="money" else None,
                             authorization_token=Account().token
                             )
        
        return request.response['status']

    def delete(self)->str:
        pass
