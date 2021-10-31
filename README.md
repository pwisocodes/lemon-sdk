# Lemon.markets inoffical Python SDK




## Install

Running following command will install all project dependencies. You have to install Python and poetry first.  
```python
$ poetry install
```

## How to start? 

1. Setup your spaces on dashboard.lemon.markets 
2. create a credatianls yml file with the following structure:

```yaml
lemon-markets:
  Space:
      - # Space 1
        client_id: "************************************"
        client_secret: "********************************************"
        grant_type: client_credentials
      - # Space 2
        client_id: "******************************+*****"
        client_secret: "********************************************"
        grant_type: client_credentials
      - # Space 3
        client_id: "************************************"
        client_secret: "********************************************"
        grant_type: client_credentials
```
3. Export your credentials to your Enviroment variables: 

```shell
LEMON_CREDENTIALS='credentials.yml'
export LEMON_CREDENTIALS
```

Tip: If you're using a virtual enviroment you can copy the two lines above and paste them into the activate script of your enviroment. Otherwise you have to export these credentails again, if you have switched your enviroment.

4. You're good to go! :) 

## How to use?
Get a account instance and show its balance and spaces.
```Python
from lemon.core.account import Account

$ acc = Account()
$ acc.balance
'85000.0000'
$ acc.spaces
[Space(Name: #1 HelloWorldStrategy, Balance: 4550.9000, Cash: 3772.2100),
 Space(Name: #2 MeanRevTest, Balance: 5000.0000, Cash: 5000.0000),
 Space(Name: #3 AnotherStrategy, Balance: 5000.0000, Cash: 5000.0000)]
```

