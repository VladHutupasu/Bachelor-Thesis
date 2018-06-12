import statsmodels.api as sm
import plotly.graph_objs as go
import plotly.offline as py
import numpy as np
import pandas as pd
import time
from matplotlib import pyplot as plt

# import numpy as np
# import pandas as pd
# import statsmodels.api as sm
# from scipy import stats
# from sklearn.metrics import mean_squared_error
# from math import sqrt
# from random import randint
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
# from keras.layers import GRU
from keras.callbacks import EarlyStopping
# from keras import initializers
# from matplotlib import pyplot
# from datetime import datetime
# from matplotlib import pyplot as plt
# import plotly.offline as py
# import plotly.graph_objs as go


def seasonal_decomposition():
    s = sm.tsa.seasonal_decompose(model_data['Close**'], freq=10)

    trace1 = go.Scatter(x=np.arange(0, len(s.trend), 1), y=s.trend, mode='lines', name='Trend',
                        line=dict(color=('rgb(244, 146, 65)'), width=4))

    trace2 = go.Scatter(x=np.arange(0, len(s.seasonal), 1), y=s.seasonal, mode='lines', name='Seasonal',
                        line=dict(color=('rgb(66, 244, 155)'), width=2))

    trace3 = go.Scatter(x=np.arange(0, len(s.resid), 1), y=s.resid, mode='lines', name='Residual',
                        line=dict(color=('rgb(209, 244, 66)'), width=2))

    trace4 = go.Scatter(x=np.arange(0, len(s.observed), 1), y=s.observed, mode='lines', name='Observed',
                        line=dict(color=('rgb(66, 134, 244)'), width=2))

    data = [trace1, trace2, trace3, trace4]
    layout = dict(title='Seasonal decomposition 02 May-02 June 2018', xaxis=dict(title='Time'),
                  yaxis=dict(title='Price, USD'))
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='seasonal_decomposition.html')


bitcoin_market_info = pd.read_html(
    "https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end=" + time.strftime("%Y%m%d"))[0]
bitcoin_market_info = bitcoin_market_info.assign(Date=pd.to_datetime(bitcoin_market_info['Date']))
bitcoin_market_info.loc[bitcoin_market_info['Volume'] == "-", 'Volume'] = 0
bitcoin_market_info['Volume'] = bitcoin_market_info['Volume'].astype('int64')

market_info = bitcoin_market_info

#--DATA only for 2017--
# market_info = market_info[market_info['Date'] >= '2017-01-01']
market_info = market_info[market_info['Date'] >= '2017-01-01']
market_info = market_info[market_info['Date'] <= '2017-12-31']

#--Create Day Diff column with values--
kwargs = {'Day Diff': lambda x: (x['Open*'] - x['Close**']) / x['Open*'] *10000}
market_info = market_info.assign(**kwargs)


# --Create Close Off High and Volatility column--
# Close_Off_High represents the gap between the closing price and price high for that day, where values
# of -1 and 1 mean the closing price was equal to the daily HIGH or daily LOW, respectively
# Volatility column is simply the difference between high and low price divided by the opening price
kwargs = {'Close Off High': lambda x: ((2 * (x['High'] - x['Close**'])) / (x['High'] - x['Low']) -1) *10000,
          'Volatility': lambda x: (x['High'] - x['Low']) / (x['Open*'])}
market_info = market_info.assign(**kwargs)


#add Movement column (initially random values)
market_info = market_info.assign(Movement=pd.Series(np.random.randn(len(market_info['Open*']))).values)

#reverse array for ascending order
market_info = market_info.sort_values(by='Date')

# Resetting the indexes
market_info = market_info.reset_index(drop=True)

#Replacing Movement random values wuth actual values -> UP or DOWN
i=0
while i <(len(market_info)-1):   # -1 because we cannot compare the last day with the next one

    market_info['Movement'][i] = market_info['Close**'][i] - market_info['Close**'][i+1]
    x = market_info['Movement'][i]
    if (x>0):
        market_info['Movement'][i] = 'Down'
    elif (x<0):
        market_info['Movement'][i] = 'Up'
    i=i+1

#Dropping the last row that doesnt have movement
model_data = market_info.drop(market_info.index[len(market_info)-1])
print('Size data -> '+str(len(model_data)))

# -------------------------------Seasonal decompose-------------------------------------
# seasonal_decomposition()

# -------------------------------Seasonal decompose-------------------------------------
# plt.figure(figsize=(15,7))
# ax = plt.subplot(211)
# sm.graphics.tsa.plot_acf(model_data['Close**'].squeeze(), lags=363, ax=ax)
# ax = plt.subplot(212)
# sm.graphics.tsa.plot_pacf(model_data['Close**'].squeeze(), lags=363, ax=ax)
# plt.tight_layout()
# plt.show()
# -----------------------------------------------------------------------------------------

train_data = model_data[:300]
test_data = model_data[300:]
print('Size TRAIN -> '+str(len(train_data)))
print('Size TEST -> '+str(len(test_data)))
print('Size ????????????????? -> '+str(len(test_data)))


# initialize sequential model, add 2 stacked LSTM layers and densely connected output neuron
model = Sequential()
model.add(LSTM(256, return_sequences=True, input_shape=train_data['Close**']))
model.add(LSTM(256))
model.add(Dense(1))

# compile and fit the model
model.compile(loss='mean_squared_error', optimizer='adam')
history = model.fit(train_data['Close**'], train_data['Movement'], epochs=100, batch_size=16, shuffle=False,
                    validation_data=(test_data['Close**'], test_data['Movement']),
callbacks = [EarlyStopping(monitor='val_loss', min_delta=5e-5, patience=20, verbose=1)])