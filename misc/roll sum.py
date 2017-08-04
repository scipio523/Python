import random
import numpy as np
import matplotlib.pyplot as plt

results = []

for trial in range(10000):
	rollsList = []
	while sum(rollsList) < 300:
		roll = random.randint(1, 30) 
		rollsList.append(roll)
	results.append(sum(rollsList))

print np.mean(results)

plt.hist(results, bins=30)
#plt.show()
