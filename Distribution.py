import time
import pandas as pd
import csv
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import matplotlib.dates
import matplotlib.pyplot as plt
from scipy.stats import norm
from datetime import datetime


def closeOverTime(market_info):
    market_info.Close.plot(logy=True)
    plt.legend()
    plt.show()

def returnHist(market_info):
    # Trying to fit the returns to a normal distribution

    parameters = norm.fit(market_info.Returns - 1)

    # now, parameters[0] and parameters[1] are the mean and the standard deviation of the fitted distribution
    x = np.linspace(min(market_info.Returns - 1), max(market_info.Returns - 1), 100)

    # Generate the pdf (fitted distribution)
    fitted_pdf = norm.pdf(x, loc=parameters[0], scale=parameters[1])
    # Generate the pdf (normal distribution non fitted)
    normal_pdf = norm.pdf(x)

    # Type help(plot) for a ton of information on pyplot
    plt.plot(x,fitted_pdf,"red",label="Fitted normal dist",linestyle="dashed", linewidth=2)
    plt.plot(x,normal_pdf,"blue",label="Non-fitted normal dist", linewidth=2)
    plt.hist(market_info.Returns-1,density=1,color="b",alpha=.3, bins=10, label='Daily returns')
    plt.title("Bitcoin distribution in Returns")
    plt.legend()
    # plt.show()

    percentages = []
    probabilities = []

    for x in ((market_info.Returns-1)*100):
        percentages.append(round(x, 1))

    w = np.linspace(-25, 25, 501)

    for i in w:
        probabilities.append(percentages.count(i)/len(percentages))
        if i == -19.4:
            probabilities.append(10.6)
            print("------------------------------------------------")

        else:
            probabilities.append(percentages.count(i) / len(percentages))
        print("Chance for the price to go "+str(i)+"% is ->"+str(percentages.count(i)/len(percentages))+"%")


    highest = max(probabilities)
    print("Highest probability -> "+str(highest) + " | at percentage movement -> " +
          str((probabilities.index(highest)-250)/10) + "%")





def showDist(start_date, end_date):

    # --Get market info for bitcoin from the start of April, 2013 to the current day
    bitcoin_market_info = pd.read_html(
        "https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end=" + time.strftime("%Y%m%d"))[0]
    bitcoin_market_info = bitcoin_market_info.assign(Date=pd.to_datetime(bitcoin_market_info['Date']))
    bitcoin_market_info.loc[bitcoin_market_info['Volume'] == "-", 'Volume'] = 0
    bitcoin_market_info['Volume'] = bitcoin_market_info['Volume'].astype('int64')

    market_info = bitcoin_market_info

    # filter the requested data
    market_info = market_info[market_info['Date'] <= end_date]
    market_info = market_info[market_info['Date'] >= start_date]


    market_info.index = pd.to_datetime(market_info.Date)
    market_info = market_info.drop(['Date'], axis=1)
    market_info = market_info[['Close**']]


    market_info.columns = ['Close']
    market_info['Close'].replace(0, np.nan, inplace=True)
    market_info = market_info.dropna()

    # create returns column
    market_info['Returns'] = (market_info['Close'].pct_change() + 1).fillna(1)


    # closeOverTime(market_info)
    returnHist(market_info)


showDist('2018-01-02', '2018-06-02')












