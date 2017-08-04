import numpy as np
import matplotlib.pyplot as plt

data = []
Avgs = []
Maxes = []

for month in range(10):
	for day in range(10):
		for stock in range(100):
			data.append(np.random.uniform())
		Maxes.append(max(data)) # average max
	Avgs.append(np.mean(Maxes)) # max of an average

plt.hist(Maxes, bins=50, label='Avg Max')
plt.hist(Avgs, bins=50, label='Max of Avg')
plt.title('Max of Avg less volatile than Avg Max')
plt.legend()
plt.show()