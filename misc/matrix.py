import math

def counterclockwise(matrix):
	n = len(matrix)
	result = ""

	for i in range(0, int(math.ceil(n/2))):

		for j in range(n-1-i, i-1, -1):
			result += matrix[i][j]		

		for j in range(i+1, n-i):
			result += matrix[j][i]

		result += matrix[n-1-i][i+1:n-i] 

		for j in range(n-2-i, i, -1):
			result += matrix[j][n-1-i]

	return result

matrix = ["CIPE","RNKU","UOWO","LESY"]

print counterclockwise(matrix)


