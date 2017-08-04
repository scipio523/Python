import pandas as pd
import numpy as np

num_days 	  = 1000
learning_rate = 0.01
discount_rate = 0.9
epsilon 	  = 0.9

""" Step 1: Define Actions/States/Rewards
Actions: buy, sell, nothing
States: adjusted close/SMA, Bollinger Band value,
	P/E ratio, holding stock, volatility (%), yesterday's return, 
	return since entry, USD index (up/down)
Reward: daily return
"""

# Load data
ohlc = pd.read_csv('SPY.csv')
ohlc = ohlc[len(ohlc)-num_days:]  # Get last n days

# Define actions, initialize Q table
actions = ['buy', 'sell', 'hold']
q_table = pd.DataFrame(columns=actions)

for episode in range(10):
	
	# Loop through adjusted close prices, ignoring the first
	for i, price in enumerate(ohlc['Adj Close']):
		if i == 0: 
			prev_price = price 
			continue

		#action = choose_action(state)
		#learn(state, action, reward, state_)

		# Reward is daily return
		reward = ((price / prev_price) - 1) * 100
		
		# Swap prices
		prev_price = price

def choose_action(state):
	# action selection
	if np.random.uniform() < epsilon:
		# choose best action
		state_action = q_table.ix[state, :]
		state_action = state_action.reindex(np.random.permutation(state_action.index))     # some actions have same value
		action = state_action.argmax()
	else:
		# choose random action
		action = np.random.choice(self.actions)
	return action	


def learn():
	return

""" Step 2: Discretization
Discretize each factor and discretized state
"""


""" Step 3: Train Q Learner
Choose in-sample training period and iteratively
update Q-table. Then backtest on in-sample data.
Repeat until model converges (stops improving).
"""


""" Step 4: Test model
Backtest on later data
"""

