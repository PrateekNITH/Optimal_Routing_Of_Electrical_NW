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
# print(startLat, endLat, startLon, endLon)

latcon = interp1d([startLat,endLat],[0,height])
loncon = interp1d([startLon, endLon], [0, width])
img = cv2.imread("../Assets/Chamba.png")



while True:
    cv2.imshow("Output",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # To Exit on pressing q
        break