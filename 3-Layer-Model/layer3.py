import numpy as np
import math
import random
from sklearn_extra.cluster import KMedoids


n = 50
# print(n)
# a = np.array([1,2,3,4,5,6,7,8,9,10])
# // Step 1
a = np.random.uniform(10, 90, (1, n))

# b = np.array([1,2,3,4,5,6,7,8,9,10])
b = np.random.uniform(10, 90, (1, n))
b, a = b.flatten(), a.flatten()


arr = np.zeros(shape=(n, 2))
# // Step 2
for i in range(n):
    # c = a[i]
    # d = b[i]
    arr[i] = [a[i], b[i]]

# print(arr)

row = a.shape
c = math.floor(row[0] * 0.1)
print("C =", c)

# // Step 3
KMobj = KMedoids(n_clusters=2).fit(arr)
print(KMobj)