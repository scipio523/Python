import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

user = 'dasei' 

symbols = ['NYSE_SPY','NASDAQ_SOXX','NYSE_VXX','AMEX_TLT','NYSE_IYR','NYSE_EWZ',
			'NYSE_FXI','NYSE_EWJ','NYSE_PIN','NYSE_RSX','NYSE_VGK','NYSE_GDXJ',
			'AMEX_GLD','NYSE_XOP','AMEX_EEM']

#load data into pandas dataframe
start = '2011-01-01'
end = '2017-01-03'
dates = pd.date_range(start, end)
df = pd.DataFrame(index=dates)
for symbol in symbols:
	filepath = 'C:/Users/'+user+'/OneDrive/Documents/Programs/Python/Quandl/data/'+symbol+'.txt'
	df_temp = pd.read_csv(filepath, index_col='Date',parse_dates=True, 
							usecols=['Date','Close'], na_values=['nan'])
	df_temp = df_temp.rename(columns={'Close': symbol})
	df = df.join(df_temp)

df = df.dropna()

corr = df.corr()

print corr

sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)
sns.plt.show()