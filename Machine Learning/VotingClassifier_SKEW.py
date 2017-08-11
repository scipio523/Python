# Attempt to predict daily SP500 return from prior returns, vix, skew index
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime as dt
from Download_Data import load_data
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.dummy import DummyClassifier

ticker = '^GSPC'
start  = '2000-01-03'
end    = '2017-07-28'

# Load data
df = pd.read_csv('data/'+ticker+'.csv', parse_dates=[0], index_col='Date')[start:end]
df['VIX'] = pd.read_csv('data/^VIX.csv', parse_dates=[0], index_col='Date')[start:end]['Adj Close']
df['SKEW'] = pd.read_csv('data/SKEW.csv', parse_dates=[0], index_col='Date')[start:end]['SKEW']

# Define Features
df['VIX_pct'] = df['VIX'].pct_change(periods=20)
df['SKEW_pct'] = df['SKEW'].pct_change(periods=20)
df['1 Day Return'] = df['Adj Close'].pct_change(periods=20)
df.dropna(inplace=True)  # Clear NaNs

# Define Target - future 1 day return
df['FutureReturn'] = df['1 Day Return'].shift(-1)  # we are predicting future day's return so shift 1 day ahead
buy_threshold = 0.5 / 100
sell_threshold = -0.5 / 100
df['Target'] = 0
df.loc[df['FutureReturn'] > buy_threshold, 'Target'] = 1
df.loc[df['FutureReturn'] < sell_threshold, 'Target'] = -1

# Train/test split
X = df.ix[:,:-2]  # all columns except Target
y = df['Target']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0)  # Default: train 75%, test 25% 

# Fit ensemble classifier
clf = VotingClassifier([('knn',  KNeighborsClassifier()),
						('rfor', RandomForestClassifier(random_state=0)),
						('lsvc', LinearSVC())
						]).fit(X_train, y_train)

dummy = DummyClassifier(strategy='stratified').fit(X_train, y_train)

print('Accuracy of Ensemble classifier on training set: {:.2f}'
     .format(clf.score(X_train, y_train)))
print('Accuracy of Ensemble classifier on test set: {:.2f}'
     .format(clf.score(X_test, y_test)))
print('Prediction Spread:', Counter(clf.predict(X_test)))
print('Accuracy of Dummy classifier on test set: {:.2f}'
	 .format(dummy.score(X_test, y_test)))
print('Dummy Prediction Spread:', Counter(dummy.predict(X_test)))

# Plot predictions
X_test = X_test.sort_index()
df['predictions'] = pd.DataFrame(clf.predict(X_test), index=X_test.index)

fig, ax = plt.subplots()
ax.plot(df['Adj Close'][-len(df['predictions']):])
ax.plot(df['predictions'].ix[df['predictions'] == 1].index,
		df['Adj Close'][-len(df['predictions']):][df['predictions'] == 1],
		'^', markersize=5, color='g')
ax.plot(df['predictions'].ix[df['predictions'] == -1].index,
		df['Adj Close'][-len(df['predictions']):][df['predictions'] == -1],
		'^', markersize=5, color='r')
plt.title(ticker)
#plt.show()