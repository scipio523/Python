#If we bet 1% of our initial capital with 51/49 % chance of doubling/losing stake each trade,
#what's the probability that we lose all our capital? Monte carlo simulation

import random
import numpy as np
import matplotlib.pyplot as plt
import math

trials = 1000000
bets = 100
betsize = .01
winProb = .60
results = []
pctDone = 0

for trial in range(trials):
	money=100
	for bet in range(bets):
		rand=random.random()
		if rand <= winProb: money *= (1 + betsize)
		else: money *= (1 - betsize)
	results.append(money)
	if float(trial) / float(trials) >= (pctDone + .01):
		pctDone = float(trial) / float(trials)
		print '%.i%% done...' % (pctDone * 100)
print 'Done.'

# print results
lossThreshold = .20
bust = sum(i < 100 * (1 - lossThreshold) for i in results)
winners = sum(i > 100 for i in results)
print '# of trials that lost over %i%%: %i' % (lossThreshold * 100., bust)
print '%% of trials that lost over %i%%: %.4f%%' % (lossThreshold * 100., (bust * 100. / trials))
print 'Avg ending money: $%.2f' % np.mean(results)
print 'Min ending money: $%.2f' % np.min(results)
print 'Max ending money: $%.2f' % np.max(results)
print 'Chance of making money: %.2f%%' % (winners * 100. / trials)

# plot histogram
f, ax1 = plt.subplots()
numBins = 100.
binwidth = (max(results) - min(results)) / numBins
ax1.hist(results, bins = range(int(min(results)), int(max(results) + binwidth), int(math.ceil(binwidth))))
ax1.set_title('Distribution Trials'' Ending Money')
ax1.set_xlabel('Ending Money')
ax1.set_ylabel('# of Trials')
plt.show()	


