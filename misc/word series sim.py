import numpy as np
import matplotlib.pyplot as plt
import random

runs = 10000
results = []
graph = []
for j in range(100):
	for i in range(runs):
		notDone = 0
		series = []
		while series.count(1) < 4 and series.count(0) < 4:
			if random.randint(0,1) == 0: series.append(0)
			else: series.append(1)
		results.append(len(series))
	graph.append(float(results.count(5)) / len(results))

plt.hist(graph, bins=30)
plt.show()