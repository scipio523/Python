#-----------------------------------Strategy---------------------------------------#
#  Test if bid/ask liquidity imbalance can predict future bid/ask
#----------------------------------------------------------------------------------#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load data
files = ['EPU17-CQG-CME-Futures-Tick-Bid',
		 'EPU17-CQG-CME-Futures-Tick-Ask',
		 'EPU17-CQG-CME-Futures-Tick-Trade']

dflist = []
for file in files:
	filepath = 'C:/Users/scipio/OneDrive/Documents/Programs/Python/Backtests/data/'+file+'.txt'
	df = pd.read_csv(filepath)
	df = df[(df['Time'] >= '09:30:00') & (df['Time'] <= '16:00:00')]	#morning session
	# combine Date and Time, convert to datetime, index to datetime
	df['Datetime'] = pd.to_datetime(df['Date'] + df['Time'], format="%m/%d/%Y%H:%M:%S.%f")
	df.set_index(['Datetime'], inplace=True)
	del(df['Date'], df['Time'])
	dflist.append(df)

bids = dflist[0]
asks = dflist[1]
trades = dflist[2]

# join into single dataframe
df = bids.join(asks, how='outer', lsuffix='_bid', rsuffix='_ask')
#df = df.join(trades, how='outer')
# fill NaNs
for column in df:
	df[column] = df[column].ffill()

print df.groupby(pd.TimeGrouper('1s'))

# find probability best ask decreases given best bid/ask
#print asks['Price'].diff().value_counts()