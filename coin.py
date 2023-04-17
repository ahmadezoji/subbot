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
import matplotlib.pyplot as plt
from utils import APIURL, SECRET_KEY

coins = ['BTC', 'ETH', 'XRP']
lastOrderId = None
def getLatestKline(symbol):
    paramsMap = {
        "symbol": symbol,
        "klineType": "1D",
    }
    paramsStr = "&sign=" + urllib.parse.quote(
        base64.b64encode(genSignature("/api/v1/market/getLatestKline", "GET", paramsMap)))
    url = f'{APIURL}/api/v1/market/getLatestKline?&symbol={symbol}&klineType=1D{paramsStr}'
    payload = {}
    headers = {
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text
def getHistory(symbol,klineType,startTs,endTs):
    paramsMap = {
        "symbol": symbol,
        "klineType": klineType,
        "startTs": startTs,
        "endTs": endTs ,
    }

    paramsStr = "&sign=" + urllib.parse.quote(
        base64.b64encode(genSignature("/api/v1/market/getHistoryKlines", "GET", paramsMap)))
    url = f'{APIURL}/api/v1/market/getHistoryKlines?&symbol={symbol}&klineType={klineType}&startTs={startTs}&endTs={endTs}{paramsStr}'
    payload = {}
    headers = {
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text
def genSignature(path, method, paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    paramsStr = method + path + paramsStr
    return hmac.new(SECRET_KEY.encode("utf-8"), paramsStr.encode("utf-8"), digestmod="sha256").digest()

def main():
    result  = getHistory("BTC-USDT","5",1680454227000,int(time.time() * 1000))
    json_object = json.loads(result)

    mlist = list(json_object["data"]["klines"])
    times = []
    prices = []
    for item in mlist:
        times.append(datetime.datetime.fromtimestamp(int(item["time"])/1000.0))
        prices.append(item["high"])

    # Program to calculate moving average
    window_size = 50

    i = 0
    # Initialize an empty list to store moving averages
    moving_averages = []

    # Loop through the array to consider
    # every window of size 3
    while i < len(prices) - window_size + 1:
        # Store elements from i to i+window_size
        # in list to get the current window
        window = prices[i: i + window_size]

        # Calculate the average of current window
        window_average = round(sum(window) / window_size, 2)

        # Store the average of current
        # window in moving average list
        moving_averages.append(window_average)

        # Shift window to right by one position
        i += 1

    # print(moving_averages)
    plt.plot(times, moving_averages)
    plt.xlabel('Time (hr)')
    plt.ylabel('prices (USDT)')
    plt.show()

    # for value in result:
    #     value.data
    # print(getLatestKline("BTC-USDT"))
    # print("getBalance:", getBalance())
    # while True:
    #     print("getLastPrice :", getLatestPrice("BTC-USDT"))
    #     time.sleep(3)

    # placeOrder("ETH-USDT", "Bid", 0, 0.02, "Market", "Open")
    # result = placeOrder("ETH-USDT", "Bid", 0, 0.01, "Market", "Open")
    # my_json = result.decode('utf8').replace("'", '"')
    # print(my_json[3])
    # print("placeOpenOrder:", placeOrder("DOGE-USDT", "Bid", 0,2, "Market", "Open"))

    # print("getPositions:", getPositions("BTC-USDT"))

    # print("placeCloseOrder:", placeOrder("BTC-USDT", "Ask", 0, 0.0004, "Market", "Close"))

if __name__ == "__main__":
    main()

