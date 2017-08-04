import random
import numpy as np
import matplotlib.pyplot as plt

trials = 100000
Alist = []
Blist = []

### basic scenario ###
# for trial in range(trials):
# 	rollA = random.randint(1, 30)
# 	rollB = random.randint(1, 20) 
# 	if rollA > rollB:  # A higher
# 		Alist.append(rollA)
# 		Blist.append(-rollA)
# 	else:   # B higher or draw
# 		Blist.append(rollB)
# 		Alist.append(-rollB)

### B reroll scenario ###
for trial in range(trials):
	rollA = random.randint(1, 3)
	rollB = random.randint(1, 2)
	if rollA > 2: 
		Alist.append(rollA)
		Blist.append(-rollA) 
	elif rollB >= rollA:
		Blist.append(rollB)
		Alist.append(-rollB)
	else:  # A rolled 1-20 and won, B rerolls
		reroll = random.randint(1, 2)
		if rollA > reroll:
			Alist.append(rollA)
			Blist.append(-rollA) 
		else:  # B wins ties
			Blist.append(reroll)
			Alist.append(-reroll)

print np.mean(Alist)