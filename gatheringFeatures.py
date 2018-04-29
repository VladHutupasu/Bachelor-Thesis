import pandas as pd
import time
import csv

# --Get market info for bitcoin from the start of April, 2013 to the current day
bitcoin_market_info = pd.read_html(
    "https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end=" + time.strftime("%Y%m%d"))[0]
bitcoin_market_info = bitcoin_market_info.assign(Date=pd.to_datetime(bitcoin_market_info['Date']))
bitcoin_market_info.loc[bitcoin_market_info['Volume'] == "-", 'Volume'] = 0
bitcoin_market_info['Volume'] = bitcoin_market_info['Volume'].astype('int64')
# print(bitcoin_market_info)


# --Create Day Diff column with values--
market_info = bitcoin_market_info
market_info = market_info[market_info['Date'] >= '2016-01-01']
kwargs = {'Day Diff': lambda x: (x['Close'] - x['Open']) / x['Open']}
market_info = market_info.assign(**kwargs)
# print(market_info)


# --Create Close Off High and Volatility column--
# Close_Off_High represents the gap between the closing price and price high for that day, where values
# of -1 and 1 mean the closing price was equal to the daily HIGH or daily LOW, respectively
# Volatility column is simply the difference between high and low price divided by the opening price

kwargs = {'Close Off High': lambda x: 2 * (x['High'] - x['Close']) / (x['High'] - x['Low']) - 1,
          'Volatility': lambda x: (x['High'] - x['Low']) / (x['Open'])}
market_info = market_info.assign(**kwargs)
# print(market_info)






# drop rest keep only Close,Volume,COH & Vola
model_data = market_info[['Date'] + [metric for metric in ['Close', 'Volume', 'Close Off High', 'Volatility']]]
# reverse array for ascending order
model_data = model_data.sort_values(by='Date')
# print(type(model_data))
# print(model_data)

split_date = '2015-06-01'
final_data = model_data[model_data['Date'] > split_date]
final_data = final_data.drop('Date', 1)
# pos 0 ->> 2018
print(final_data)

with open('features.csv', 'w') as csvfile:
    fieldnames = ['Close', 'Volume', 'Close Off High', 'Volatility']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    for i in range(len(final_data)):
        writer.writeheader()
        writer.writerow({'Close': final_data['Close'][i], 'Volume': final_data['Volume'][i],
                     'Close Off High': final_data['Close Off High'][i], 'Volatility': final_data['Volatility'][i]})
