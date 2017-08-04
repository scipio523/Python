import numpy as np
import matplotlib.pyplot as plt

results = []

for i in range(1, 60000 + 1):
	if '6' not in str(i): 
		results.append(i)
		print i

print 'total #s with no 6: ', len(results)
print 'probability: ', len(results) / 60000.
