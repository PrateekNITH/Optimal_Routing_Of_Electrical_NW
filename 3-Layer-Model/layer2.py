from helpers import *
from DataAcquisition import *
from layer1 import *
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
INF = 99999999
# Optimal Routing of a LV Grid Network
# N -> no. of residential customers
# M -> no. of LV transformers
# S -> no. of substations
# Step 1

# p, distN, X, Y, Cap, R
# TO get from frontend
N = len(resi_lat)
print("N: ", N)
M = len(optTrans.cluster_centers_)
S = 1
P=N+M
X=resi_lon
Y=resi_lat
t_lon = list(optTrans.cluster_centers_[:,1])

t_lat = list(optTrans.cluster_centers_[:,0])
X.extend(t_lon)
Y.extend(t_lat)

# Step 2
# dist -> 2D array
dist = [[0 for x in range(P)] for y in range(P)]
G = [[0 for x in range(P)] for y in range(P)]
# ############################## Make G (P X P connectivity matrix) ###################################################
for i in range(N+M):
    for j in range(N+M):
        if i >= N and j >= N:
             G[i][j] = INF
        elif i != j:
            dist[i][j] = haversine(X[i], Y[i], X[j], Y[j])
            if dist[i][j] <= R:
                 G[i][j] = dist[i][j]
            else:
                 G[i][j] = INF
        else: # i == j
            dist[i][j] = 0
            G[i][j] = 0



# for i in range(P):
#      print(G[i])
# Step 3
# t = haversine(77.2878, 28.4452, 77.3092, 28.4270)
# print(t)
# Gr = [[0, 19, 5, INF, INF],
#      [19, 0, 5, 9, 2],
#      [5, 5, 0, 1, 6],
#      [INF, 9, 1, 0, 1],
#      [INF, 2, 6, 1, 0]]
# graph = Graph(P)
# graph.add_edge(1,2,5)
# graph.add_edge(2,3,5)
# graph.add_edge(3,4,4)
# graph.add_edge(0,4,5)
# graph.add_edge(3,2,5)
# graph.add_edge(1,4,5)
# graph.edges = G
min_dist_list = []

# ####################################### Apply Dijkstra ##############################################################
# pred = dijkstra(G, P)
# P-> total number of subscribers including N, M and S
minidx_lst = []
for i in range(N):
     mini = INF
     minidx = 0
     temp = Graph(P)
     temp.edges = G
     d = dijkstra(temp, i)
     for j in range(N,N+M):
          if d.get(j)<mini:
               mini = d.get(j)
               minidx = j
     minidx_lst.append(minidx)

     min_dist_list.append(d)

# print(min_dist_list)     # min_dist_list is the dictionary of every customer's djikstra output
print(minidx_lst)

# g = Graph(5)
# g.edges = Gr
# ##################################### MINIMUM SPANNING TREE #########################################################

# Gra = csr_matrix(G)
# T = minimum_spanning_tree(Gra)
# lis = T.toarray().astype(int)
# print(lis)
cost = 0
# ######################################### Optimal Routing LV Grid ##################################################
for i in range(N, N+M):
    temporary = [[0 for x in range(P)] for y in range(P)]
    for j in range(P):
        for k in range(P):
            temporary[j][k] = G[j][k]
    for j in range(N):
        if minidx_lst[j] != i:
            for k in range(P):
                temporary[j][k] = INF
                temporary[k][j] = INF
    for j in range(N, N+M):
        if j != i:
            for k in range(N+M):
                temporary[j][k] = INF
                temporary[k][j] = INF
    Gra = csr_matrix(temporary)
    T = minimum_spanning_tree(Gra)
    print(T)
    lis = T.toarray().astype(int)
    # print(lis)
    print('\n')
    # ################################################### COST CALCULATION AND OUTPUT ################################################
    for j in range(P):
        for k in range(P):
            if j<k and lis[j][k]<INF and lis[j][k]>0:
                cost += lis[j][k]
print("Amount of LV Connection: ")
print(cost, "M")

# for Trans = 1 : N do
#   X = [Xnp(Pred)XTrans];
#   Y = [Ynp(Pred)YTrans];
#   disti,j = haversine(X, Y);
#   G(disti,j <= R) 1;
#   path primmst(sparse(G));
# EndFor

# Step 5: - Determine the final cost of LV

# for i ! 1 : length(X) do
#     for j ! 1 : length(X) do
#         costLV = costLV + disti,j(path);
#     EndFor
#
