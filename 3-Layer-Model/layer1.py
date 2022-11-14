import numpy as np
import math
from sklearn_extra.cluster import KMedoids
from DataAcquisition import *
from layer2 import *
from OptLoc import optimalLocationFinder, singleIteration

# optTrans = KMedoids(n_clusters=6).fit(cand_latlon)
# print(optTrans.cluster_centers_)
connectionPercentage=0
nmax = len(cand_latlon)
print("Cand loc size",nmax)

n=1
while connectionPercentage<100 and n < nmax:
    optTrans = optimalLocationFinder(n);
    # optTrans = singleIteration(n);
    # print(optTrans.cluster_centers_)
    connectionPercentage = secondlayer(optTrans, resi_lat, resi_lon)
    print("K = ",n)
    print("Connection Percentage = ", connectionPercentage)
    n+=1

# print("SUCCESSFULLY CONNECTED...")
# print("Connection percentage: ", connectionPercentage)
print("53,54,55: ")
print(resi_lat[52]," ",resi_lon[52])
print(resi_lat[53]," ",resi_lon[53])
print(resi_lat[54]," ",resi_lon[54])