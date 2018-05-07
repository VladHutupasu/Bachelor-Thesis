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
# print(bitcoin_market_info)


# --Create Day Diff column with values--
market_info = bitcoin_market_info
market_info = market_info[market_info['Date'] >= '2017-01-01']
market_info = market_info[market_info['Date'] < '2018-01-01']
kwargs = {'Day Diff': lambda x: (x['Open'] - x['Close']) / x['Open'] *10000}
market_info = market_info.assign(**kwargs)


# --Create Close Off High and Volatility column--
# Close_Off_High represents the gap between the closing price and price high for that day, where values
# of -1 and 1 mean the closing price was equal to the daily HIGH or daily LOW, respectively
# Volatility column is simply the difference between high and low price divided by the opening price

kwargs = {'Close Off High': lambda x: ((2 * (x['High'] - x['Close'])) / (x['High'] - x['Low']) -1) *10000,
          'Volatility': lambda x: (x['High'] - x['Low']) / (x['Open'])}
market_info = market_info.assign(**kwargs)
# print(market_info)

#add Movement column
# kwargs = {'Movement': lambda x: (x['Open'] - x['Close'])}
# market_info = market_info.assign(**kwargs)

# market_info['Movement Up/Down'] = Series(np.random.randn(len(market_info['Open'])), index=market_info.index)
market_info = market_info.assign(Movement=pd.Series(np.random.randn(len(market_info['Open']))).values)
print(market_info)


i=120
#Replacing Movement values wuth actual name UP or DOWN
while i <(len(market_info)-1):   # -1 because we cannot compare the last day with the next one

    market_info['Movement'][i] = market_info['Close'][i] - market_info['Close'][i+1]
    x = market_info['Movement'][i]
    if (x>0):
        market_info['Movement'][i] = 'Down'
    elif (x<0):
        market_info['Movement'][i] = 'Up'
    i=i+1

# print(market_info)

# drop rest keep only Close,Volume,COH & Vola
model_data = market_info[['Date'] + [metric for metric in ['Volume', 'Close Off High', 'Day Diff', 'Volatility', 'Movement']]]


# reverse array for ascending order
# model_data = model_data.sort_values(by='Date')

split_date = '2015-06-01'
final_data = model_data[model_data['Date'] > split_date]
# final_data = final_data.drop('Date', 1)
final_data = final_data.drop(final_data.index[len(final_data)-1]) #dropping the last row that doesnt have movement

print(final_data)

with open('features2017test.csv', 'w') as csvfile:
    fieldnames = ['Date', 'Volume', 'Close Off High', 'Day Diff', 'Volatility', 'Movement']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    i=120
    while i < (len(market_info) - 1):

        writer.writerow({'Date': final_data['Date'][i], 'Volume': final_data['Volume'][i],
                     'Close Off High': final_data['Close Off High'][i], 'Day Diff': final_data['Day Diff'][i], 'Volatility': final_data['Volatility'][i], 'Movement': final_data['Movement'][i]})
        i=i+1