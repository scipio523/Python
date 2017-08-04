import random
import numpy as np
import matplotlib.pyplot as plt

results = []
rollsList = []

for j in range(1000):
	for trial in range(100):
		sequence = []
		for i in range(3):
			roll = random.randint(1, 6) 
			sequence.append(roll)
		if np.prod(sequence) % 2 == 0: rollsList.append(0)
		else: rollsList.append(1)
	results.append(np.mean(rollsList))

print np.mean(results)

plt.hist(results, bins=50)
plt.show()

