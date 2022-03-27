import datetime
import json
from lemon.common.requests import ApiRequest
from lemon.core.account import *

class Order():
    _isin:str
    _side:str
    _quantity:int
    _venue:str
    _stop_price:int = None
    _limit_price:int = None
    _notes:str = None

    _status:str= None
    _id:str = None
    _regulatory_information:dict = None
    _estimated_price: int = None

    _is_placed: bool = False

    def __init__(self, isin:str, expired_at, side:str, quantity:int, venue:str, trading_type:str, stop_price:int = None, limit_price:int = None, notes:str= None) -> None:
        self._trading_type = trading_type
        self._isin = isin
        self._side = side
        self._quantity = quantity
        self._venue = venue
        self._stop_price = stop_price
        self._limit_price = limit_price
        self._notes = notes
        self._expired_at = expired_at

    def place(self):
        if self._is_placed:
            raise Exception(f"Order is already placed. Order-ID: {self._id}") #TODO
        
        # Remove _ from self.__dict__ to make names fit
        body= {k[1:] : v for k,v in self.__dict__.items()}

        request = ApiRequest(type=self._trading_type,
                             endpoint="/orders/",
                             method="POST",
                             body=body,
                             authorization_token=Account().token
                             )

        if request.response['status'] == "ok":
            self._is_placed=True

            self._status = request.response['results']['status']
            self._id = request.response['results']['id']
            self._regulatory_information = request.response['results']['regulatory_information']
            self._estimated_price = request.response['results']['estimated_price']


            return f"Order with id: {self._id} created!"

        raise Exception(f"Request cannot be created: \"{request.response['error_message']}\"")
        
        
    def activate(self, pin:str=None)->str:
        if not self._is_placed:
            raise Exception("Order must first be placed") # TODO

        if self._trading_type == "paper":
            type="paper"
        else:
            type="money"
            data = json.dumps({"pin": pin})


        request = ApiRequest(type=type,
                             endpoint=f"/orders/{self._id}/activate/",
                             method="POST",
                             body=data if type=="money" else None,
                             authorization_token=Account().token
                             )
        
        return request.response['status']

    def cancel(self)->str:
        if self._is_placed:
            return Account().cancel_order(self._id)
        else:
            return 'ok'
        

    @property
    def isin(self):
        return self._isin

    @isin.setter
    def isin(self, value):
        if self._is_placed:
            raise Exception("Can't modify attributes after Order is placed")
        else:
            self._isin = value

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, value):
        if self._is_placed:
            raise Exception("Can't modify attributes after Order is placed")
        else:
            self._side = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if self._is_placed:
            raise Exception("Can't modify attributes after Order is placed")
        else:
            self._quantity = value

    @property
    def venue(self):
        return self._venue

    @venue.setter
    def venue(self, value):
        if self._is_placed:
            raise Exception("Can't modify attributes after Order is placed")
        else:
            self._venue = value    

    @property
    def stop_price(self):
        return self._stop_price

    @stop_price.setter
    def stop_price(self, value):
        if self._is_placed:
            raise Exception("Can't modify attributes after Order is placed")
        else:
            self._stop_price = value

    @property
    def limit_price(self):
        return self._limit_price

    @limit_price.setter
    def limit_price(self, value):
        if self._is_placed:
            raise Exception("Can't modify attributes after Order is placed")
        else:
            self._limit_price = value

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, value):
        if self._is_placed:
            raise Exception("Can't modify attributes after Order is placed")
        else:
            self._notes = value

    @property
    def expired_at(self):
        return self._expired_at

    @expired_at.setter
    def expired_at(self, value):
        if self._is_placed:
            raise Exception("Can't modify attributes after Order is placed")
        else:
            self._expired_at = value

    # Available after placed

    @property
    def id(self):
        if self._is_placed:
            return self._id
        else:
            raise Exception("Not available until placed") # TODO

    @property
    def status(self):
        if self._is_placed:
            return self._expired_at
        else:
            return "draft"

    @property
    def regulatory_information(self):
        if self._is_placed:
            return self._regulatory_information
        else:
            raise Exception("Not available until placed") # TODO

    @property
    def estimated_price(self):
        if self._is_placed:
            return self._estimated_price
        else:
            raise Exception("Not available until placed") # TODO