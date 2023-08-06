from uuid import uuid4
import datetime
import sys
import pyotp
import os
from dotenv import load_dotenv
load_dotenv()
import requests

import robin_stocks.robinhood as r
import robin_stocks.gemini as g
import robin_stocks.tda as t


# totp  = pyotp.TOTP(os.environ['robin_mfa']).now()
# print("Current OTP:", totp)
# login = r.login(os.environ['robin_username'], os.environ['robin_password'], store_session=True, mfa_code=totp)
# # print("login data is ", login)

# print("===")
# print("running test at {}".format(datetime.datetime.now()))
# print("===")

# order = r.get_watchlist_by_name("test")
# print(order)

g.login("account-Dsugh2UMPP4CRRTvibCa", "jiWyAYDggrbF8Ut9pzWXVguj8yw")
# generate_signature({"request": "/v1/mytrades", "symbol": "btcusd"})

# response = SESSION.post("https://api.gemini.com/v1/mytrades")

# my_trades = response.json()
# g.set_default_json_flag(True)
for i in range(10):
    my_trades, error = g.get_trades_for_crypto("btcusd")
    print(my_trades.json())
