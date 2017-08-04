import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick2_ochl as candle
import quandl

quandl.ApiConfig.api_key = "24j97rXQ8QwNoN1ssXbj"

def get_data(stock, start="2013-01-01", end="2016-01-01"):
	return quandl.get("YAHOO/INDEX_"+str(stock), start_date=start, end_date=end)

def main(stock, ema_length=20):

	#get stock data
	df = get_data(stock)
	Open = df['Open']
	Close = df['Close']
	Low = df['Low']
	High = df['High']
	AdjClose=df['Adjusted Close']

	#calc moving avg
	ma = pd.rolling_mean(AdjClose, window=ema_length)

	#calc rolling stdev
	std = pd.rolling_std(AdjClose, window=ema_length)

	#calc bands
	upper_band = ma + std * 2
	lower_band = ma - std * 2

	#cut off data for which there is no moving avg
	df=df[ema_length:]
	
	#plot data
	ax = AdjClose.plot(title='SPY', label='SPY', color='black')
	#ax = plt.subplot2grid((1,1), (0,0), rowspan=1, colspan=1, axisbg='white')
	#candle(ax, Open, Close, High, Low, width=.6, colorup='#53c156', colordown='#ff1717', alpha=.75)
	ma.plot(label='moving average', color='blue', ax=ax)
	upper_band.plot(label='upper band', color='blue', ax=ax)
	lower_band.plot(label='lower band', color='blue', ax=ax)
	ax.set_xlabel("Date")
	ax.set_ylabel("Price")
	plt.show()
	
main("SPY")