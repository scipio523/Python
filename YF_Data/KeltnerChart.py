import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
from matplotlib.finance import quotes_historical_yahoo_ohlc
import numpy as np
import pandas as pd
import urllib2
import datetime as dt
import pylab

def calcEMA(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a
	
def calcATR(date, highp, lowp, closep, window=10):
	x = 1
	TRDates = []
	TrueRanges = []

	while x < len(date):
		trueHigh=max(highp[x], closep[x-1])
		trueLow=min(lowp[x], closep[x-1])
		TrueRange = trueHigh - trueLow
		TrueRanges.append(TrueRange)
		x += 1

	return calcEMA(TrueRanges, window)

def calcKeltner(EMA, ATR, ATRmult):
	#make EMA and ATR same length
	EMA = EMA[1:] 

	upper = EMA + ATRmult * ATR
	lower = EMA - ATRmult * ATR

	return upper, lower

def generateTrades(date, closep, upper, lower, EMA):
	#make everything same length
	date, closep, EMA = date[1:], closep[1:], EMA [1:]
	x = 0
	signal = 'NONE'
	trigger = 'NONE'

	#create empty arrays filled with NaNs
	buyAry = np.empty(len(date))
	buyAry.fill(np.nan)
	sellAry = np.empty(len(date))
	sellAry.fill(np.nan)

	while x < len(date):
		if signal == 'BUY' and closep[x] > lower[x]: trigger = 'BUY'
		if signal == 'SELL' and closep[x] < upper[x]: trigger = 'SELL'

		if closep[x] < lower[x]: signal = 'BUY'
		elif closep[x] > upper[x]: signal = 'SELL'
		else: signal = 'NONE'

		if trigger == 'BUY': buyAry[x] = (closep[x])
		elif trigger == 'SELL': sellAry[x] = (closep[x])

		trigger = 'NONE'
		x+= 1

	return buyAry, sellAry

def graph_data(stock, timeframe, ema_period=20, ATRmult=2.25):
    
    """
    #download stock data
    stock_price_url = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range='+timeframe+'/csv'
    source_code = urllib2.urlopen(stock_price_url).read()
    stock_data = []
    split_source = source_code.split('\n')

    if 'd' in timeframe:
        dateformat = '%Y-%m-%d %H:%M:%S'
        xUnits = '%H:%M:%S'
    	xFrequency = 50
    	candleWidth = .0002
    else :
        dateformat = '%Y%m%d'
        xUnits = '%Y%m%d'
        xFrequency = 10
        candleWidth = .5
    
    for line in split_source:
        split_line = line.split(',')

        fixMe = split_line[0]

        if len(split_line) == 6:
            if 'values' not in line and 'labels' not in line:
                if 'd' in timeframe:
                    line = line.replace(fixMe,str(dt.datetime.fromtimestamp(int(fixMe)).strftime(dateformat)))
                stock_data.append(line)
    """

    #load data into pandas dataframe
    df = pd.read_csv('~\OneDrive\Documents\Programs\Python\YF_Data\data\SPY.txt')

    #strip whitespace from headers
    df.rename(columns=lambda x: x.strip(), inplace=True)

    #combine Date and Time, convert to datetime
    df['Datetime'] = df['Date'].map(str) + df['Time'].map(str)
    df['Datetime'] = pd.to_datetime(df['Datetime'])

    date = df['Datetime']
    closep = df['Last']
    highp = df['High']
    lowp = df['Low']
    openp = df['Open']
    volume = df['Volume']

    """
    date, closep, highp, lowp, openp, volume = np.loadtxt(stock_data,
                                                          delimiter=',',
                                                          unpack=True,
                                                          converters={0: mdates.strpdate2num(dateformat)})
    """

    EMA = calcEMA(closep, ema_period)
    ATR = calcATR(date, highp, lowp, closep)
    upper, lower = calcKeltner(EMA, ATR, ATRmult)
    buyAry, sellAry = generateTrades(date, closep, upper, lower, EMA)

    start = -len(date[ema_period-1:])

    x = 0
    y = len(date)
    ohlc = []

    while x < y:
    	#use index for x axis to account for 
    	#date[x] = x

        append_me = date[x], openp[x], highp[x], lowp[x], closep[x], volume[x]
        ohlc.append(append_me)
        x+=1

    #make a plot
    fig = plt.figure()
    ax1 = plt.subplot(1, 1, 1, axisbg='#07000d')

    #plot Candlesticks
    candlestick_ohlc(ax1, ohlc, width=candleWidth, colorup='#77d879', colordown='#db3f3f')

    #plot EMA
    ax1.plot(date[start:], EMA[start:], color='w', label=str(ema_period)+' EMA', linewidth=1.5)

    #plot Keltner Channels
    ax1.plot(date[start:], upper[start:], color='w', label=str(ema_period)+' EMA + '+str(ATRmult)+' ATRs', linewidth=1.5)
    ax1.plot(date[start:], lower[start:], color='w', label=str(ema_period)+' EMA - '+str(ATRmult)+' ATRs', linewidth=1.5)
    ax1.fill_between(date[start:], upper[start:], EMA[start:], alpha=0.5, facecolor='#00ffe8', edgecolor='#00ffe8')
    ax1.fill_between(date[start:], EMA[start:], lower[start:], alpha=0.5, facecolor='#00ffe8', edgecolor='#00ffe8')

    #plot Trades
    ax1.plot(date[start:], buyAry[start:], marker='^', markersize=7, color='b')
    ax1.plot(date[start:], sellAry[start:], marker='v', markersize=7, color='r')

    #rotate dates
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(60)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter(xUnits))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(xFrequency))
    ax1.grid(True, color='w')

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(stock)
    plt.legend(loc=9, ncol=3, prop={'size':9}, fancybox=True, borderaxespad=0)
    #plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    plt.show()

graph_data('SPY', '1d')
