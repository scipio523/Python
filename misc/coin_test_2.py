### We flip a coin 100 times - what is the probability of getting an even # of heads? ###

import random

trials = 10000
trialsList = []
flips = 2

for trial in range(trials):
	total = 0
	for flip in range(flips):
		if random.randint(1, 2) == 1: total += 1
	if total % 2 == 0: trialsList.append(1)
	else: trialsList.append(0)

print '%% of trials with even # of heads: %.4f' % (float(sum(trialsList)) / len(trialsList))