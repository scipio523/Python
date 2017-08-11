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
    data_df = pd.DataFrame.from_csv('key_stats_acc_perf_NO_NA.csv')
    data_df.fillna(0, inplace=True)

    X = np.array(data_df[features].values)
    X = preprocessing.scale(X)

    y = np.array((data_df['Status'].replace('underperform', 0).replace('outperform', 1).values))#.tolist())

    Z = np.array(data_df[['stock_p_change', 'sp500_p_change']])

    return X, y, Z        

def Analysis():

    test_size = 1000
    invest_amount = 1000
    total_trades = 0
    if_market = 0
    if_strat = 0    

    X, y, Z = Build_Data_Set()

    X_train, X_test, y_train, y_test = train_test_split(X,
														y, 
														test_size = test_size / len(y), 
														random_state = 0)

    clf = svm.SVC(kernel = 'linear', C = 1.0)
    clf.fit(X_train, y_train)

    # Calculate performance
    for x in range(1, test_size + 1):
        if clf.predict(X[-x])[0] == 1:
            invest_return = invest_amount + (invest_amount * (Z[-x][0] / 100))
            market_return = invest_amount + (invest_amount * (Z[-x][1] / 100))
            total_trades += 1
            if_market += market_return
            if_strat += invest_return

    print('# observations:', len(X))
    print('Accuracy of RF classifier on training set: {:.2f}'
        .format(clf.score(X_train, y_train)))
    print('Accuracy of RF classifier on test set: {:.2f}'
        .format(clf.score(X_test, y_test)))
    print('Total Trades:', total_trades)
    print('Ending with Strategy: $' + str(if_strat))
    print('Ending with Market: $' + str(if_market))

    compared = 100 * (if_strat - if_market) / if_market
    do_nothing = total_trades * invest_amount

    avg_market = 100 * (if_market - do_nothing) / do_nothing
    avg_strat = 100 * (if_strat - do_nothing) / do_nothing

    print('Compared to market, we earn', str(round(compared, 2)) + '% more')
    print('Average strat return:', str(round(avg_strat, 2)) + '%')
    print('Average market return:', str(round(avg_market, 2)) + '%')

Analysis()