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
# import numpy as np
# Replace YOUR_API_KEY with your actual API key
APIURL = "https://api-swap-rest.bingbon.pro"
API_KEY = 'v29D1wyTsUbNLfinjqqgorjRV5nMyPJgrWye80AxnhiAQrP4wAo3RmU34otFehnHJcjOoZCLkJzLcNB5ZKyyQ'
SECRET_KEY = '96ou8MIZzN9mXgZVEjFxMLwWM4iDrivKJ4eDx3gYyZ4LR5F0yzrkvbUdgzpiX1p8EbVyC8qgHfC1Zyzqg'

# Define a list of your favorite cryptocurrencies
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

# def getposition():
#     asset = "ICX-USDT"
#     timestamp = round(time.time() * 1000)
#
#     # url = "https://api-swap-rest.bingbon.pro/api/v1/user/getPositions?symbol=BTC-USDT&apiKey=v29D1wyTsUbNLfinjqqgorjRV5nMyPJgrWye80AxnhiAQrP4wAo3RmU34otFehnHJcjOoZCLkJzLcNB5ZKyyQ&timestamp=1680854882890&sign=ST060Grop95aRb7KR%2Fz4rrER4llHlNRAztuaEgkUbCU%3D"
#     originString = f'POST/api/v1/user/getPositionsapiKey={API_KEY}&symbol={asset}&timestamp={timestamp}'
#
#     signature = (base64.b64encode(
#         hmac.new(bytes(SECRET_KEY, 'utf-8'), bytes(originString, 'utf-8'), digestmod=hashlib.sha256).digest()).decode(
#         "utf-8"))
#
#     paramstring = (str("apiKey=") +
#                    str(API_KEY) +
#                    str("&symbol=") +
#                    str(asset) +
#                    str("&timestamp=") +
#                    str(timestamp))
#     url = f'https://api-swap-rest.bingbon.pro/api/v1/user/getPositions?&{paramstring}&sign={str(signature)}'
#     payload = {}
#     headers = {
#     }
#
#     response = requests.request("POST", url, headers=headers, data=payload)
#
#     print(response.text)
# def getbalance():
#     asset = "BTC"
#     timestamp = round(time.time() * 1000)
#     paramstring = (str("apiKey=") +
#                    str(API_KEY) +
#                    str("&currency=") +
#                    str(asset) +
#                    str("&timestamp=") +
#                    str(timestamp))
#
#
#     originString = f'POST/api/v1/user/getBalanceapiKey={API_KEY}&currency=USDT&timestamp={timestamp}'
#
#     signature = (base64.b64encode(
#         hmac.new(bytes(SECRET_KEY, 'utf-8'), bytes(originString, 'utf-8'), digestmod=hashlib.sha256).digest()).decode(
#         "utf-8"))
#     # print(signature)
#     url = f'https://api-swap-rest.bingbon.pro/api/v1/user/getBalance?&{paramstring}&sign={str(signature)}'
#     payload = {}
#     headers = {
#     }
#
#     response = requests.request("POST", url, headers=headers, data=payload)
#
#     print(response.text)


def main():
    # print("getBalance:", getBalance())
    lastOrderId = placeOrder("BTC-USDT", "Bid", 0, 0.0004, "Market", "Open")
    print("placeOpenOrder:", placeOrder("BTC-USDT", "Bid", 0, 0.0004, "Market", "Open"))

    # print("getPositions:", getPositions("BTC-USDT"))

    # print("placeCloseOrder:", placeOrder("BTC-USDT", "Ask", 0, 0.0004, "Market", "Close"))

if __name__ == "__main__":
    main()
while True:
    # price_data = get_all_price_data()
    # df = calculate_percentage_changes(price_data)
    # display_data(df)

    time.sleep(3)
