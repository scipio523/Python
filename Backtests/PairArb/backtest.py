import sys
import csv
import pull_historical_data
import numpy as np

#output_path = '/Users/Scipio/OneDrive/Programs/Python'
#sys.path.append(output_path)
directory = 'PairArb'

def getData(ticker, start_date, end_date):
	#Call function to download csv file from Yahoo finance
	pull_historical_data.get_data(ticker, directory)
	datafile = open(ticker + '.csv', 'r')
	datareader = csv.reader(datafile)
	
	#Move data from csv file to array and format it
	data = []
	for row in datareader:
		count = 1
		if(row[0] == "Date"): continue	
		date = str(row[0])		
		date = int(date[:4] + date[5:7] + date[8:])	
		adjclose = round(float(row[6]), 2)
		new_bar = [date, adjclose]
		data.append(new_bar)			
	
	#Slice data for the timeframe we want and isolate the price
	for row in data:
		if(row[0] == int(end_date)): end_date_pos = data.index(row)
		if(row[0] == int(start_date)): start_date_pos = data.index(row)
	data = sorted(data[end_date_pos : start_date_pos + 1])
	data = [row.pop(1) for row in data]
	
	#Split data into trainset and testset
	mid   = int(round(len(data)*0.5, 0))
	train = data[:mid]
	test  = data[mid:]
	return train, test

def get_spreads(x_series, y_series):
	#calculate hedgeratio as OLS beta
	n, xsum, ysum, xysum, xxsum = len(x_series), 0, 0, 0, 0
	for x, y in zip(x_series, y_series):		
		xsum += x
		ysum += y
		xysum += x*y
		xxsum += x*x
	hedgeratio = (n*xysum - xsum*ysum) / (n*xxsum - xsum*xsum) 
	spreads = []
	for x, y in zip(x_series, y_series):		
		spread = x - hedgeratio*y
		spreads.append(spread)
	return spreads

def get_zscores(spreads):
	spreadmean = np.mean(spreads)
	spreadstd = np.std(spreads)
	zlist = []
	for spread in spreads:
		z = (spread - spreadmean) / spreadstd
		zlist.append(z)
	return zlist

def lag(list):
	return list[1:len(list)-1]

def backtest(ticker1, ticker2, start_date, end_date):
	pair1_train, pair1_test = getData(ticker1, start_date, end_date)
	pair2_train, pair2_test = getData(ticker2, start_date, end_date)
	
	spreads = get_spreads(pair1_train, pair2_train)
	zlist = get_zscores(spreads)

	#z-score entry/exit parameters
	long_entry = -1
	short_entry = 1
	exit = 0.5

	#create lags 
	zlist_lag = lag(zlist)
	pair1_train_lag = lag(pair1_train)
	pair2_train_lag = lag(pair2_train)

	dailyret = []
	for i in range(len(zlist)):
		ret = ()

	sharpe_train = np.sqrt(252)*np.mean(pnl(pair1_train))

backtest('GLD', 'GDX', '20100702', '20130710')










