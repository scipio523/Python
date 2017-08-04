tot = 0
for num in xrange(0, 1001):
	for digit in str(num):
		tot += int(digit)

print tot