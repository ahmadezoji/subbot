import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import json
from sklearn.model_selection import train_test_split
import time
from coin import getHistory
import csv

# Define your neural network model
class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.fc1 = nn.Linear(10, 5)
        self.fc2 = nn.Linear(5, 1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        return x

def loadData():
    result  = getHistory("BTC-USDT","60",1679244507000,int(time.time() * 1000))
    json_object = json.loads(result)
    mlist = list(json_object["data"]["klines"])
    header = ['Date','Time','Open','High','Low','Close', 'Volume']
    with open('crypto_prices.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    for item in mlist:
        data = [item["statDate"],item["time"],item["open"],item["high"],item["low"],item["close"], item["volume"]]
        with open('crypto_prices.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(data)

loadData()
# Load and preprocess data
data = pd.read_csv('crypto_prices.csv')
# preprocess data ...

# Split data into training and testing sets
train_data, test_data = train_test_split(data, test_size=0.2)

# Define transformer model
class CryptoPriceTransformer(nn.Module):
    def __init__(self):
        super(CryptoPriceTransformer, self).__init__()
        # define transformer layers ...

    def forward(self, x):
        # pass input through transformer layers and output prediction
        return prediction

# Train the model
# model = CryptoPriceTransformer()
# criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(model.parameters(), lr=0.001)
# Create an instance of your model
model = MyModel()

# Define your loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Generate some dummy input data and targets
x = torch.randn(32, 10)
y = torch.randn(32, 1)

# Forward pass
output = model(x)
loss = criterion(output, y)

# Backward pass and optimizer step
optimizer.zero_grad()
loss.backward()
optimizer.step()
# for item in test_data:
print(test_data)
# for epoch in range(100):
#     for data, target in train_data:
#         print(data)
        # optimizer.zero_grad()
        # output = model(data)
        # loss = criterion(output, target)
        # loss.backward()
        # optimizer.step()
#
# # Evaluate the model
# with torch.no_grad():
#     correct = 0
#     total = 0
#     for data, target in test_data:
#         output = model(data)
#         prediction = torch.argmax(output)
#         if prediction == target:
#             correct += 1
#         total += 1
#     accuracy = correct / total
#
# # Make predictions
# new_data = pd.read_csv('new_crypto_prices.csv')
# # preprocess new data ...
# with torch.no_grad():
#     for data in new_data:
#         output = model(data)
#         prediction = torch.argmax(output)
#         if prediction == 0:
#             print('Price will go down')
#         else:
#             print('Price will go up')