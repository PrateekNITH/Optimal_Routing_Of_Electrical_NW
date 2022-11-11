import numpy as np
import math
from sklearn_extra.cluster import KMedoids
from DataAcquisition import *
from layer2 import *

# optTrans = KMedoids(n_clusters=6).fit(cand_latlon)
# print(optTrans.cluster_centers_)
connectionPercentage=0
nmax = len(cand_latlon)
n=1
while connectionPercentage<99 and n < nmax:
    optTrans = KMedoids(n_clusters=n).fit(cand_latlon)
    # print(optTrans.cluster_centers_)
    connectionPercentage = secondlayer(optTrans, resi_lat, resi_lon)
    print("K = ",n)
    print("Connection Percentage = ", connectionPercentage)
    n+=1

# print("SUCCESSFULLY CONNECTED...")
# print("Connection percentage: ", connectionPercentage)
