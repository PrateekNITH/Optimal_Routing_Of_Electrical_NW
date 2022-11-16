import cv2
import numpy as np
from scipy.interpolate import interp1d
from bs4 import BeautifulSoup
with open('../Assets/chamba.osm', 'r') as f:
    data = f.read()
bso = BeautifulSoup(data, "xml")
tf = bso.find('bounds')
endLat = tf.get('maxlat')
startLat = tf.get('minlat')
endLon = tf.get('maxlon')
startLon = tf.get('minlon')
img = cv2.imread("../Assets/Chamba.png")
# print(startLat, endLat, startLon, endLon)
height = img.shape[0]
width = img.shape[1]
print(height, width)
latcon = interp1d([startLat,endLat],[0,height])
loncon = interp1d([startLon, endLon], [0, width])

# To start plotting according to given data


while True:
    cv2.imshow("Output",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # To Exit on pressing q
        break