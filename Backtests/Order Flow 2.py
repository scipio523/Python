import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#-----------------------------------Strategy---------------------------------------#
# Define order flow as signed volume, eg if 15 contracts traded at the bid price 
# the order flow would be -15 (it would be +15 if it transacted at the offer). 
#
#----------------------------------------------------------------------------------#

tick = 0.015625
tickMultiplier = 1000   # 1 contract
lookback = 1000
holdingPeriod = 100
threshold = 3

# get data
filename = 'ZN_M17_5.24.17.txt'
filepath = filepath = 'C:/Users/scipio/OneDrive/Documents/Programs/Python/Backtests/data/'+filename
df = pd.read_csv(filepath)
df.rename(columns=lambda x: x.strip(), inplace=True) #strip whitespace 

# combine Date and Time, convert to datetime, index to datetime
df['Datetime'] = pd.to_datetime(df['Date'].map(str) + df['Time'].map(str))
df.set_index(['Datetime'], inplace=True)

# order flow positive if transaction at offer, negative if at bid
df['OrderFlowSign'] = 1
df.loc[(df['BidVolume'] > 0), 'OrderFlowSign'] = -1
df['OrderFlow'] = df['Volume'] * df['OrderFlowSign']
df['RollingOrderFlow'] = df['OrderFlow'].rolling(lookback).sum()

df['OrderFlowRatio'] = df['RollingOrderFlow'] / df['Volume'].rolling(lookback).sum()

buy_idx  = ( df['RollingOrderFlow'] > (df['RollingOrderFlow'].mean() + df['RollingOrderFlow'].std() * threshold) )
sell_idx = ( df['RollingOrderFlow'] < (df['RollingOrderFlow'].mean() + df['RollingOrderFlow'].std()* threshold) )

print sell_idx.value_counts()

buy_idx.loc[(buy_idx.diff() != 0) & (buy_idx.diff(10) != 0)] = False
sell_idx.loc[sell_idx.diff() != 0] = False

print sell_idx.value_counts()

df['buyPNL'] = 0.
df['shortPNL'] = 0.
df['buyPNL'][buy_idx] = df['Last'][buy_idx].shift(-holdingPeriod) - df['Last'][buy_idx]
df['shortPNL'][sell_idx] = df['Last'][sell_idx] - df['Last'][sell_idx].shift(-holdingPeriod)

print df['buyPNL'].mean()
print df['shortPNL'].mean()
print 'pnl: ', (df['buyPNL'] + df['shortPNL']).mean()
df.Last.plot(c='black', lw=1)
df.Last[buy_idx].plot(marker='^', color='blue')
df.Last[sell_idx].plot(marker='v', color='red')
plt.show()
