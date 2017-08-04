import pandas_datareader.data as web

symbols = ['UUP']
source = 'yahoo'
start_date = '1990-01-01'
end_date = '2017-07-30'

for symbol in symbols:
	print('Downloading '+symbol+'...')
	data = web.DataReader(symbol, source, start_date, end_date)
	data.to_csv(symbol+'.csv')

