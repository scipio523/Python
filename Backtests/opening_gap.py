import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

user = 'dasei' 
filename = 'JNUG'
filepath = 'C:/Users/dasei/OneDrive/Documents/Programs/Python/Google_Data/data/'+filename+'.txt'

#parameters for holding period
increment = 1
holdmax = 10

#load data into pandas dataframe
df = pd.read_csv(filepath)

#set index to the datetime column
df.set_index('Datetime', inplace=True)

#calculate returns
df['OC'] = df['Open'] / df['Close'].shift(1) - 1

#mark opening gaps > or < 4%
threshhold = .04
df['Gap'] = np.where(df['OC'] > threshhold, 1, 0)
df['Gap'] = np.where(df['OC'] < -threshhold, -1, df['Gap'])

#returns of 1st bar after gap
df['Ret'] = np.where(df['Gap'] == 1, df['Close'] / df['Open'] - 1, 0)
df['Ret'] = np.where(df['Gap'] == -1, -(df['Close'] / df['Open'] - 1), df['Ret'])

#plot
df['Ret'].plot()
plt.show()