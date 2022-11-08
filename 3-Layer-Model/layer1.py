import numpy as np
import math
from sklearn_extra.cluster import KMedoids
from DataAcquisition import cand_latlon

optTrans = KMedoids(n_clusters=6).fit(cand_latlon)
print(optTrans.cluster_centers_)
