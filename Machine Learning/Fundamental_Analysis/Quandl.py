import pandas as pd
import os
import time
import quandl
quandl.ApiConfig.api_key = '24j97rXQ8QwNoN1ssXbj'

path = "C:/Users/dasei/Desktop/intraQuarter"

def Stock_Prices():
	df = pd.DataFrame()
	statspath = path + '/_KeyStats'
	stock_list = [x[0] for x in os.walk(statspath)]

	for each_dir in stock_list[1:]:
		try:
			ticker = each_dir.split('\\')[1]
			print(ticker)
			data = quandl.get('WIKI/' + ticker.upper(), 
								trim_start = '2000-12-12',
								trim_end   = '2014-12-30',)
			data[ticker.upper()] = data['Adj. Close']
			df = pd.concat([df, data[ticker.upper()]], axis = 1)
		
		except Exception as e:
			print('1st try', str(e))
			time.sleep(10)
			try:
				ticker = each_dir.split('\\')[1]
				data = quandl.get('WIKI/' + ticker.upper(), 
								trim_start = '2000-12-12',
								trim_end   = '2014-12-30',)
				data[ticker.upper()] = data['Adj. Close']
				df = pd.concat([df, data[ticker.upper()]], axis = 1)
			except Exception as e:
				print('2nd try', str(e))
				time.sleep(10)

	df.to_csv('stock_prices_new.csv')

Stock_Prices()
