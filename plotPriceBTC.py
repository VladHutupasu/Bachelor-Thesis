import time
import pandas as pd
import datetime
import matplotlib.pyplot as plt


def get_market_data(market, tag=True):
      """
      market: the full name of the cryptocurrency as spelled on coinmarketcap.com. eg.: 'bitcoin'
      tag: eg.: 'btc', if provided it will add a tag to the name of every column.
      returns: panda DataFrame
      This function will use the coinmarketcap.com url for provided coin/token page.
      Reads the OHLCV and Market Cap.
      Converts the date format to be readable.
      Makes sure that the data is consistant by converting non_numeric values to a number very close to 0.
      And finally tags each columns if provided.
      """
      market_data = pd.read_html("https://coinmarketcap.com/currencies/" + market +
                                 "/historical-data/?start=20130428&end="+time.strftime("%Y%m%d"), flavor='html5lib')[0]
      market_data = market_data.assign(Date=pd.to_datetime(market_data['Date']))
      market_data['Volume'] = (pd.to_numeric(market_data['Volume'], errors='coerce').fillna(0))
      if tag:
        market_data.columns = [market_data.columns[0]] + [tag + '_' + i for i in market_data.columns[1:]]
        return market_data

def show_plot(data, tag):
  fig, (ax1, ax2) = plt.subplots(2,1, gridspec_kw = {'height_ratios':[3, 1]})
  ax1.set_ylabel('Closing Price ($)',fontsize=12)
  ax2.set_ylabel('Volume ($ bn)',fontsize=12)
  ax2.set_yticks([int('%d000000000'%i) for i in range(10)])
  ax2.set_yticklabels(range(10))
  ax1.set_xticks([datetime.date(i,j,1) for i in range(2013,2019) for j in [1,7]])
  ax1.set_xticklabels('')
  ax2.set_xticks([datetime.date(i,j,1) for i in range(2013,2019) for j in [1,7]])
  ax2.set_xticklabels([datetime.date(i,j,1).strftime('%b %Y')  for i in range(2013,2019) for j in [1,7]])
  ax1.plot(data['Date'].astype(datetime.datetime),data[tag +'_Open*'])
  ax2.bar(data['Date'].astype(datetime.datetime).values, data[tag +'_Volume'].values)
  fig.tight_layout()
  plt.show()

btc_data = get_market_data("bitcoin", tag='BTC')
print(btc_data.head())
show_plot(btc_data, tag='BTC')