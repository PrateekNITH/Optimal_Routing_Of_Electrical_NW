from helpers import *
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
def secondlayer(optTrans, resi_lat, resi_lon):
    N = len(resi_lat)
    print("N: ", N)
    M = len(optTrans.cluster_centers_)
    S = 1
    P=N+M
    X=[]
    Y=[]
    X.extend(resi_lon)
    Y.extend(resi_lat)
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
                dist[i][j] = round(haversine(X[i], Y[i], X[j], Y[j]), 3)
                if dist[i][j] <= R:
                    G[i][j] = dist[i][j]
                else:
                    G[i][j] = INF
            else: # i == j
                dist[i][j] = 0
                G[i][j] = 0


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
    # ##################################### MINIMUM SPANNING TREE #########################################################

    cost = 0
    cp=0 # Connection Percentage
    connectedNodes=0
    con = [0 for x in range(P)]
    # ######################################### Optimal Routing LV Grid ##################################################
    for i in range(N, N+M):
        # print("\n",i,"\n")
        temporary = [[0 for x in range(P)] for y in range(P)]
        for j in range(P):
            for k in range(P):
                temporary[j][k] = G[j][k]
        for j in range(N):
            if minidx_lst[j] != i:
                for k in range(P):
                    temporary[j][k] = 0
                    temporary[k][j] = 0
        for j in range(N, N+M):
            if j != i:
                for k in range(N+M):
                    temporary[j][k] = 0
                    temporary[k][j] = 0
        Gra = csr_matrix(temporary)
        T = minimum_spanning_tree(Gra)
        print(T)
        lis = T.toarray().astype(int)
        # print('\n')
        # ################################################### COST CALCULATION AND OUTPUT ################################################
        for j in range(N+M):
            for k in range(N+M):
                if lis[j][k]<INF and lis[j][k]>0:
                    cost += lis[j][k]
           
        for j in range(N+M):
            for k in range(N+M):
                if lis[j][k]<INF and lis[j][k]>0:
                    if con[j]==0 and j<N:
                        connectedNodes+=1
                        con[j]=1
                    if con[k]==0 and k<N:
                        connectedNodes+=1
                        con[k]=1

    print("Amount of LV Connection: ")
    print(cost, "M")
    # ############################# Calculate connection percentage and return it #############
    # print(con)
    cp = connectedNodes*100/N
    return cp


