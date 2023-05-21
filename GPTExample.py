import pandas as pd
import numpy as np
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Dropout, TextVectorization
from keras.models.cloning import Sequential
from keras.optimizers.adam import Adam
from keras.losses import BinaryCrossentropy
from keras.metrics import BinaryAccuracy
from keras.callbacks import EarlyStopping

# from matplotlib.pyplot import plot
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
import tensorflow as tf

import pandas as pd
import numpy as np
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score

import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder

import matplotlib.pyplot as plt

from coin import getHistory
import time
import json
import csv

def loadData():
    result  = getHistory("BTC-USDT","60",1671100783000,int(time.time() * 1000))
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
    loadData()
    # Load the CSV data
    data = pd.read_csv('tempdata.csv')

    # Preprocess the data
    X = data[['Open', 'High', 'Low', 'Close', 'Volume']].values
    y = data['Close'].values

    # Scale the data
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    y_scaled = scaler.fit_transform(y.reshape(-1, 1))

    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, shuffle=False)

    # Build the model
    model = Sequential([
        Dense(128, activation='relu', input_shape=(5,)),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(1)
    ])

    model.compile(loss='mean_squared_error', optimizer=Adam())

    # Train the model
    early_stopping = EarlyStopping(patience=10, restore_best_weights=True)
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, callbacks=[early_stopping])

    # Make predictions
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions)

    # Calculate the movement direction
    y_test_direction = np.sign(np.diff(y_test.flatten()))
    predicted_direction = np.sign(np.diff(predictions.flatten()))

    print(predicted_direction)

    # Plot the predicted prices///
    plt.figure(figsize=(10, 6))
    # plt.plot(range(len(predictions)), y_test[:-1], label='Actual Price')
    plt.plot(range(1, len(predictions) + 1), predictions, label='Predicted Price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('BTC_USDT Price Prediction')
    plt.legend()
    plt.show()

    # print('Accuracy of movement direction prediction:', accuracy)



def prediction_movment():

    loadData()
    # Load the data from the CSV file
    data = pd.read_csv('tempdata.csv')
    try:

        # Preprocess the data
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])
        data.set_index('Timestamp', inplace=True)
        data.sort_index(inplace=True)

        # Calculate the increase/decrease ratio
        data['Increase_Ratio'] = (data['Close'] - data['Open']) / data['Open']
        data['Movement_Direction'] = np.where(data['Increase_Ratio'] > 0, 'Increase', 'Decrease')

        # Prepare the data for training
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(data[['Open', 'High', 'Low', 'Close', 'Volume', 'Increase_Ratio']])

        X = []
        y = []

        # Sliding window approach to create input sequences
        window_size = 24
        for i in range(window_size, len(data)):
            X.append(scaled_data[i - window_size:i])
            y.append(data['Movement_Direction'].iloc[i])

        X = np.array(X)
        y = np.array(y)

        # Reshape the target labels
        y = np.reshape(y, (-1, 1))

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

        # Encode the target labels
        label_encoder = LabelEncoder()
        y_train_encoded = label_encoder.fit_transform(y_train.flatten())
        y_test_encoded = label_encoder.transform(y_test.flatten())

        # Build the transformer-based model
        model = Sequential([
            Dense(128, activation='relu', input_shape=(window_size, 6)),
            Dropout(0.2),
            Dense(64, activation='relu'),
            Dropout(0.2),
            Dense(1, activation='sigmoid')
        ])

        # Compile and train the model
        model.compile(optimizer=Adam(), loss=BinaryCrossentropy(), metrics=[BinaryAccuracy()])
        early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        model.fit(X_train, y_train_encoded, epochs=100, batch_size=32, validation_split=0.2, callbacks=[early_stopping])

        # Evaluate the model
        _, accuracy = model.evaluate(X_test, y_test_encoded)
        print(f'Test accuracy: {accuracy}')

        # Make predictions
        predictions = model.predict(X_test)
        predicted_labels = label_encoder.inverse_transform((predictions > 0.5).astype(int).flatten())

        # Plot the predicted movement direction
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(data.index[window_size + len(X_train):window_size + len(data) - len(X_test)], y_test.flatten(),
                label='Testing Labels')
        ax.plot(data.index[window_size + len(X_train):window_size + len(data) - len(X_test)], predicted_labels,
                label='Predicted Labels')
        plt.xticks(rotation=45)
        plt.xlabel('Timestamp')
        plt.ylabel('Movement Direction')
        plt.legend()
        plt.show()
    except NameError:
        print("Variable x is not defined")

prediction_movment()