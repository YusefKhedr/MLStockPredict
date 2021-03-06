# -*- coding: utf-8 -*-
"""MLStockPredict"""

#Description: First ML Program!, Using artificial reccurent NN called Long Short Term Memory (LSTM)
#             To predict the closing stock price of corporation (Apple) using the past 60 day stock price.

import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential 
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Get the stock quote DF
df = web.DataReader('AMD', data_source='yahoo', start='2012-01-01', end='2020-09-02')
#Show Data
df

#Get Rows and Columns
df.shape

#Visualization
plt.figure(figsize=(16,8))
plt.title('Close Price History')
plt.plot(df['Close'])
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price USD($)', fontsize=18)
plt.show

#Create a DF with only "Close Column"
data = df.filter(['Close'])
#Convert the DF to a numpy array
dataset = data.values
#Get Number of Rows to train model
training_data_len = math.ceil(len(dataset) * .8)
training_data_len

#Scale data
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)
scaled_data

#Create the training data set
#create the scaled training data set
train_data = scaled_data[0:training_data_len, :]
#split the data into x_train and y_train data sets
x_train = []
y_train = []

for i in range(60, len(train_data)):
  x_train.append(train_data[i-60:i, 0])
  y_train.append(train_data[i, 0])
  if i<= 61:
    print(x_train)
    print(y_train)
    print()

#Convert x_train and Y_train to numpy arrays in order to use them to train 
x_train, y_train = np.array(x_train), np.array(y_train)

#Reshape the x_train data set for LSTM as we need it to be 3 dimensional 
x_train = np.reshape(x_train,(x_train.shape[0], x_train.shape[1], 1))
x_train.shape

#Build LSTM model
model = Sequential()
model.add(LSTM(50, return_sequences=True,input_shape=(x_train.shape[1],1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

#Compile the Model
model.compile(optimizer= 'adam', loss='mean_squared_error')

#Training!!
model.fit(x_train, y_train, batch_size = 1, epochs=1)

#Create Testing data set
#create new array with scalled values from index 1543 to 2003
test_data = scaled_data[training_data_len - 60:, :]
#Create data sets x_test and y_test
x_test = []
y_test = dataset[training_data_len:,:]
for i in range(60 ,len(test_data)):
  x_test.append(test_data[i-60:i,0])

#Convert the data to a numpy array
x_test = np.array(x_test)

#Reshaping the data
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

#Get the models predicted Price values
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

#Test the model using Root Mean Squared Error (RMSE)
rmse = np.sqrt(np.mean(predictions-y_test)**2)
rmse

#Plot the data
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions
#Visualization
plt.figure(figsize =(16,8))
plt.title('Model')
plt.xlabel('Date')
plt.ylabel('Close Price USD ($)')
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train', 'Val', 'Predictions'],loc ='lower right')
plt.show()

#Show Valid price and predicted prices
valid

#Get the quote
AMD_quote = web.DataReader('AMD', data_source='yahoo', start='2012-01-01', end='2020-09-01')
#Create new DF
new_df = AMD_quote.filter(['Close'])
#get the last 60 day closing price values and convert the DF to an array
last_60_days = new_df[-60:].values
#Scale to be between 0 and 1 
last_60_days_scaled = scaler.transform(last_60_days)
#Create Empty list 
X_test = []
#Append the past 60 days into x_test
X_test.append(last_60_days_scaled)
#Convert X_test to a np array
X_test = np.array(X_test)
#Reshape for the model
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
#Get Predicted Scaled Price
pred_price = model.predict(X_test)
#undo the scaling
pred_price = scaler.inverse_transform(pred_price)
print(pred_price)

AMD_quote2 = web.DataReader('AMD', data_source='yahoo', start= '2020-09-02', end= '2020-09-02')
print(AMD_quote2['Close'])
