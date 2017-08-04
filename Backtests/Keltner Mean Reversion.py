import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

user = 'scipio' #for desktop
#user = 'dasei' #for laptop
filename = 'CL_F17_500tick.txt'
filepath = 'C:/Users/'+user+'/OneDrive/Documents/Programs/Python/Backtests/data/'+filename
title = 'CL Keltner Mean Reversion'
increment = 2
holdmax = 40

def calcPctReturns(df, period):
	long_rets = (df['Close'].shift(-period)[df.buy == True]) / (df['Close'][df.buy == True]) - 1
	short_rets = (df['Close'].shift(-period)[df.short == True]) / (df['Close'][df.short == True]) - 1
	rets = long_rets.append(-short_rets)
	return rets * 100	#convert to percent

def calcDollarReturns(df, period, mult=1000, contracts=1):
	long_rets = (df['Close'].shift(-period)[df.buy == True] - df['Close'][df.buy == True]) \
				* mult * contracts
	short_rets = (df['Close'].shift(-period)[df.short == True] - df['Close'][df.short == True]) \
				* mult * contracts
	rets = long_rets.append(-short_rets)
	return rets

#load data into pandas dataframe
df = pd.read_csv(filepath)

#strip whitespace from headers, rename Last column to be Close
df.rename(columns=lambda x: x.strip(), inplace=True)
df.rename(columns={'Last': 'Close'}, inplace=True)

#combine Date and Time, convert to datetime, index to datetime
df['Datetime'] = df['Date'].map(str) + df['Time'].map(str)
df['Datetime'] = pd.to_datetime(df['Datetime'])
df.set_index(['Datetime'], inplace=True)

#filter dates/times. This strategy only has positive returns after hours
#df = df[df['Date'] == '2016/7/12']
#df = df[(df['Time'] < ' 09:30:00') | (df['Time'] > ' 16:00:00')]	#after hours
#df = df[(df['Time'] > ' 09:30:00') & (df['Time'] < ' 16:00:00')]	#day session

#--------------------TRADING SIGNALS--------------------#
#long if 'free' bar below bands, short if above bands
lag = 10	#min number of bars before new signal can be generated
df['buy'] = df['Close'] < df['Bottom']
df['short'] = df['Close'] > df['Top']
df['buy'] = (df['Close'] < df['Bottom']) & (pd.rolling_sum(df['buy'], lag) == 1)
df['short'] = (df['Close'] > df['Top']) & (pd.rolling_sum(df['short'], lag) == 1)

#--------------------PLOTS--------------------#
fig = plt.figure()
fig.patch.set_facecolor('white')     				#set the outer colour to white
plt.subplots_adjust(hspace = 0.4)
ax1 = fig.add_subplot(211, ylabel='Price ($)')		#subplot for strategy's signals
plt.title(title)
ax2 = fig.add_subplot(212, ylabel='Cum PnL ($)')	#subplot for cumulative pnl for various holding periods
num_colors = holdmax / increment
cm = plt.get_cmap('gist_rainbow')
ax2.set_color_cycle([cm(1.*i/num_colors) for i in range(num_colors)])

#plot prices & indicators
df['High'].plot(ax=ax1, color='black', lw=1)
df['Low'].plot(ax=ax1, color='black', lw=1)
df['Top'].plot(ax=ax1, color='blue', lw=2)
df['Bottom'].plot(ax=ax1, color='blue', lw=2)

#plot buy/sell markers
ax1.plot(df['buy'].ix[df.buy == True].index, 
	df['Bottom'][df.buy == True],
	'^', markersize=10, color='g')
ax1.plot(df['short'].ix[df.short == True].index, 
	df['Top'][df.short == True],
	'v', markersize=10, color='r')

#--------------------STATISTICS--------------------#
print '		  (Avg $ / Trade)  (Avg $ / Day)    (Sharpe)       (P-value)'
for i in range(increment, holdmax+1, increment):
	#-----$-----#
	df['pnl'] = calcDollarReturns(df, i)
	daily_pnl = df['pnl'].groupby(df.index.date).sum()		#pnl grouped by day

	#-----%-----#
	df['rets'] = calcPctReturns(df, i)
	daily_ret = df['rets'].groupby(df.index.date).sum()		#rets grouped by day
	sharpe = daily_ret.mean() / daily_ret.std() * daily_ret.count() ** .5
	annual_sharpe = sharpe * (252 ** .5)
	pval = (1 - stats.norm.cdf(sharpe))*2	#two-tailed

	print (str(i)+':'+'\t$'+str('%.2f' % df['pnl'].mean()) \
		  +'\t$'+str('%.2f' % daily_pnl.mean()) \
		  +'\t'+str('%.4f' % sharpe) \
		  +'\t'+str('%.4f' % pval)).expandtabs(15)

	#plot equity curve
	df['pnl'].fillna(value=0).cumsum().plot(ax=ax2, label=str(i)+' Bar')

#plot the figure
plt.legend(loc='upper left', bbox_to_anchor=(1,1))
plt.show()
