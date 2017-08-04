import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from sklearn import cross_validation

boston = load_boston()
bos = pd.DataFrame(boston.data)  # convert to pandas dataframe
bos.columns = boston.feature_names

# dependent variable
bos['Price'] = boston.target

# independent variables
X = bos.drop('Price', axis = 1)

# create linear model
lm = LinearRegression()
lm.fit(X, bos.Price)

# pair independent variables with estimated coefficients
model = pd.DataFrame(zip(X.columns, lm.coef_), columns = ['features', 'estimatedCoefficients'])

# calculate predicted prices
pred = lm.predict(X)

# scatterplot comparing true to predicted prices
f, (ax1, ax2) = plt.subplots(2)
plt.subplots_adjust(hspace = 0.5)
ax1.scatter(bos.Price, pred)
ax1.set_title("Prices vs Predicted Prices: $Y_i$ vs $\hat{Y}_i$")
ax1.set_xlabel("Prices: $Y_$i$")
ax1.set_ylabel("Predicted prices: $\hat{Y}_i$")

# calculate mean squared error
mseFull = np.mean((bos.Price - pred) ** 2)
# print 'Mean squared error: %.4f' % mseFull

# create randomly generated train and test sets
X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(
	X, bos.Price, test_size=0.33, random_state = 2)

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
ax2.hlines(y = 0, xmin = 0, xmax = 50)
ax2.set_title('Residual plot using training (blue) and test (green) data')
ax2.set_ylabel('Residuals')

plt.show()