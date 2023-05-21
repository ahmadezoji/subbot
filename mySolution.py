import json
import time
from datetime import datetime

from coin import getHistory
import csv
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def loadData():
    result  = getHistory("BTC-USDT","5",1678876783000,int(time.time() * 1000))
    json_object = json.loads(result)
    mlist = list(json_object["data"]["klines"])
    header = ['Timestamp','Open','High','Low','Close', 'Volume']
    with open('tempdata.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    for item in mlist:
        data = [item["time"],item["open"],item["high"],item["low"],item["close"], item["volume"]]
        with open('tempdata.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(data)
def prediction():
    # This code will load the data from the provided API, convert the timestamp column to a datetime index,
    # and calculate the percentage change in price. It will then create a new dataframe for training the linear
    # regression model, fit the model to the data, and predict the next 15 minutes' closing price.

    # Finally, the code will create a plot of the historical data and the predicted price for the next 15 minutes
    # using the pyplot module from matplotlib. Please note that the predicted prices are just estimates, and the actual price may differ significantly.

    loadData()
    # Load data from API
    data = pd.read_csv('realdata.csv')

    # Convert Timestamp column to datetime and set it as the index
    data['Timestamp'] = pd.to_datetime(data['Timestamp'],unit='ms')
    data.set_index('Timestamp', inplace=True)

    # Create a new column for the closing price
    data['Price'] = data['Close']
    # Calculate the percentage change in price
    data['Returns'] = data['Price'].pct_change()

    # Create a new dataframe for training the model
    df = pd.DataFrame({'x': np.arange(len(data)), 'y': data['Price']})

    # Fit a linear regression model to the data
    model = LinearRegression().fit(df[['x']], df['y'])

    # Predict the next 15 minutes' closing price
    next_price = model.predict([[len(data) + 1], [len(data) + 2], [len(data) + 3], [len(data) + 4], [len(data) + 5]])

    # Create a plot of the historical data and the predicted price
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=data, x=data.index, y='Price')
    sns.lineplot(
        x=[data.index[-1], data.index[-1] + pd.Timedelta(minutes=15), data.index[-1] + pd.Timedelta(minutes=30),
           data.index[-1] + pd.Timedelta(minutes=45), data.index[-1] + pd.Timedelta(minutes=60)], y=next_price)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.show()

def slope_detection():
    # # Sample Bitcoin price data (date and price)
    # bitcoin_data = {
    #     'date': ['2023-05-01', '2023-05-02', '2023-05-03', '2023-05-04', '2023-05-05'],
    #     'price': [40000, 41000, 38000, 39000, 42000]
    # }
    #
    # # Create a pandas DataFrame from the Bitcoin data
    # df = pd.DataFrame(bitcoin_data)
    loadData()
    # Load the CSV data
    df = pd.read_csv('tempdata.csv')
    # Convert the 'date' column to a datetime type
    df['date'] = pd.to_datetime(df['Timestamp'], unit='ms')

    # Sort the DataFrame by date in ascending order
    df.sort_values(by='date', inplace=True)

    # Add a new column for slope
    df['slope'] = df['Close'].diff(5)

    # Calculate the percentage change
    df['percentage_change'] = df['slope'] / df['Close'] * 100

    # Check if slope is positive (increase) or negative (decrease)
    df['slope_direction'] = df['slope'].apply(lambda x: 'Increase' if x > 0 else 'Decrease')

    # plt.plot(df['date'],df['percentage_change'])
    # plt.show()
    # Print the DataFrame with slope and percentage change information
    # print(df['percentage_change'] > 5)
    df2 = df[df['percentage_change'] > 1]
    df2['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
    print(df2)

slope_detection()