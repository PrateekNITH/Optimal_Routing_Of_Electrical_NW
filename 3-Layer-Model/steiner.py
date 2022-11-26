import networkx as nx

from networkx.algorithms.approximation.steinertree import steiner_tree
import sys
from DataAcquisition import mat, cand_latlon
import numpy as np
from helpers import haversine
import matplotlib.pyplot as plt

# temp = nx.Graph()
def modified_prim(nodemat):
    nodemat.sort()
    st_n = len(mat)
    for i in range(st_n):
        for j in range(st_n):
            if mat[i][j] == 1:
                st_temp = haversine(
                    cand_latlon[j][1],
                    cand_latlon[j][0],
                    cand_latlon[i][1],
                    cand_latlon[i][0],
                )
                mat[i][j] = st_temp
                mat[j][i] = st_temp

    np.set_printoptions(threshold=sys.maxsize)
    # print(A.shape)
    A = np.array(mat)
    # print(A)
    temp = nx.from_numpy_matrix(A)
    # print(temp.nodes)
    # print(nodemat)
    # B = nx.adjacency_matrix(temp)
    # print(B.todense())
    # print(list(temp.edges))
    G = nx.Graph()
    G = steiner_tree(temp, nodemat)
    # print(list(temp.edges))
    plt.figure()
    nx.draw_networkx(G)
    plt.show()


if __name__ == "__main__":
    modified_prim([0])
