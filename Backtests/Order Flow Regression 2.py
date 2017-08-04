import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.api as sm

#-----------------------------------Strategy---------------------------------------#
# Define order flow as signed volume, eg if 15 contracts traded at the bid price 
# the order flow would be -15 (it would be +15 if it transacted at the offer). 
#
#----------------------------------------------------------------------------------#

tick = 0.015625
tickMultiplier = 1000   # 1 contract
lookback = 100

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

# create linear model
X = df['RollingOrderFlow'].shift().diff()[lookback+1:]
Y = df['OrderFlowSign'][lookback+1:]

# linear model for train set
model = sm.OLS(Y, X).fit()
predictions = model.predict(X) # make the predictions by the model

# Print out the statistics
print model.summary()

# Plot 
f, ax1 = plt.subplots()
ax1.scatter(X, Y)
ax1.set_title('Title')
ax1.set_xlabel('Order Flow')
ax1.set_ylabel('1 if ask, -1 if bid')
plt.show()