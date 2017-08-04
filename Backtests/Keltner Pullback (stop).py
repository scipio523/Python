import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

user = 'dasei'
filename = 'ES_U16_5min.txt'
filepath = 'C:/Users/'+user+'/OneDrive/Documents/Programs/Python/Backtests/data/'+filename
title = 'ES Keltner Pullback'
increment = 1
riskmax = 5

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print x
    pd.reset_option('display.max_rows')

def roundup_tick(price):
	remainder = price % 0.25
	price.loc[remainder != 0] = price + 0.25 - remainder
	return price

#load data into pandas dataframe
df = pd.read_csv(filepath)

#strip whitespace from headers, rename Last column to be Close
df.rename(columns=lambda x: x.strip(), inplace=True)
df.rename(columns={'Last': 'Close'}, inplace=True)

#combine Date and Time, convert to datetime, index to datetime
df['Datetime'] = df['Date'].map(str) + df['Time'].map(str)
df['Datetime'] = pd.to_datetime(df['Datetime'])
df.set_index(['Datetime'], inplace=True)

#filter dates/times
#df = df[(df['Date'] == '2016/6/27') | (df['Date'] == '2016/6/28')]
#df = df[(df['Time'] < ' 09:30:00') | (df['Time'] > ' 16:00:00')]	#after hours
df = df[(df['Time'] > ' 09:30:00') & (df['Time'] < ' 14:00:00')]	#day session

#--------------------TRADING SIGNALS--------------------#
#logic for the 'overshoot' setup
df.loc[df['High'] > df['Top'], 'setup'] = 1
df.loc[df['Low'] < df['Bottom'], 'setup'] = -1

#logic for touching the previous bar's EMA
df['setup'].loc[(df['Low'] <= df['Keltner Average'].shift()) & \
			   (df['High'] >= df['Keltner Average'].shift())] = 0
df['setup'] = df['setup'].ffill()

#generate the actual buy/sell signals (first EMA touch after an overshoot)
df.loc[(df['setup'] == 0) & (df['setup'].shift() == 1), 'entrySignal'] = 1
#df.loc[(df['setup'] == 0) & (df['setup'].shift() == -1), 'entrySignal'] = -1

#entry price
df.loc[df['entrySignal'] == 1, 'entryPrice'] = roundup_tick(df['Keltner Average'].shift())
df['entryPrice'] = df['entryPrice'].ffill() 

#hi/lo pnl
df['hiPNL'] = df['High'] - df['entryPrice'] 
df['loPNL'] = df['entryPrice'] - df['Low']

print '		                   (Total pnl)    (Avg pnl)      (# Entries)     (# Exits)'
i = 1
for i in range(increment, riskmax, increment):

	risk = i
	ptarget = risk

	#check if stop or target hit
	df['signal'] = df['entrySignal']
	df['signal'].loc[(df['entrySignal'] != 1) & (df['hiPNL'] > ptarget)] = 2	#profit target hit
	df['signal'].loc[(df['entrySignal'] != 1) & (df['loPNL'] >= risk)] = 3		#stop loss hit
	df['signal'] = df['signal'].ffill()

	#trade pnl
	df.loc[(df['signal'] == 2) & (df['signal'].shift() == 1), 'pnl'] = ptarget
	df.loc[(df['signal'] == 3) & (df['signal'].shift() == 1), 'pnl'] = -risk

	df.loc[(df['signal'] == 2) & (df['signal'].shift() == 1), 'exitSignal'] = 1
	df.loc[(df['signal'] == 3) & (df['signal'].shift() == 1), 'exitSignal'] = 1

	del(df['signal'])

	print ('stop/target: %.2f/%.2f' % (risk, ptarget) \
		  +'\t'+'%.2f' % df['pnl'].sum() \
		  +'\t'+'%.2f' % df['pnl'].mean() \
		  +'\t'+'%.2f' % df['entrySignal'].count() \
		  +'\t'+'%.2f' % df['exitSignal'].count()).expandtabs(15)


#--------------------PLOTS--------------------#
fig = plt.figure()
fig.patch.set_facecolor('white')     				#set the outer colour to white
plt.subplots_adjust(hspace = 0.4)
ax1 = fig.add_subplot(211, ylabel='Price ($)')		#subplot for strategy's signals
plt.title(title)
ax2 = fig.add_subplot(212, ylabel='Cum PnL ($)')	#subplot for cumulative pnl for various holding periods
num_colors = riskmax / increment
cm = plt.get_cmap('gist_rainbow')
ax2.set_color_cycle([cm(1.*i/num_colors) for i in range(num_colors)])

#plot prices & indicators
df['High'].plot(ax=ax1, color='black', lw=1)
df['Low'].plot(ax=ax1, color='black', lw=1)
df['Top'].plot(ax=ax1, color='blue', lw=2)
df['Bottom'].plot(ax=ax1, color='blue', lw=2)

#plot buy/sell markers
ax1.plot(df['entrySignal'].ix[df['entrySignal'] == 1].index, 
	df['Low'][df['entrySignal'] == 1],
	'^', markersize=10, color='g')

'''
ax1.plot(df['exitSignal'].ix[df['exitSignal'] == 1].index, 
	df['Low'][df['exitSignal'] == 1],
	'v', markersize=10, color='r')

ax1.plot(df['entrySignal'].ix[df['entrySignal'] == -1].index, 
	df['High'][df['entrySignal'] == -1],
	'v', markersize=10, color='r')
'''

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

'''
print '		  (Avg $ / Trade)  (Avg $ / Day)   (Annual Sharpe)  (P-value)'
for i in range(increment, holdmax+1, increment):
	#-----$-----#
	df['pnl'] = calcDollarReturns(df, i)
	daily_pnl = df['pnl'].groupby(df.index.date).sum()		#pnl grouped by day

	#-----%-----#
	df['rets'] = calcPctReturns(df, i)
	daily_ret = df['rets'].groupby(df.index.date).sum()		#rets grouped by day
	annual_sharpe = daily_ret.mean() / daily_ret.std() * 252 ** .5
	pval = (1 - stats.norm.cdf(annual_sharpe))*2	#two-tailed

	print (str(i)+':'+'\t$'+str('%.2f' % df['pnl'].mean()) \
		  +'\t$'+str('%.2f' % daily_pnl.mean()) \
		  +'\t'+str('%.4f' % annual_sharpe) \
		  +'\t'+str('%.4f' % pval)).expandtabs(15)

	#plot equity curve
	df['pnl'].fillna(value=0).cumsum().plot(ax=ax2, label=str(i)+' Bar')

print '# trades: %i' % df['signal'].count()

#plot the figure
plt.legend(loc='upper left', bbox_to_anchor=(1,1))
'''

plt.show()