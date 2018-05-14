import pandas as pd
import time
import csv
import numpy as np

# --Get market info for bitcoin from the start of April, 2013 to the current day
bitcoin_market_info = pd.read_html(
    "https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end=" + time.strftime("%Y%m%d"))[0]
bitcoin_market_info = bitcoin_market_info.assign(Date=pd.to_datetime(bitcoin_market_info['Date']))
bitcoin_market_info.loc[bitcoin_market_info['Volume'] == "-", 'Volume'] = 0
bitcoin_market_info['Volume'] = bitcoin_market_info['Volume'].astype('int64')

market_info = bitcoin_market_info

#--DATA only for 2017--
# market_info = market_info[market_info['Date'] >= '2017-01-01']
market_info = market_info[market_info['Date'] >= '2018-01-01']

#--Create Day Diff column with values--
kwargs = {'Day Diff': lambda x: (x['Open'] - x['Close']) / x['Open'] *10000}
market_info = market_info.assign(**kwargs)


# --Create Close Off High and Volatility column--
# Close_Off_High represents the gap between the closing price and price high for that day, where values
# of -1 and 1 mean the closing price was equal to the daily HIGH or daily LOW, respectively
# Volatility column is simply the difference between high and low price divided by the opening price
kwargs = {'Close Off High': lambda x: ((2 * (x['High'] - x['Close'])) / (x['High'] - x['Low']) -1) *10000,
          'Volatility': lambda x: (x['High'] - x['Low']) / (x['Open'])}
market_info = market_info.assign(**kwargs)


#add Movement column (initially random values)
market_info = market_info.assign(Movement=pd.Series(np.random.randn(len(market_info['Open']))).values)

#reverse array for ascending order
market_info = market_info.sort_values(by='Date')

# Resetting the indexes
market_info = market_info.reset_index(drop=True)

#Replacing Movement random values wuth actual values -> UP or DOWN
i=0
while i <(len(market_info)-1):   # -1 because we cannot compare the last day with the next one

    market_info['Movement'][i] = market_info['Close'][i] - market_info['Close'][i+1]
    x = market_info['Movement'][i]
    if (x>0):
        market_info['Movement'][i] = 'Down'
    elif (x<0):
        market_info['Movement'][i] = 'Up'
    i=i+1

print(market_info)

# drop rest keep only Close,Volume,COH & Vola
# model_data = market_info[['Date'] + [metric for metric in ['Volume', 'Close Off High', 'Day Diff', 'Volatility', 'Movement']]]
model_data = market_info[['Date', 'Close', 'Volume', 'Close Off High', 'Day Diff', 'Volatility', 'Movement']]


#Dropping the last row that doesnt have movement
model_data = model_data.drop(model_data.index[len(model_data)-1])
print(model_data)


with open('2018_test_data.csv', 'w') as csvfile:
    fieldnames = ['Date', 'Close', 'Volume', 'Close Off High', 'Day Diff', 'Volatility', 'Movement']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    i=0
    while i < (len(market_info) - 1):

        writer.writerow({'Date': model_data['Date'][i], 'Close': model_data['Close'][i], 'Volume': model_data['Volume'][i],
                         'Close Off High': model_data['Close Off High'][i], 'Day Diff': model_data['Day Diff'][i],
                         'Volatility': model_data['Volatility'][i], 'Movement': model_data['Movement'][i]})
        i=i+1