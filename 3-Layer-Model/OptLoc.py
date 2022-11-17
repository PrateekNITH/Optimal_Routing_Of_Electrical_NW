#!/usr/bin/env python
# coding: utf-8

# In[143]:
from helpers import haversine;

from DataAcquisition import cand_latlon, resi_lat, resi_lon
import numpy as np
from sklearn.cluster  import KMeans
from random import sample
from math import inf, sqrt



def findNearest(curr_clusters, k):
    req = [0 for i in range(k)]
    for i in range(k):
        tmp = inf
        for j in range(len(cand_latlon)):
            # ########################################### IMP TO DISCUSS...
            dis = haversine(cand_latlon[j][1], cand_latlon[j][0], curr_clusters[i][1], curr_clusters[i][0]) # ERROR SUSPECTED, TO BE DISCUSSED
            if (dis < tmp):
                tmp = dis
                req[i] = cand_latlon[j]
    return req
87

# Define k for the number of transformers we want, get random sample from cand_lat_lon
# In[144]:

def singleIteration(k):
    residential = np.array([[resi_lat[i], resi_lon[i]] for i in range(len(resi_lat))])
    compute = KMeans(n_clusters = k, random_state=0)
    curr = compute.fit(residential)
    def findNearest(curr_clusters):
        req = [0 for i in range(k)]
        for i in range(k):
            tmp = inf
            for j in range(len(cand_latlon)):
                dis = distance(cand_latlon[j], curr_clusters[i])
                if (dis < tmp):
                    tmp = dis
                    req[i] = cand_latlon[j]
        return req
    tmp = findNearest(curr.cluster_centers_)    
    lat, lon = zip(*tmp)
    return lat, lon


def optimalLocationFinder(k):
    compute = KMeans(n_clusters = k, random_state=0)
    residential = np.array([[resi_lat[i], resi_lon[i]] for i in range(len(resi_lat))])
    extra = compute.fit(residential).cluster_centers_

    residential_cand_site = np.concatenate((residential, np.array(extra)))

    iters = 4
    for i in range(iters):
        curr_centers = compute.fit(residential_cand_site).cluster_centers_;
        curr_cand = findNearest(curr_centers, k)
        residential_cand_site[-k:] = np.array(curr_cand)
    cand_lat, cand_lon = zip(*curr_cand)
    return cand_lat, cand_lon
   

if __name__ == "__main__":
    print(f"the optimal location for k = 3 is {optimalLocationFinder(3)}")
