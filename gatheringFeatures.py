import pandas as pd
import time
import csv
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import matplotlib.dates
import matplotlib.pyplot as plt


# --Get market info for bitcoin from the start of April, 2013 to the current day
bitcoin_market_info = pd.read_html(
    "https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end=" + time.strftime("%Y%m%d"))[0]
bitcoin_market_info = bitcoin_market_info.assign(Date=pd.to_datetime(bitcoin_market_info['Date']))
bitcoin_market_info.loc[bitcoin_market_info['Volume'] == "-", 'Volume'] = 0
bitcoin_market_info['Volume'] = bitcoin_market_info['Volume'].astype('int64')

market_info = bitcoin_market_info

#--DATA only for 2017--
# market_info = market_info[market_info['Date'] >= '2017-01-01']
market_info = market_info[market_info['Date'] >= '2018-05-02']
market_info = market_info[market_info['Date'] <= '2018-06-02']

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

# drop rest keep only Close,Volume,COH & Vola
# model_data = market_info[['Date'] + [metric for metric in ['Volume', 'Close Off High', 'Day Diff', 'Volatility', 'Movement']]]
model_data = market_info[['Date', 'Close**', 'Volume', 'Close Off High', 'Day Diff', 'Volatility', 'Movement']]


#Dropping the last row that doesnt have movement
model_data = model_data.drop(model_data.index[len(model_data)-1])
print(model_data)

#----------------------------------------from 02 May ->June 2--------------------------------------------------------------------------
sia = SIA()

#------------------------SIA--------------------------------------
fileCounter = 32
sentimentList=[]
list_dates=market_info['Date']

posValues=[]
negValues=[]
neutralValues=[]


while fileCounter >= 1:
    with open('redditCommentsBitcoinMarketsMay/' + str(fileCounter), 'r', encoding='utf-8', errors='ignore') as file:

        neutralCounter = 0
        positiveCounter = 0
        negativeCounter = 0
        firstLine = file.readlines(1)

        # if 'Daily Discussion,' not in firstLine[0]:
        #     continue

        for line in file:
            res = sia.polarity_scores(line)
            if res['compound'] > 0.2:
                positiveCounter+=1
            elif res['compound'] < -0.2:
                negativeCounter+=1
            else:
                neutralCounter+=1

        posValues.append(positiveCounter)
        negValues.append(negativeCounter)
        neutralValues.append(neutralCounter)

        fileCounter-=1

    # totalSentiment = positiveCounter+negativeCounter+neutralCounter
    totalSentiment = positiveCounter+negativeCounter+neutralCounter
    sentimentList.append(((positiveCounter-negativeCounter)/totalSentiment)*1000)

#---------------plot for SIA----------------------------------------------
plt.plot(list_dates, posValues, color='g', label='positive')
plt.plot(list_dates, negValues, color='red', label='negative')
plt.plot(list_dates, neutralValues, color='orange', label='neutral')
plt.gcf().autofmt_xdate()
plt.legend()
plt.xlabel('Time line')
plt.ylabel('No. of comments')
plt.title('Positive, negative & neutral sentiment over time')
plt.show()
#---------------------------------------------------------------------------


#------------------------SIA2--------------------------------------
fileCounter = 32
sentimentList2=[]


while fileCounter >= 1:

    with open('redditCommentBitcoinMay/' + str(fileCounter), 'r', encoding='utf-8', errors='ignore') as file:

        neutralCounter = 0
        positiveCounter = 0
        negativeCounter = 0
        firstLine = file.readlines(1)

        # if 'Daily Discussion,' not in firstLine[0]:
        #     continue

        for line in file:
            res = sia.polarity_scores(line)
            if res['compound'] > 0.2:
                positiveCounter+=1
            elif res['compound'] < -0.2:
                negativeCounter+=1
            else:
                neutralCounter+=1

        fileCounter-=1

    # totalSentiment = positiveCounter+negativeCounter+neutralCounter
    totalSentiment = positiveCounter+negativeCounter+neutralCounter
    sentimentList2.append(((positiveCounter-negativeCounter)/totalSentiment)*1000)


print('Length is'+str(len(sentimentList2)))

#-------------------------------------------------------------------------------------------------------------------------


with open('scrath.csv', 'w') as csvfile:
    fieldnames = ['Date', 'Close**', 'Volume', 'Close Off High', 'Day Diff', 'Volatility', 'SIA', 'SIA2','Movement']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    i=0
    while i < (len(market_info) - 1):

        writer.writerow({'Date': model_data['Date'][i], 'Close**': model_data['Close**'][i], 'Volume': model_data['Volume'][i],
                         'Close Off High': model_data['Close Off High'][i], 'Day Diff': model_data['Day Diff'][i],
                         'Volatility': model_data['Volatility'][i], 'SIA': sentimentList[i], 'SIA2': sentimentList2[i],'Movement': model_data['Movement'][i]})
        i=i+1