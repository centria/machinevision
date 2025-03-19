import cv2
import numpy as np

# Lataa kuvat
kuva1 = cv2.imread('panorama1.jpg')
kuva2 = cv2.imread('panorama2.jpg')

# Luo Stitcher-objekti
stitcher = cv2.Stitcher_create()

# Yhdistä kuvat
(status, panoraama) = stitcher.stitch([kuva1, kuva2])

# Tarkista, onnistuiko yhdistäminen
if status == cv2.Stitcher_OK:
    cv2.imshow('Panoraama', panoraama)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print('Kuvien yhdistäminen epäonnistui')