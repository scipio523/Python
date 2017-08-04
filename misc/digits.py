import matplotlib.pyplot as plt 

results = []
for i in range(1, 10000):
    tot = 0
    for digit in str(i):
        tot += int(digit)
    if tot == 12: results.append(tot)

print(len(results))
print(100 * len(results) / 9999.)
