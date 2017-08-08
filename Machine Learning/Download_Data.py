import pandas_datareader.data as web

def load_data(symbols, source, start_date, end_date):
	for symbol in symbols:
		print('Downloading '+symbol+'...')
		data = web.DataReader(symbol, source, start_date, end_date)
		data.to_csv('data/'+symbol+'.csv')

if __name__ == "__main__":
	symbols = ['^GSPC']
	source = 'yahoo'
	start_date = '1980-01-01'
	end_date = '2017-08-04'
	load_data(symbols, 'yahoo', start_date, end_date)

