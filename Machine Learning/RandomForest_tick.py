import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

file = 'ES_MU16_500tick.txt'

# Load data
data = pd.read_csv('data/'+file)  # Get last n days
data.rename(columns=lambda x: x.strip(), inplace=True)  #strip whitespace from headers
data['Datetime'] = data['Date'].map(str) + data['Time'].map(str)
data['Datetime'] = pd.to_datetime(data['Datetime'])  #combine Date and Time, convert to datetime

# Define Features
df = pd.DataFrame(index=data.index)
df['1 Day Return'] = data['Last'].pct_change()
df['2 Day Return'] = data['Last'].pct_change(periods=5)
df['3 Day Return'] = data['Last'].pct_change(periods=10)
df['4 Day Return'] = data['Last'].pct_change(periods=20)
df['5 Day Return'] = data['Last'].pct_change(periods=30)
df['Target'] = df['1 Day Return'].shift(-1)  # we are predicting future day's return so shift 1 day ahead
df.dropna(inplace=True)  # Clear NaNs

X = df.ix[:,:-1]
y = df['Target']
X_train, X_test, y_train, y_test = train_test_split(X.as_matrix(),
                                                   y.as_matrix(),
                                                   random_state = 0)

clf = RandomForestRegressor(n_estimators = 10, random_state=0).fit(X_train, y_train)

print('Random Forest, SPY, default settings')
print('Accuracy of RF classifier on training set: {:.2f}'
     .format(clf.score(X_train, y_train)))
print('Accuracy of RF classifier on test set: {:.2f}'
     .format(clf.score(X_test, y_test)))

# df['Adj Close'].plot()
# plt.title('SPY '+str(df.index[0])+' - '+str(df.index[-1]))
# plt.show()