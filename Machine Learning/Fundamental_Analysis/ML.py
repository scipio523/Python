import numpy as np
from sklearn import svm, preprocessing
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

features = ['Total Debt/Equity',
			'Trailing P/E',
			'Price/Sales',
			'Price/Book',
			'Profit Margin',
			'Operating Margin',
			'Return on Assets',
			'Return on Equity',
			'Revenue Per Share',
			'Market Cap',
			'Enterprise Value',
			'Forward P/E',
			'PEG Ratio',
			'Enterprise Value/Revenue',
			'Enterprise Value/EBITDA',
			'Revenue',
			'Gross Profit',
			'EBITDA',
			'Net Income Avl to Common ',
			'Diluted EPS',
			'Earnings Growth',
			'Revenue Growth',
			'Total Cash',
			'Total Cash Per Share',
			'Total Debt',
			'Current Ratio',
			'Book Value Per Share',
			'Cash Flow',
			'Beta',
			'Held by Insiders',
			'Held by Institutions',
			'Shares Short (as of',
			'Short Ratio',
			'Short % of Float',
			'Shares Short (prior ']

def Build_Data_Set():
	data_df = pd.DataFrame.from_csv('key_stats_acc_perf_WITH_NA.csv')
	data_df = data_df.replace('NaN', 0).replace('N/A', 0)
	#data_df.fillna(0, inplace=True)

	X = np.array(data_df[features].values)
	X = preprocessing.scale(X)

	y = (data_df['Status'].replace('underperform', 0).replace('outperform', 1).values.tolist())

	return X, y

def Analysis():

	X, y = Build_Data_Set()
	test_size = 1500 / len(y)
	X_train, X_test, y_train, y_test = train_test_split(X,
														y, 
														test_size = test_size, 
														random_state = 0)

	clf = svm.SVC(kernel = 'linear', C = 1.0)
	clf.fit(X_train, y_train)

	print('Accuracy of RF classifier on training set: {:.2f}'
     .format(clf.score(X_train, y_train)))
	print('Accuracy of RF classifier on test set: {:.2f}'
     .format(clf.score(X_test, y_test)))

Analysis()