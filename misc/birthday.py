def birthday(n):
	result = 1.0
	days = 365.0
	for i in range(0, n):		
		result *= (days - i) / days		
	return (1-result)

print birthday(3)



