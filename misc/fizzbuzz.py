# for i in range(1,101):
# 	if (i % 3 == 0) & (i % 5 == 0): result = 'fizzbuzz'
# 	elif i % 3 == 0: result = 'fizz'
# 	elif i % 5 == 0: result = 'buzz'
# 	else: result = i
#  	print result

# for i in range(1, 101):
# 	result = ''
# 	if i % 3 == 0: result = 'fizz'
# 	if i % 5 == 0: result += 'buzz'
# 	if result: print result 
# 	else: print i

print ['Fizz'*(i%3<1)+'Buzz'*(i%5<1) or i for i in range(1,101)]



