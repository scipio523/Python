import random
import numpy as np

trials = 10000
trialsList = []

for trial in range(trials):
	sequence = []
	flipCount = 0
	while sequence != [1,1,1]:
		flip = random.randint(1, 2) # heads 1, tails 2
		sequence.append(flip)
		if len(sequence) > 3: sequence.pop(0)
		flipCount += 1
	trialsList.append(flipCount)

print('Average flips to get 3 heads in a row: %.4f' % np.mean(trialsList))