import pandas_datareader.data as web

symbols = ['GLD']
source = 'yahoo'
start_date = '1990-01-01'
end_date = '2017-07-31'

def load_data(symbols, source='yahoo', start_date='1990-01-01', end_date='2017-07-31'):
	for symbol in symbols:
		print('Downloading '+symbol+'...')
		data = web.DataReader(symbol, source, start_date, end_date)
		data.to_csv('data/'+symbol+'.csv')

def __init__():
	load_data(symbols)

