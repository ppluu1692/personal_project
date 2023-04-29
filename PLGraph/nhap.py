# from math import *
# import operator, random
# def getUnit(scale, standard=200):
# 	exponent = math.floor(math.log10(standard/scale))
# 	mantissa = (standard/scale)/(10**exponent)
# 	if mantissa < 2:
# 		return 10**exponent
# 	elif mantissa < 5:
# 		return 2*10**exponent
# 	else:
# 		return 5*10**exponent
# # for scale in range(1, 100):
# # 	print(scale,getUnit(scale), getUnit(scale)*scale)

# # for i in range(0, 10, 2):
# # 	print(i)

# a = [1, 2,3 ]

# print(log(0))
# importing the required modules
import numpy as np
  
# setting the x - coordinates
x = np.arange(0, 2*(np.pi), 0.1)
# setting the corresponding y - coordinates
y = 1/x

print(x)
print('------------')
print(y)