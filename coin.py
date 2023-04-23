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
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

import csv
from utils import APIURL, SECRET_KEY
from sklearn.metrics import accuracy_score, classification_report

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
def loadData():
    result  = getHistory("BTC-USDT","60",1679244507000,int(time.time() * 1000))
    json_object = json.loads(result)
    mlist = list(json_object["data"]["klines"])
    times = []
    prices = []
    header = ['close', 'volume','ma_50', 'rsi_14', 'direction']
    with open('crypto_data.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    for item in mlist:
        data = [item["close"], item["volume"],0,0,0]
        times.append(item["time"])
        prices.append(item["close"])
        with open('crypto_data.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    showData(times,prices)
def arrangeData():
    df = pd.read_csv('crypto_data.csv')
    df['ma_50'] = df['close'].rolling(window=50).mean()
    df['ma_50'] = df['ma_50'].fillna(0)

    print(df)
    # Calculate price changes
    delta = df['close'].diff()

    # Calculate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)

    # Calculate the average gains and losses over the past 14 days
    avg_gain = gains.rolling(window=14).mean()
    avg_loss = losses.rolling(window=14).mean()

    # Calculate the Relative Strength (RS) and RSI
    rs = avg_gain / avg_loss
    df['rsi_14'] = 100 - (100 / (1 + rs))

    # Define the direction based on the price change
    df.loc[delta > 0, 'direction'] = 1
    df.loc[delta <= 0, 'direction'] = 0

    df['direction'] = df['direction'].fillna(0)
    df['rsi_14'] = df['rsi_14'].fillna(0)


    df.to_csv('crypto_data_new.csv', sep=',', encoding='utf-8')
def showData(times,prices):
    i = 0
    window_size = 50
    moving_averages = []
    print(f'length = {len(prices)}')
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
    plt.plot(times, prices)
    plt.xlabel('Time (hr)')
    plt.ylabel('prices (USDT)')
    plt.show()


def main():
    loadData()
    arrangeData()
    estimate_direction()


def estimate_direction():
    df = pd.read_csv('crypto_data_new.csv')
    # Define the features and target variable
    features = ['close', 'volume', 'ma_50', 'rsi_14']
    target = 'direction'

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

    # Train a logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate the model on the testing set
    y_pred = model.predict(X_test)
    print('Accuracy:', accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # Make predictions on new data
    new_data = pd.DataFrame({'close': [1000], 'volume': [2000], 'ma_50': [1050], 'rsi_14': [70]})
    direction = model.predict(new_data)
    print('Direction:', direction)
if __name__ == "__main__":
    main()

