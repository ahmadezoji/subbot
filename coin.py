import requests
import pandas as pd
import time

# Replace YOUR_API_KEY with your actual API key
API_KEY = 'iTV2lq2325eSpTHO'

# Define a list of your favorite cryptocurrencies
coins = ['BTC', 'ETH', 'XRP']

# Define a function to get the price data for a given coin
def get_price_data(coin):
    url = f'https://api.coinbase.com/v2/prices/{coin}-USD/spot'
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(url, headers=headers)
    data = response.json()['data']
    return {'time': data['time'], 'price': data['amount']}

# Define a function to get the price data for all coins
def get_all_price_data():
    data = {}
    for coin in coins:
        price_data = get_price_data(coin)
        data[coin] = price_data['price']
    return data

# Define a function to calculate the percentage change in price for each coin
def calculate_percentage_changes(data):
    df = pd.DataFrame.from_dict(data, orient='index', columns=['price'])
    df['pct_change'] = df['price'].pct_change() * 100
    return df

# Define a function to display the price data and percentage changes
def display_data(df):
    print(df)

# Run the main loop to get and display the price data every minute
while True:
    price_data = get_all_price_data()
    df = calculate_percentage_changes(price_data)
    display_data(df)
    time.sleep(60)
