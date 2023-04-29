import random

N = 10
arr = []
for i in range(N*(N+1)):
	arr.append(random.randint(-N, N))

def render(a, n):
	for i in range(n):
		print(a[i*(n+1):(i+1)*(n+1)])
	print('-------------------')

def swapRow(a, n, r1, r2):
	for i in range(n+1):
		a[r1*(n+1) + i], a[r2*(n+1) + i] = a[r2*(n+1) + i], a[r1*(n+1) + i]
def swapCol(a, n, c1, c2):
	for i in range(n):
		a[i*(n+1) + c1], a[i*(n+1) + c2] = a[i*(n+1) + c2], a[i*(n+1) + c1]
# dir:
# '+' plus  row r by x
# '*' multiply row r by x
def oneRow(a, n, r, dir, x):
	if (dir == '+'):
		for i in range(n+1):
			a[r*(n+1) + i] += x;
	if (dir == '*'):
		for i in range(n+1):
			a[r*(n+1) + i] *= x;
	if (dir == '/'):
		for i in range(n+1):
			a[r*(n+1) + i] /= x;

# r1 <- k1*r1 + k2*r2
def twoRow(a, n, r1, r2, k1 = 1, k2 = 1):
	for i in range(n+1):
		a[r1*(n+1) + i] = k1*a[r1*(n+1) + i] + k2*a[r2*(n+1) + i]

def oneStepGauss(a, n, index):
	error = True
	if a[index*(n+1) + index] != 0:
		error = False
	else:
		for i in range(1+index, n):
			if a[i*(n+1) + index] != 0:
				swapRow(a, n, index, i)
				error = False
				break
	if a[index*(n+1) + index] != 0:
		oneRow(a, n, index, '/', a[index*(n+1) + index])
	else:
		error = True

	for i in range(1+index, n):
		twoRow(a, n, i, index, k2 = -a[i*(n+1) + index])
	return error
def oneStepGaussJordan(a, n, index):
	for i in range (index):
		twoRow(a, n, i, index, k2 = -a[i*(n+1) + index])
def solveSolution(a, n):
	result = []
	for i in range(n-1):
		if oneStepGauss(a, n, i):
			return False
		render(arr, n)
	if a[(n-1)*(n+1) + (n-1)] == 0:
		return False
	oneRow(a, n, n-1, '/', a[(n-1)*(n+1) + (n-1)])
	for i in range(n-1):
		oneStepGaussJordan(a, n, n-i-1)
		render(arr, n)
	for i in range(n):
		result.append(round(a[i*(n+1)+n], 2))
	return result
render(arr, N)
result = solveSolution(arr, N)
print(result)