import numpy as np
import math
from sklearn_extra.cluster import KMedoids
from DataAcquisition import *
from layer2 import secondlayer
from OptLoc import optimalLocationFinder, singleIteration
from helpers import *

# optTrans = KMedoids(n_clusters=6).fit(cand_latlon)
# print(optTrans.cluster_centers_)
optTrans = []
connectionPercentage=0
nmax = len(cand_latlon)
print("Cand loc size",nmax)
N=len(resi_lat)
n=1
conNodes = 0
rval = []
tuner = []
while connectionPercentage<95 and n < nmax:
    optTrans = optimalLocationFinder(n);
    # optTrans = singleIteration(n);
    # print(optTrans.cluster_centers_)
    conNodes, rval = secondlayer(optTrans, resi_lat, resi_lon)
    connectionPercentage = conNodes*100/N
    print("K = ",n)
    print("Connection Percentage = ", connectionPercentage)
    print("Connection: ", rval)
    n+=1
def dhruvCode():
    print("DHRUV SHOULD ADD HIS CODE")
    # DHRUV SHOULD ADD HIS CODE HERE

def finalsteps(tuner, k):
    tem = KMedoids(n_clusters=k).fit(tuner)
    t = tem.cluster_centers_
    lat, lon = zip(*t)
    return lat, lon
if connectionPercentage==100:
    dhruvCode()
else:
    print("IMPROVING EFFICIENCY (Fast Mode)...")
    
    for i in range(N):
        if rval[i]==0:
            # finding nearest transformer
            print(resi_lat[i], resi_lon[i])
            tmp = INF
            req = ()
            for j in range(nmax):
                # distn = pow((cand_latlon[j][1]-resi_lon[i]), 2)+pow((cand_latlon[j][0]-resi_lat[i]), 2)
                distn = haversine(cand_latlon[j][1], cand_latlon[j][0], resi_lon[i], resi_lat[i])
                if distn<tmp:
                    tmp = distn
                    req = cand_latlon[j]
            # checking if not in tuner
            flag=0
            for x in tuner:
                if x==req:
                    flag=1
            if flag==0:
                tuner.append(req)
            
        
    transloc = ()
    transloc = transloc+optTrans
    k=0
    print("tuner: ", tuner)
    # print(transloc)
    # print(optTrans)
    while k<len(tuner) and connectionPercentage<100:
        k+=1
        extloc = finalsteps(tuner, k)
        t1 = transloc[0]+extloc[0]
        t2 = transloc[1]+extloc[1]
        transloc = t1, t2
        print(transloc)
        conNodes, rval = secondlayer(transloc, resi_lat, resi_lon)
        connectionPercentage = conNodes*100/N
        print("K = ", n+k-1)
        print("Connection Percentage = ", connectionPercentage)
    print("Maximum Possible Connection Percentage Reached...")
    dhruvCode()
    if connectionPercentage<100:
        print("Try increasing the range constraint of LV connection...")

