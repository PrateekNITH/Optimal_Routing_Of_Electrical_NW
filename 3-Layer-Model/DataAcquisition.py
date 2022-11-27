import osmium as osm
import pandas as pd
from bs4 import BeautifulSoup
####################### AKSHAT #####################################

with open('../Assets/chamba.osm', 'r') as f:
    data = f.read()
bso = BeautifulSoup(data, "xml")
tf = bso.find('bounds')
# found starting and ending locations
endLat = float(tf.get('maxlat'))
startLat = float(tf.get('minlat'))
endLon = float(tf.get('maxlon'))
startLon = float(tf.get('minlon'))


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
            if tag.k == "building" and (tag.v == "yes" or tag.v == "residential"):
                nd = []
                for n in elem.nodes:
                    nd.append(n.ref)
                self.i.append(nd)
            # Highway
            if tag.k == "highway":
                rd = []
                # print(elem.nodes)
                for n in elem.nodes:
                    # append ref in set
                    # set.add()
                    for lis in self.node_data:
                        if lis[0] == n.ref:
                            lat = lis[1]
                            lon = lis[2]
                            if lat>startLat and lat<endLat and lon>startLon and lon<endLon:
                                self.streets[n.ref] = (lat, lon)
                    if lat>startLat and lat<endLat and lon>startLon and lon<endLon:
                        rd.append(n.ref)
                self.cand_loc.append(rd)

    def node(self, n):
        self.node_data.append((n.id, n.location.lat, n.location.lon))
        # self.tag_inventory(n, "node")

    def way(self, w):
        self.tag_inventory(w, "way")
        # print(w.nd)

    # def relation(self, r):
    #     self.tag_inventory(r, "relation")


oh = OSMHandler()

oh.apply_file("../Assets/chamba.osm")

node_colnames = ["id", "latitude", "longitude"]
df_node = pd.DataFrame(oh.node_data, columns=node_colnames)

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
        lat += df_node["latitude"].where(df_node["id"] == y).dropna().tolist()[0]
        lon += df_node["longitude"].where(df_node["id"] == y).dropna().tolist()[0]
        idx = idx + 1
    lat = lat / idx
    lon = lon / idx
    resi_lat.append(round(lat, 6))
    resi_lon.append(round(lon, 6))

# print(resi_lat)
# print(resi_lon)


# Highway graph building
# oh.streets -> hash_map: (id): (lat, lon)
# cand loc -> list: connections

tmpmap = {}
cnt = 0
for i in oh.streets:
    tmpmap[i] = cnt
    cnt += 1

mat = [[0 for i in range(len(oh.streets))] for j in range(len(oh.streets))]

for lists in oh.cand_loc:
    if(len(lists)>0):
        for i in range(len(lists) - 1):
            a, b = tmpmap[lists[i]], tmpmap[lists[i + 1]]
            mat[a][b] = 1
            mat[b][a] = 1


cand_latlon = list(oh.streets[i] for i in tmpmap)


# cand_latlon = possible transformer location latitute and longitude - list of tuples
# mat = adjacency matrix - int[][]
# resi_lat, resi_lon = residential latitude and longitude - lists
if __name__ == "__main__":
    print("Residential Lats: ")
    print(resi_lat)
    print("Residential Longs: ")
    print(resi_lon)
    print("Candidate Data: ")
    print(cand_latlon)
    print("Adjacency Matrix: ")
    print(mat)
