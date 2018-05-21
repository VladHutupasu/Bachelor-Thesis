import datetime
import time
from datetime import datetime, timedelta
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import Sequential

class MLBot():
    def __init__(self, name):
        self.name = name


    def predict_coin_price(self, coin):
        #for now we will focus on bit coin and ethereum
        name = ""
        if coin.upper() == 'BTC':
            name = "bitcoin"
        else:
            name = "ethereum"

        b_market = pd.read_html("https://coinmarketcap.com/currencies/{}/historical-data/?start=20130428&end=".format(name) + time.strftime("%Y%m%d"))[0]

        #Convert to a better date format.
        b_market = b_market.assign(Date=pd.to_datetime(b_market['Date']))

        if coin == "BTC":
            b_market.loc[b_market['Volume'] == "-", 'Volume']=0
        # convert to int
        b_market['Volume'] = b_market['Volume'].astype('int64')

        #use the close price instead
        b_market = b_market[['Date','Close']]

        start_date = '2017-01-01'
        split_date = '2018-01-01'
        #split_date = datetime.today() - timedelta(days=1)
        training_set = b_market[b_market['Date'] >= start_date]
        training_set = training_set[training_set['Date']<= split_date]

        test_set = b_market[b_market['Date'] >= split_date]

        #close price
        training_set = training_set.iloc[:,1:2]

        #Convert to a 2D array
        training_set = training_set.values

        # Feature Scaling
        from sklearn.preprocessing import MinMaxScaler
        sc = MinMaxScaler()
        training_set = sc.fit_transform(training_set)

        #Get the inputs and the outputs
        n = training_set.shape[0]
        X_train = training_set[0:n]
        Y_train = training_set[0:n+1]

        today = pd.DataFrame(X_train[0:5])
        tomorrow = pd.DataFrame(Y_train[0:])
        ex = pd.concat([today, tomorrow], axis=1)
        ex.columns = (['today', 'tomorrow'])

        #Now reshape the X training data set into the shape to pass into Keras
        X_train = np.reshape(X_train, (n, 1, 1))

        #Initialize the RNN (Recurrent Neural Network
        rnn = Sequential()

        #Use the input layer with the sigmoid activation function
        rnn.add(LSTM(units=4, activation='sigmoid', input_shape=(None, 1)))

        #Add the output layer which will give us tomorrow's prediction
        rnn.add(Dense(units=1))

        #Compile the rnn
        rnn.compile(optimizer='adam',loss='mean_squared_error')

        #Fit the RNN to the training set loaded earlier
        rnn.fit(X_train, Y_train, batch_size=64, epochs=3)

        #Now make a prediction
        real_price = test_set.iloc[:,1:2]
        print(real_price.tail())

        #Convert to a 2D array
        real_price = real_price.values
        # Getting the predicted stock price of 2017
        inputs = real_price
        inputs = sc.transform(inputs)
        tn = test_set.shape[0]
        inputs = np.reshape(inputs, (tn, 1, 1))
        predicted_stock_price = rnn.predict(inputs)
        predicted_stock_price = sc.inverse_transform(predicted_stock_price)

        #Getting the real price of
        real_stock_price_train = test_set
        real_stock_price_train = real_stock_price_train.iloc[:,1:2].values

        print(real_stock_price_train)

        # Getting the predicted stock price of 2012 - 2016
        predicted_stock_price_train = rnn.predict(X_train)
        predicted_stock_price_train = sc.inverse_transform(predicted_stock_price_train)

        print(predicted_stock_price_train)

        print("Predicted stock price")
        print(predicted_stock_price)

        d = {'TPrice':predicted_stock_price[0]}
        data = pd.DataFrame(data=d)

        return data