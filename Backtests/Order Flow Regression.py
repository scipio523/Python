import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
from sklearn import cross_validation

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

# df.OrderFlowRatio.plot(c='green')
# df.Last.diff(-holdingPeriod).plot(c='blue')

# create linear model
X = df.OrderFlow.reshape(-1,1)
Y = df.Last
lm = LinearRegression()
lm.fit(X, Y)

# calculate prediction
pred = lm.predict(X)

# scatterplot comparing true to predicted prices
f, (ax1, ax2) = plt.subplots(2)
plt.subplots_adjust(hspace = 0.5)
ax1.scatter(Y, pred)
ax1.set_title("Actual vs Predicted: $Y_i$ vs $\hat{Y}_i$")
ax1.set_xlabel("Actual: $Y_i$")
ax1.set_ylabel("Predicted: $\hat{Y}_i$")

# calculate mean squared error
mseFull = np.mean((Y - pred) ** 2)
print 'Mean squared error: %.4f' % mseFull

# create randomly generated train and test sets
X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(
	X, Y, test_size=0.30, random_state = 2)

# linear model for train set
lm = LinearRegression()
lm.fit(X_train, Y_train)
pred_train = lm.predict(X_train)
pred_test = lm.predict(X_test)
print 'Fit a model X_train, and calculate MSE for train set:', np.mean((Y_train - pred_train) ** 2)
print 'Fit a model X_train, and calculate MSE for test set:', np.mean((Y_test - pred_test) ** 2)

# check residuals
ax2.scatter(pred_train, pred_train - Y_train, c='b', s=40, alpha=0.5, marker='x')   #train set
ax2.scatter(pred_test, pred_test - Y_test, c='g', s=40)								#test set
ax2.hlines(y = 0, xmin = 125.7, xmax = 126)
ax2.set_title('Residual plot using training (blue) and test (green) data')
ax2.set_ylabel('Residuals')

print lm.coef_

plt.show()