import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.layers import Input, Dense, Dropout, MultiHeadAttention, LayerNormalization
import tensorflow as tf


# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Dropout, TransformerBlock, MultiHeadAttention, TimeDistributed, LayerNormalization
# from tensorflow.keras.optimizers import Adam
# from tensorflow.keras.losses import MeanSquaredError
# from tensorflow.keras.callbacks import EarlyStopping
# from keras.optimizers import Adam
# from keras.losses import MeanSquaredError
# from keras.callbacks import EarlyStopping

# import transformers


from coin import getHistory
import time
import json
import csv

def loadData():
    result  = getHistory("BTC-USDT","60",1679244507000,int(time.time() * 1000))
    json_object = json.loads(result)
    mlist = list(json_object["data"]["klines"])
    header = ['Timestamp','Open','High','Low','Close', 'Volume']
    with open('bitstampUSDT.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    for item in mlist:
        data = [item["time"],item["open"],item["high"],item["low"],item["close"], item["volume"]]
        with open('bitstampUSDT.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(data)
def create_sequences(data, window_size):
    X = []
    y = []
    for i in range(len(data)-window_size-1):
        X.append(data[i:i+window_size,:])
        y.append(data[i+window_size,:])
    return np.array(X), np.array(y)


loadData()
df = pd.read_csv('bitstampUSDT.csv')
df = df.dropna()
# pd.to_datetime(date_col_to_force, errors = 'coerce')


df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
df = df.set_index('Timestamp')
df = df.resample('H').mean()
df = df.dropna()
scaler = MinMaxScaler()
data = scaler.fit_transform(df)

train_size = int(len(data) * 0.8)
test_size = len(data) - train_size
train_data, test_data = data[0:train_size,:], data[train_size:len(data),:]


window_size = 24
X_train, y_train = create_sequences(train_data, window_size)
X_test, y_test = create_sequences(test_data, window_size)


# model = Sequential([
#     TransformerBlock(
#         num_heads=8,
#         key_dim=2,
#         attention_dropout=0.3,
#         output_dropout=0.3,
#         use_masking=True,
#         ),
#     Dense(32, activation='relu'),
#     Dropout(0.3),
#     Dense(1)
# ])
def create_model(sequence_length, n_features):
    # Define input layer
    inputs = Input(shape=(sequence_length, n_features))

    # Add transformer blocks
    x = inputs
    for i in range(3):
        # Multi-head attention layer
        x = MultiHeadAttention(num_heads=8, key_dim=32)(x, x)
        # Add & Norm
        x = LayerNormalization(epsilon=1e-6)(x)
        # Feed-forward layer
        x = Dense(units=256, activation='relu')(x)
        # Dropout
        x = Dropout(0.1)(x)

    # Flatten output
    x = Dense(units=1, activation='linear')(x)
    model = tf.keras.models.Model(inputs=inputs, outputs=x)

    # Compile model
    model.compile(loss='mean_squared_error', optimizer=tf.keras.optimizers.Adam(lr=1e-4))

    return model

model = create_model(sequence_length=60, n_features=1)

# Reshape input data to have 60 time steps and 1 feature
X_test_reshaped = np.reshape(X_test, (X_test.shape[0], 60, 1))

# Make predictions on reshaped input data
y_pred = model.predict(X_test_reshaped)

# y_pred = model.predict(X_test)
y_test_inv = scaler.inverse_transform(y_test)
y_pred_inv = scaler.inverse_transform(y_pred)
rmse = np.sqrt(MeanSquaredError()(y_test_inv, y_pred_inv).numpy())
print('RMSE:', rmse)

fig, ax = plt.subplots(figsize=(12,6))
ax.plot(y_test_inv, label='Actual')
ax.plot(y_pred_inv, label='Predicted')
ax.set_title('Bitcoin Price Forecasting')
ax.set_xlabel('Time')
ax.set_ylabel('Price')
ax.legend()
plt.show()