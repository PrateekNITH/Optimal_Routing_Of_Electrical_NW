# # Everything to get from frontend
# N = 10  # No of users
# M = 5  # No of Transformers
# S = 1  # No of Substations

# P = N + M + S

# # JUST FOR TESTING PURPOSE
# X = [x for x in range(P)]  # Longitude matrix
# Y = [x for x in range(P)]  # Latitude Matrix
# R = 9999999999  # Range of LV connections


########################################## AKSHAT #############################

# from pyrosm import OSM
# from pyrosm import get_data

# # Pyrosm comes with a couple of test datasets 
# # that can be used straight away without
# # downloading anything
# fp = get_data("test_pbf")

# # Initialize the OSM parser object
# osm = OSM(fp)

# # Read all drivable roads
# # =======================
# drive_net = osm.get_network(network_type="driving")
# drive_net.plot()

######################################### RISHIKA ##########################
import osmium as osm
import pandas as pd

# class OSMHandler(osm.SimpleHandler):
#     def __init__(self):
#         osm.SimpleHandler.__init__(self)
#         self.osm_data = []
#         self.node_data = []
#         self.i = []
#     def tag_inventory(self, elem, elem_type):
#         # if self.i == 0 and elem_type=="way":
#         #     print(dir(elem))
#         #     self.i = 1
#         for tag in elem.tags:
#             if tag.k=="building" and (tag.v=="yes" or tag.v=="residential"):
#                 self.osm_data.append([elem_type, 
#                                     elem.id, 
#                                     elem.version,
#                                     elem.visible,
#                                     pd.Timestamp(elem.timestamp),
#                                     elem.uid,
#                                     elem.user,
#                                     elem.changeset,
#                                     len(elem.tags),
#                                     tag.k, 
#                                     tag.v])
#                 nd = []
#                 for n in elem.nodes:
#                     nd.append(n.ref)
#                 self.i.append(nd)
                

#     def node(self, n):
#         self.node_data.append([n.id, n.location.lat, n.location.lon])
#         self.tag_inventory(n, "node")

#     def way(self, w):
#         self.tag_inventory(w, "way")
#         # print(w.nd)

#     def relation(self, r):
#         self.tag_inventory(r, "relation")


# oh = OSMHandler()
# oh.apply_file("chamba.osm")

# data_colnames = ['type', 'id', 'version', 'visible', 'ts', 'uid',
#                  'user', 'chgset', 'ntags', 'tagkey', 'tagvalue']
# df_osm = pd.DataFrame(oh.osm_data, columns=data_colnames)
# node_colnames = ['id', 'latitude', 'longitude']
# df_node = pd.DataFrame(oh.node_data, columns = node_colnames)

# # print(df_node)
# # print(df_osm)
# resi_lat = []
# resi_lon = []
# for x in oh.i:
#     lat = 0
#     lon = 0
#     idx = 0
#     for y in x:
#         # print(df_node['latitude'].where(df_node['id']==y).dropna())
#         lat += df_node['latitude'].where(df_node['id']==y).dropna().tolist()[0]
#         lon += df_node['longitude'].where(df_node['id']==y).dropna().tolist()[0]
#         idx = idx+1
#     lat = lat/idx
#     lon = lon/idx
#     resi_lat.append(round(lat,6))
#     resi_lon.append(round(lon,6))

# print(resi_lat)
# print(resi_lon)



####################### AKSHAT #####################################
class OSMHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.osm_data = []
        self.node_data = []
        self.i = []
        self.cand_loc = []
        # declare dict
        self.streets = dict()
    def tag_inventory(self, elem, elem_type):
        # if self.i == 0 and elem_type=="way":
        #     print(dir(elem))
        #     self.i = 1
        for tag in elem.tags:
            if tag.k=="building" and (tag.v=="yes" or tag.v=="residential"):
                nd = []
                for n in elem.nodes:
                    nd.append(n.ref)
                self.i.append(nd)
            # Highway
            if tag.k=="highway":
                rd = []
                # print(elem.nodes)
                for n in elem.nodes:
                    # append ref in set
                    # set.add()
                    for lis in self.node_data:
                        if lis[0]==n.ref:
                            lat = lis[1]
                            lon = lis[2]
                            self.streets[n.ref] = (lat, lon)
                    rd.append(n.ref)
                self.cand_loc.append(rd)
            
                

    def node(self, n):
        self.node_data.append((n.id, n.location.lat, n.location.lon))
        self.tag_inventory(n, "node")

    def way(self, w):
        self.tag_inventory(w, "way")
        # print(w.nd)

    def relation(self, r):
        self.tag_inventory(r, "relation")


oh = OSMHandler()
oh.apply_file("Assets/chamba.osm")

node_colnames = ['id', 'latitude', 'longitude']
df_node = pd.DataFrame(oh.node_data, columns = node_colnames)

# print(df_node)
# print(df_osm)
resi_lat = []
resi_lon = []
for x in oh.i:
    lat = 0
    lon = 0
    idx = 0
    for y in x:
        # print(df_node['latitude'].where(df_node['id']==y).dropna())
        lat += df_node['latitude'].where(df_node['id']==y).dropna().tolist()[0]
        lon += df_node['longitude'].where(df_node['id']==y).dropna().tolist()[0]
        idx = idx+1
    lat = lat/idx
    lon = lon/idx
    resi_lat.append(round(lat,6))
    resi_lon.append(round(lon,6))

# print(resi_lat)
# print(resi_lon)
for x in oh.streets:
    print(x, oh.streets[x])

print(oh.cand_loc)

# Highway graph building
# oh.streets -> hash_map: (id): (lat, lon)
# cand loc -> list: connections

tmpmap = {}
cnt = 0
for i in oh.streets:
    tmpmap[i] = cnt
    cnt+=1

mat = [[0 for i in range(len(oh.streets))] for j in range(len(oh.streets))]

for lists in oh.cand_loc:
    for i in range(len(lists)-1):
        a, b = tmpmap[lists[i]], tmpmap[lists[i+1]]
        mat[a][b] = 1
        mat[b][a] = 1

for x in mat:
    print(x)

cand_latlon = list(oh.streets[i] for i in tmpmap)
print(cand_latlon)


# cand_latlon = possible transformer location latitute and longitude - list of tuples
# mat = adjacency matrix - int[][]
# resi_lat, resi_lon = residential latitude and longitude - lists
