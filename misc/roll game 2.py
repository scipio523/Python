import random
import numpy as np
import matplotlib.pyplot as plt

total = 0
trials = 10000

for trial in range(trials):
	rollA = random.randint(1, 10)
	rollB = random.randint(1, 20)

	if rollA > rollB:
		total += 1

print float(total) / trials