import threading

import requests
import pandas as pd
import time
import datetime
import hmac
import hashlib
import time
import base64
import urllib
import json
import asyncio
# import numpy as np
# Replace YOUR_API_KEY with your actual API key
# from ChannelMessages import getLastMessage

# APIURL = "https://api-swap-rest.bingbon.pro"
# API_KEY = 'v29D1wyTsUbNLfinjqqgorjRV5nMyPJgrWye80AxnhiAQrP4wAo3RmU34otFehnHJcjOoZCLkJzLcNB5ZKyyQ'
# SECRET_KEY = '96ou8MIZzN9mXgZVEjFxMLwWM4iDrivKJ4eDx3gYyZ4LR5F0yzrkvbUdgzpiX1p8EbVyC8qgHfC1Zyzqg'

# Define a list of your favorite cryptocurrencies
from utils import SECRET_KEY, API_KEY, APIURL

coins = ['BTC', 'ETH', 'XRP']
lastOrderId = None
def genSignature(path, method, paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    paramsStr = method + path + paramsStr
    return hmac.new(SECRET_KEY.encode("utf-8"), paramsStr.encode("utf-8"), digestmod="sha256").digest()

def post(url, body):
    req = urllib.request.Request(url, data=body.encode("utf-8"), headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req).read()

def getBalance():
    paramsMap = {
        "apiKey": API_KEY,
        "timestamp": int(time.time()*1000),
        "currency": "USDT",
    }
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    paramsStr += "&sign=" + urllib.parse.quote(base64.b64encode(genSignature("/api/v1/user/getBalance", "POST", paramsMap)))
    url = "%s/api/v1/user/getBalance" % APIURL
    return post(url, paramsStr)

def getPositions(symbol):
    paramsMap = {
        "symbol": symbol,
        "apiKey": API_KEY,
        "timestamp": int(time.time()*1000),
    }
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    paramsStr += "&sign=" + urllib.parse.quote(base64.b64encode(genSignature("/api/v1/user/getPositions", "POST", paramsMap)))
    url = "%s/api/v1/user/getPositions" % APIURL
    return post(url, paramsStr)

def placeOrder(symbol, side, price, volume, tradeType, action):
    paramsMap = {
        "symbol": symbol,
        "apiKey": API_KEY,
        "side": side,
        "entrustPrice": price,
        "entrustVolume": volume,
        "tradeType": tradeType,
        "action": action,
        "timestamp": int(time.time()*1000),
    }
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    paramsStr += "&sign=" + urllib.parse.quote(base64.b64encode(genSignature("/api/v1/user/trade", "POST", paramsMap)))
    url = "%s/api/v1/user/trade" % APIURL
    return post(url, paramsStr)

def cancleOrder(symbol,orderId):
    paramsMap = {
        "symbol": symbol,
        "apiKey": API_KEY,
        "orderId": orderId,
        "timestamp": int(time.time()*1000),
    }
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    paramsStr += "&sign=" + urllib.parse.quote(base64.b64encode(genSignature("/api/v1/user/trade", "POST", paramsMap)))
    url = "%s/api/v1/user/trade" % APIURL
    return post(url, paramsStr)

def getLatestPrice(symbol):
    paramsMap = {
        "symbol": symbol,
    }
    paramsStr = "&sign=" + urllib.parse.quote(base64.b64encode(genSignature("/api/v1/market/getLatestPrice", "GET", paramsMap)))
    url = f'https://api-swap-rest.bingbon.pro/api/v1/market/getLatestPrice?&symbol={symbol}{paramsStr}'
    payload = {}
    headers = {
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text



def main():
    # print(getLatestPrice("BTC-USDT"))
    # thr = threading.Thread(target=getLastMessage, args=(), kwargs={})
    # thr.start()
    # coro = getLastMessage()
    # asyncio.run(coro)
    # loop = asyncio.get_event_loop()

    # print("getBalance:", getBalance())
    # while True:
    #     getLastMessage()
        # print("getLastPrice :", getLatestPrice("BTC-USDT"))
        # result = loop.run_until_complete(coro)
        # time.sleep(3)

    # placeOrder("ETH-USDT", "Bid", 0, 0.02, "Market", "Open")
    # result = placeOrder("ETH-USDT", "Bid", 0, 0.01, "Market", "Open")
    # my_json = result.decode('utf8').replace("'", '"')
    # print(my_json[3])
    # print("placeOpenOrder:", placeOrder("DOGE-USDT", "Bid", 0,2, "Market", "Open"))

    # print("getPositions:", getPositions("BTC-USDT"))

    # print("placeCloseOrder:", placeOrder("BTC-USDT", "Ask", 0, 0.0004, "Market", "Close"))

if __name__ == "__main__":
    main()

