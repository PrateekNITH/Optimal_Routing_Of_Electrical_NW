import cv2
import numpy as np
from scipy.interpolate import interp1d
from bs4 import BeautifulSoup
from DataAcquisition import resi_lat, resi_lon, cand_latlon
from helpers import INF

with open('../Assets/chamba.osm', 'r') as f:
    data = f.read()
bso = BeautifulSoup(data, "xml")
tf = bso.find('bounds')
# found starting and ending locations
endLat, startLat, endLon, startLon = map(float, (tf.get("maxlat"), tf.get("minlat"), tf.get("maxlon"), tf.get("minlon")))
global img, drawColor, brushThickness, N
img = cv2.imread("../Assets/Chamba.png")
# print(startLat, endLat, startLon, endLon)
height = img.shape[0]
width = img.shape[1]
print(height, width)
latcon = interp1d([startLat,endLat],[0,height])
loncon = interp1d([startLon, endLon], [0, width])
img = cv2.flip(img, 0)
drawColor = (255,0,0)
brushThickness = 2
N = len(resi_lat)


def plotting(active_nodes, connections, lvconnections):
    '''
        Plotting: everything
    '''
    print(active_nodes)
    # converting lat and lon in pixel values
    global img, drawColor, brushThickness, N
    a = latcon(resi_lat)
    b = loncon(resi_lon)
    t_lat, t_lon = zip(*cand_latlon)
    # print(t_lat)
    c = latcon(t_lat)
    d = loncon(t_lon)
    M = len(active_nodes)
    # plotting residential areas
    for i in range(len(resi_lat)):
        x1 = int(a[i])
        y1 = int(b[i])
        # print(x1,y1, a[i], b[i])
        cv2.circle(img, (y1, x1), brushThickness//2, drawColor, cv2.FILLED)
    drawColor = (100, 0, 0)
    # LV Connections
    for i in range(N):
        # print(lvconnections[i])
        for j in range(i, N+M):
            if lvconnections[i][j]<INF and lvconnections[i][j]>0:
                # plot between i and j
                x1 = int(a[i])
                y1 = int(b[i])
                if j<N:
                    x2 = int(a[j])
                    y2 = int(b[j])
                    cv2.line(img, (y2, x2), (y1, x1), drawColor, brushThickness)
                else:
                    x2 = int(c[active_nodes[j-N]])
                    y2 = int(d[active_nodes[j-N]])
                    cv2.line(img, (y2, x2), (y1, x1), drawColor, brushThickness)



    img = cv2.flip(img, 0)
    while True:
        
        cv2.imshow("Output",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # To Exit on pressing q
            break

# cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
# cv2.circle(img, (x1, y1), int(brushThickness/2), drawColor, cv2.FILLED)

# To start plotting according to given data

if __name__ == "__main__":
    print(type(startLat))
    # print(startLat) 
    t_lat, t_lon = zip(*cand_latlon)
    # for i in t_lat:
    #     if i > endLat:
    #         print("Print fat gaya t_lat endLat ", i)
    #     if i < startLat:
    #         print("Print fat gaya t_lat startLat ", i)
    # print("-------*---------")
    # for i in t_lon:
    #     if i > endLon:
    #         print("Print fat gaya t_lon endLon ", i)
    #     if i < startLon:
    #         print("Print fat gaya t_lat startlon ", i)