import time
from datetime import timedelta, datetime

import requests
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import json


from coin import getHistory


def getBTC():
    df = yf.download('BTC-USD', start='2022-04-01', end='2022-04-27', interval='1d')

    df['MA10'] = df['Close'].rolling(window=10).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()

    plt.plot(df.index, df['Close'], label='Price')
    plt.plot(df.index, df['MA10'], label='MA10')
    plt.plot(df.index, df['MA50'], label='MA50')
    plt.legend()
    plt.show()

def patternRecognition():
    result = getHistory("BTC-USDT", "60", 1674827332000, int(time.time() * 1000))
    json_object = json.loads(result)
    mlist = list(json_object["data"]["klines"])
    times = []
    prices = []
    for item in mlist:
        times.append(item["time"])
        prices.append(item["close"])
    df = pd.DataFrame()
    df['date'] = times
    df['close'] = prices
    # Read the data from a CSV file
    # df = pd.read_csv('crypto_data.csv')

    # # Convert the date column to a datetime object
    df['date'] = pd.to_datetime(df['date'])
    #
    # Set the date column as the DataFrame index
    df.set_index('date', inplace=True)

    # Resample the data to hourly intervals
    # df_hourly = df.resample('H').mean()

    # Calculate the hourly moving averages
    hourly_ma = df['close'].rolling(window=24).mean()
    print(hourly_ma)

    # Identify patterns using Z-score
    df['z_score'] = (df['close'] - hourly_ma) / df['close'].rolling(window=24).std()
    print( df['z_score'])
    #
    # Plot the hourly data, moving averages, and Z-score
    plt.plot(df.index, df['close'], label='Hourly Data')
    plt.plot(hourly_ma.index, hourly_ma, label='Hourly Moving Average')
    plt.plot(df.index, df['z_score'], label='Z-Score')
    plt.legend()
    plt.show()
def newRecognition():

    # Set the API endpoint and parameters
    endpoint = 'https://api.binance.com/api/v3/klines'
    symbol = 'BTCUSDT'
    interval = '1h'
    startTime = int((datetime.now() - timedelta(days=50)).timestamp() * 1000)
    endTime = int(datetime.now().timestamp() * 1000)

    # Call the API and parse the data into a DataFrame
    params = {'symbol': symbol, 'interval': interval, 'startTime': startTime, 'endTime': endTime}
    response = requests.get(endpoint, params=params)
    data = response.json()
    print(data)
    df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                     'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                     'taker_buy_quote_asset_volume', 'ignore'])
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    df.set_index('date', inplace=True)

    # Resample the data to hourly intervals
    df_hourly = df.resample('H').mean()

    # Calculate the hourly moving averages
    hourly_ma = df_hourly['close'].rolling(window=24).mean()

    # Identify patterns using Z-score
    df_hourly['z_score'] = (df_hourly['close'] - hourly_ma) / df_hourly['close'].rolling(window=24).std()

    # Plot the hourly data, moving averages, and Z-score

    plt.plot(df_hourly.index, df_hourly['close'], label='Hourly Data')
    plt.plot(hourly_ma.index, hourly_ma, label='Hourly Moving Average')
    plt.plot(df_hourly.index, df_hourly['z_score'], label='Z-Score')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    newRecognition()


