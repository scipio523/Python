import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

user = 'dasei'
file1 = 'ES_U16_500tick.txt'
file2 = 'ES_U16_5000tick.txt'
filepath1 = 'C:/Users/'+user+'/OneDrive/Documents/Programs/Python/Backtests/data/'+file1
filepath2 = 'C:/Users/'+user+'/OneDrive/Documents/Programs/Python/Backtests/data/'+file2
title = 'ES Keltner Pullback'
increment = 2
holdmax = 40

#load data into pandas dataframe
df1 = pd.read_csv(filepath1)
df2 = pd.read_csv(filepath2)

#strip whitespace from headers, rename Last column to be Close
df1.rename(columns=lambda x: x.strip(), inplace=True)
df1.rename(columns={'Last': 'Close'}, inplace=True)

df2.rename(columns=lambda x: x.strip(), inplace=True)
df2.rename(columns={'Last': 'Close'}, inplace=True)

#combine Date and Time, convert to datetime, index to datetime
df1['Datetime'] = df1['Date'].map(str) + df1['Time'].map(str)
df1['Datetime'] = pd.to_datetime(df1['Datetime'])
df1.set_index(['Datetime'], inplace=True)

df2['Datetime'] = df2['Date'].map(str) + df2['Time'].map(str)
df2['Datetime'] = pd.to_datetime(df2['Datetime'])
df2.set_index(['Datetime'], inplace=True)

#filter dates/times
#df1 = df1[(df1['Date'] == '2016/3/12') | (df1['Date'] == '2016/3/14')]
#df1 = df1[(df1['Time'] < ' 09:30:00') | (df1['Time'] > ' 16:00:00')]	#after hours
df1 = df1[(df1['Time'] > ' 09:30:00') & (df1['Time'] < ' 16:00:00')]	#day session

#df2 = df2[(df2['Date'] == '2016/3/12') | (df2['Date'] == '2016/3/14')]
#df2 = df2[(df2['Time'] < ' 09:30:00') | (df2['Time'] > ' 16:00:00')]	#after hours
df2 = df2[(df2['Time'] > ' 09:30:00') & (df2['Time'] < ' 16:00:00')]	#day session

#--------------------TRADING SIGNALS--------------------#
#logic for the 'overshoot' setup
df1.loc[df1['High'] > df1['Top'], 'setup'] = 1
df1.loc[df1['Low'] < df1['Bottom'], 'setup'] = -1

#logic for touching the previous bar's EMA
df1['setup'].loc[(df1['Low'] <= df1['Keltner Average'].shift()) & \
			   (df1['High'] >= df1['Keltner Average'].shift())] = 0
df1['setup'] = df1['setup'].ffill()

#logic for higher timeframe above/below EMA
df2.loc[df2['Low'] > df2['Keltner Average'], 'setup'] = 1
df2.loc[df2['Low'] < df2['Keltner Average'], 'setup'] = -1

#generate the actual buy/sell signals (first EMA touch after an overshoot)
df1.loc[(df1['setup'] == 0) & (df1['setup'].shift() == 1), 'signal'] = 1
df1.loc[(df1['setup'] == 0) & (df1['setup'].shift() == -1), 'signal'] = -1

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
df1['High'].plot(ax=ax1, color='black', lw=1)
df1['Low'].plot(ax=ax1, color='black', lw=1)
df1['Top'].plot(ax=ax1, color='blue', lw=2)
df1['Bottom'].plot(ax=ax1, color='blue', lw=2)

#plot buy/sell markers
ax1.plot(df1['signal'].ix[df1['signal'] == 1].index, 
	df1['Low'][df1['signal'] == 1],
	'^', markersize=10, color='g')
ax1.plot(df1['signal'].ix[df1['signal'] == -1].index, 
	df1['High'][df1['signal'] == -1],
	'v', markersize=10, color='r')

#--------------------STATISTICS--------------------#
def calcPctReturns(df, period):
	long_rets = (df['Close'].shift(-period)[df.signal == 1]) / (df['Open'].shift(-1)[df.signal == 1]) - 1
	short_rets = (df['Close'].shift(-period)[df.signal == -1]) / (df['Open'].shift(-1)[df.signal == -1]) - 1
	rets = long_rets.append(-short_rets)
	return rets * 100	#convert to percent

def calcDollarReturns(df, period, mult=50, contracts=1):
	long_rets = (df['Close'].shift(-period)[df.signal == 1] - df['Open'].shift(-1)[df.signal == 1]) \
				* mult * contracts
	short_rets = (df['Close'].shift(-period)[df.signal == -1] - df['Open'].shift(-1)[df.signal == -1]) \
				* mult * contracts
	rets = long_rets.append(-short_rets)
	return rets

print '(Bars)   (Avg $ / Trade)  (Avg $ / Day)  (Annual Sharpe)   (P-value)'
for i in range(increment, holdmax+1, increment):
	#-----$-----#
	df1['pnl'] = calcDollarReturns(df1, i)
	daily_pnl = df1['pnl'].groupby(df1.index.date).sum()					#pnl grouped by day

	#-----%-----#
	df1['rets'] = calcPctReturns(df1, i)
	daily_ret = df1['rets'].groupby(df1.index.date).sum()					#rets grouped by day
	annual_sharpe = daily_ret.mean() / daily_ret.std() * 252 ** .5
	pval = (1 - stats.norm.cdf(annual_sharpe))*2							#two-tailed

	print (str(i)+':'+'\t$'+str('%.2f' % df1['pnl'].mean()) \
		  +'\t$'+str('%.2f' % daily_pnl.mean()) \
		  +'\t'+str('%.4f' % annual_sharpe) \
		  +'\t'+str('%.4f' % pval)).expandtabs(15)

	#plot equity curve
	df1['pnl'].fillna(value=0).cumsum().plot(ax=ax2, label=str(i)+' Bar')

#plot the figure
plt.legend(loc='upper left', bbox_to_anchor=(1,1))
plt.show()