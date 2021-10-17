# Lemon.markets inoffical Python SDK


## Install

Running following command will install all project dependencies. You have to install Python and poetry first.  
```python
$ poetry install
```

## How to use? 

```Python
from client.auth import credentials
from core.account import Account
import datetime
```
Get a account instance and show its balance and spaces.
```python
$ acc = Account.instance()
$ acc.balance
'85000.0000'
$ acc.spaces
[Space(Name: #1 HelloWorldStrategy, Balance: 4550.9000, Cash: 3772.2100),
 Space(Name: #2 MeanRevTest, Balance: 5000.0000, Cash: 5000.0000),
 Space(Name: #3 AnotherStrategy, Balance: 5000.0000, Cash: 5000.0000)]
```
Viewing space orders
```python
$ acc.spaces[0].orders()
{'next': None,
 'previous': None,
 'results': [{'valid_until': 1634248800.0,
   'side': 'buy',
   'quantity': 1,
   'stop_price': None,
   'limit_price': None,
   'uuid': '9cbc5ab6-3d29-43a5-a595-ef697a482b67',
   'status': 'inactive',
   'average_price': '0.0000',
   'created_at': 1634230481.181818,
   'type': 'market',
   'processed_at': None,
   'processed_quantity': 0,
   'trading_venue_mic': 'xmun',
   'instrument': {'isin': 'US88160R1014', 'title': 'TESLA INC.'}},
  {'valid_until': 1624625441.0,
   'side': 'buy',
   'quantity': 1,
   'stop_price': None,
   'limit_price': None,
   'uuid': '36989a25-e87b-4699-ae1e-0f31189a94ae',
   'status': 'deleted',
   'average_price': '0.0000',
   'created_at': 1624548738.299171,
   ...
```
