#-----------------------------------Strategy---------------------------------------#
# Define order flow as signed volume, eg if 15 contracts traded at the bid price 
# the order flow would be -15 (it would be +15 if it transacted at the offer). 
# Compute ratio of order flow over volume for some period to use as trading signal.
# 1 is all trades at offer, -1 is all trades at bid. Entry signal is if order flow % 
# crosses above/below some threshold. Hold for some number of ticks. Optimize 
# threshold and holding period. 
#----------------------------------------------------------------------------------#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.mplot3d import Axes3D

tickMultiplier = 1000
contracts = 1
#longLag = 100
shortLag = 50
stdThreshold = 2

# get data
filename = 'ZN_M17_5.25.17.txt'
filepath = filepath = 'C:/Users/scipio/OneDrive/Documents/Programs/Python/Backtests/data/'+filename
df = pd.read_csv(filepath)
df.rename(columns=lambda x: x.strip(), inplace=True) #strip whitespace 

# combine Date and Time, convert to datetime, index to datetime
df['Datetime'] = pd.to_datetime(df['Date'].map(str) + df['Time'].map(str))
df.set_index(['Datetime'], inplace=True)

# order flow positive if lift offer, negative if hit bid
df['OrderFlowSign'] = 1
df.loc[(df['BidVolume'] > 0), 'OrderFlowSign'] = -1
df['OrderFlow'] = df['Volume'] * df['OrderFlowSign']

# calculate long/short signals, pnl, and optimal long/short lags & stdThreshold
optimalLongLag = 0
optimalShortLag = 0
optimalStdThreshold = 0
optimalPNL = 0
plotAry = []

for longLag in range(300, 1300, 200):
	for stdThreshold in np.linspace(-1.5, 0.5, 20):
		df['longAvg'] = df['OrderFlow'].rolling(longLag).mean()
		df['shortAvg'] = df['OrderFlow'].rolling(shortLag).mean()
		df['std'] = df['OrderFlow'].rolling(longLag).std()
		df['longRets'] = (df['Low'] - df['High'].shift()) * tickMultiplier * contracts
		df['shortRets'] = (df['High'] - df['Low'].shift()) * tickMultiplier * contracts
		long_idx = (df['shortAvg'] > (df['longAvg'] + df['std'] * stdThreshold))
		short_idx = (df['shortAvg'] < (df['longAvg'] - df['std'] * stdThreshold))
		df['pnl'] = 0.
		df['pnl'][long_idx] = df['longRets'][long_idx] 
		df['pnl'][short_idx] = df['shortRets'][short_idx] 

		plotAry.append( [longLag, stdThreshold, df['pnl'].mean()] )  # data for scatterplot

		if df['pnl'].mean() > optimalPNL:
			optimalPNL = df['pnl'].mean()
			optimalLongLag = longLag
			optimalShortLag = shortLag
			optimalStdThreshold = stdThreshold
	print longLag

print 'Optimal long lag: %i' % (optimalLongLag)
print 'Optimal std threshold: %.1f' % (optimalStdThreshold)
print 'Optimal avg PNL: $%.2f' % (optimalPNL * tickMultiplier * contracts)

#----------test with optimal parameters on out of sample data----------#

# get data
filename = 'ZN_M17_5.24.17.txt'
filepath = filepath = 'C:/Users/scipio/OneDrive/Documents/Programs/Python/Backtests/data/'+filename
df = pd.read_csv(filepath)
df.rename(columns=lambda x: x.strip(), inplace=True) #strip whitespace 

# combine Date and Time, convert to datetime, index to datetime
df['Datetime'] = pd.to_datetime(df['Date'].map(str) + df['Time'].map(str))
df.set_index(['Datetime'], inplace=True)

# order flow positive if lift offer, negative if hit bid
df['OrderFlowSign'] = 1
df.loc[(df['BidVolume'] > 0), 'OrderFlowSign'] = -1
df['OrderFlow'] = df['Volume'] * df['OrderFlowSign']
df['longAvg'] = df['OrderFlow'].rolling(optimalLongLag).mean()
df['shortAvg'] = df['OrderFlow'].rolling(optimalShortLag).mean()
df['std'] = df['OrderFlow'].rolling(optimalLongLag).std()
df['longRets'] = (df['Low'] - df['High'].shift()) * tickMultiplier * contracts
df['shortRets'] = (df['High'] - df['Low'].shift()) * tickMultiplier * contracts
long_idx = (df['shortAvg'] > (df['longAvg'] + df['std'] * optimalStdThreshold))
short_idx = (df['shortAvg'] < (df['longAvg'] - df['std'] * optimalStdThreshold))
df['pnl'] = 0.
df['pnl'][long_idx] = df['longRets'][long_idx] 
df['pnl'][short_idx] = df['shortRets'][short_idx] 

print 'Optimal avg PNL: $%.2f' % (df['pnl'].mean() * tickMultiplier * contracts)

# 3d plot
fig = pylab.figure()
ax = Axes3D(fig)
ax.scatter(*zip(*plotAry))
ax.set_xlabel('Long Lag')
ax.set_ylabel('Std Threshold')
ax.set_zlabel('Avg PNL / Trade')
plt.show()