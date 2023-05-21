import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import tensorflow_addons as tfa


from coin import getHistory
import time
import json
import csv

def loadData():
    result  = getHistory("RNDR-USDT","60",1682899202000,int(time.time() * 1000))
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
def create_sequences(data, seq_length):
    X = []
    y = []

    for i in range(len(data)-seq_length-1):
        X.append(data[i:(i+seq_length)])
        y.append(data[i+seq_length])

    return np.array(X), np.array(y)

loadData()
# Load data from CSV file
df = pd.read_csv('tempdata.csv')

# Choose relevant columns
df = df[['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']]

# Convert Timestamp column to datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'],unit='ms')


# Set Timestamp column as index
df.set_index('Timestamp', inplace=True)

# Calculate mid-price as the average of the high and low prices
df['MidPrice'] = (df['High'] + df['Low']) / 2
# Define function to create input sequences and labels for training

# Choose number of time steps for input sequence
seq_length = 60

# Normalize data using MinMaxScaler
scaler = MinMaxScaler()
data = scaler.fit_transform(df['MidPrice'].values.reshape(-1, 1))

# Create input sequences and labels
X, y = create_sequences(data, seq_length)

# Split data into training and testing sets
train_size = int(len(X) * 0.8)
X_train, y_train = X[:train_size], y[:train_size]
X_test, y_test = X[train_size:], y[train_size:]

# Build transformer model
# keras.layers.Transformer(num_layers=2, d_model=512, num_heads=8,
#                             activation='relu', dropout=0.1),
# tf.keras.layers.DenseWithMultiheadAttention(512, num_heads=8, activation='relu', dropout=0.1),
# model = keras.models.Sequential([
#     tf.keras.layers.MultiHeadAttention(num_heads=8, key_dim=512),
#     tf.keras.layers.DenseWithMultiheadAttention(512, num_heads=8, activation='relu', dropout=0.1)
# ])
# model = tf.keras.models.Sequential([
#     tf.keras.layers.MultiHeadAttention(num_heads=8, key_dim=512),
#     tf.keras.layers.Dense(512, activation='relu'),
#     tf.keras.layers.Dropout(0.1),
#     tf.keras.layers.Dense(1)
# ])
model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(units=64, input_shape=(60, 1)),
    tf.keras.layers.Dense(1)
])
# Compile model
model.compile(optimizer='adam', loss='mse')

# Train model
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Evaluate model
model.evaluate(X_test, y_test)

# Make predictions on test set
y_pred = model.predict(X_test)

# Rescale predictions and labels
y_pred = scaler.inverse_transform(y_pred)
y_test = scaler.inverse_transform(y_test)
# print(y_pred)

# Calculate direction of next time frame based on predicted and actual mid-prices
direction_pred = np.sign(y_pred[-1] - y_pred[-2])
direction_actual = np.sign(y_test[-1] - y_test[-2])

# Plot actual and predicted mid-prices
plt.plot(y_test, label='Actual')
plt.plot(y_pred, label='Predicted')
plt.legend()
plt.show()

# Print predicted and actual directions
print('Predicted direction:', direction_pred)
print('Actual direction:', direction_actual)
# This code adds a plot of the actual and predicted mid-prices using matplotlib.pyplot, an


#predict next period
# # Get the last lookback time steps of the test set
# lookback = 60
# num_features = 1
# last_sequence = X_test[-lookback:]
#
# # Create a new input sequence that includes the last lookback time steps
# # and the next hour (i.e., 60 minutes)
# next_sequence = np.append(last_sequence[:, 1:], [[0] * (num_features-1) + [1]], axis=0)
#
# # Reshape the input sequence to match the model's input shape
# next_sequence = next_sequence.reshape(1, lookback, num_features)
#
# # Make the prediction for the next hour
# y_next = model.predict(next_sequence)
#
# # Rescale the prediction
# y_next = scaler.inverse_transform(y_next)
#
# # Print the predicted value
# print("Predicted value for the next hour: ", y_next[0][0])