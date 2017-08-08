import pandas as pd
import os
import time
import re
from datetime import datetime as dt
from time import mktime
from matplotlib import pyplot as plt
from matplotlib import style
style.use('dark_background')

path = "C:/Users/dasei/Desktop/intraQuarter"

features = ['Total Debt/Equity',
			'Trailing P/E',
			'Price/Sales',
			'Price/Book',
			'Profit Margin',
			'Operating Margin',
			'Return on Assets',
			'Return on Equity',
			'Revenue Per Share',
			'Market Cap',
			'Enterprise Value',
			'Forward P/E',
			'PEG Ratio',
			'Enterprise Value/Revenue',
			'Enterprise Value/EBITDA',
			'Revenue',
			'Gross Profit',
			'EBITDA',
			'Net Income Avl to Common ',
			'Diluted EPS',
			'Earnings Growth',
			'Revenue Growth',
			'Total Cash',
			'Total Cash Per Share',
			'Total Debt',
			'Current Ratio',
			'Book Value Per Share',
			'Cash Flow',
			'Beta',
			'Held by Insiders',
			'Held by Institutions',
			'Shares Short (as of',
			'Short Ratio',
			'Short % of Float',
			'Shares Short (prior ']

def Key_Stats(features):
	statspath = path+'/_KeyStats'
	stock_list = [x[0] for x in os.walk(statspath)]

	sp500_df = pd.DataFrame.from_csv('C:/Users/dasei/OneDrive/Documents/Programs/Python/Machine Learning/data/^GSPC.csv')
	stock_df = pd.DataFrame.from_csv('stock_prices.csv')

	ticker_list   = []
	features_list = []

	for each_dir in stock_list[1:]:
		each_file = os.listdir(each_dir)
		ticker = each_dir.split('\\')[1]
		ticker_list.append(ticker)

		print(ticker)

		if len(each_file) > 0:
			for file in each_file:
				date_stamp = dt.strptime(file, '%Y%m%d%H%M%S.html')
				unix_time = time.mktime(date_stamp.timetuple())
				full_filepath = each_dir+'/'+file
				source = open(full_filepath, 'r').read()
				try:
					# Key Statistics values
					value_list = []
					for each_data in features:
						try:
							regex = re.escape(each_data) + r'.*?(\d{1,8}\.\d{1,8}M?B?|N/A)%?</td>'
							value = re.search(regex, source)
							value = (value.group(1))

							if 'B' in value:
								value = float(value.replace('B',''))*1000000000

							elif 'M' in value:
								value = float(value.replace('M',''))*1000000

							value_list.append(value)

						except Exception as e:
							value_list.append('N/A')

					# SP500 currently
					try:
						sp500_date = dt.fromtimestamp(unix_time).strftime('%Y-%m-%d')
						row = sp500_df[(sp500_df.index == sp500_date)]
						sp500_value = float(row['Adj Close'])
					except Exception as e:
						sp500_date = dt.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
						row = sp500_df[(sp500_df.index == sp500_date)]
						sp500_value = float(row['Adj Close'])
						#print(str(e), 'sp500_value')

					one_year_later = int(unix_time + 31536000)

					# SP500 price 1 year later
					try:
						sp500_1y = dt.fromtimestamp(one_year_later).strftime('%Y-%m-%d')
						row = sp500_df[(sp500_df.index == sp500_1y)]
						sp500_1y_value = float(row['Adj Close'])
					except Exception as e:
						try:
							sp500_1y = dt.fromtimestamp(one_year_later - 259200).strftime('%Y-%m-%d')
							row = sp500_df[(sp500_df.index == sp500_1y)]
							sp500_1y_value = float(row['Adj Close'])
						except Exception as e:
							print(str(e), 'SP500 1 yr')

					# Stock Price 1 year later
					try:
						stock_price_1y = dt.fromtimestamp(one_year_later).strftime('%Y-%m-%d')
						row = stock_df[(stock_df.index == stock_price_1y)][ticker.upper()]
						stock_1y_value = round(float(row), 2)
					except Exception as e:
						try:
							stock_price_1y = dt.fromtimestamp(one_year_later - 259200).strftime('%Y-%m-%d')
							row = stock_df[(stock_df.index == stock_price_1y)][ticker.upper()]
							stock_1y_value = round(float(row), 2)
						except Exception as e:
							print(str(e), '1 yr stock price')

					# Stock Price currently
					try:
						stock_price = dt.fromtimestamp(unix_time).strftime('%Y-%m-%d')
						row = stock_df[(stock_df.index == stock_price)][ticker.upper()]
						stock_price = round(float(row), 2)
					except Exception as e:
						try:
							stock_price = dt.fromtimestamp(unix_time - 259200).strftime('%Y-%m-%d')
							row = stock_df[(stock_df.index == stock_price)][ticker.upper()]
							stock_price = round(float(row), 2)
						except Exception as e:
							print(str(e), 'stock price')

					# Calculate difference and status features
					stock_p_change = round((100 * (stock_1y_value - stock_price) / stock_price), 2)
					sp500_p_change = round((100 * (sp500_1y_value - sp500_value) / sp500_value), 2)
					difference = stock_p_change - sp500_p_change
					
					if difference > 0:
						status ='outperform'
					else:
						status = 'underperform'

					# Collect features in dictionary
					if value_list.count('N/A') > 15:
						pass
					else:
						try:
							features_dict = {'Date':date_stamp,
											 'Unix':unix_time,
											 'Ticker':ticker,
											 'Price':stock_price,
											 'stock_p_change':stock_p_change,
											 'SP500':sp500_value,
											 'sp500_p_change':sp500_p_change,
											 'Difference':difference,
											 'Status':status}
							for i, feature in enumerate(features):
								features_dict[feature] = value_list[i]

							features_list.append(features_dict)

						except Exception as e:
							#print(str(e), 'df creation')
							pass
				except Exception as e:
					pass
	
	df = pd.DataFrame(features_list, columns = ['Date',
												'Unix',
												'Ticker',
												'Price',
												'stock_p_change',
												'SP500',
												'sp500_p_change',
												'Difference',
												'Status']
												+ features)

	df.to_csv('key_stats_acc_perf_WITH_NA.csv')

Key_Stats(features)