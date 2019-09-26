import cv2
import numpy as np

img = cv2.imread('others/test.png', 0)
f = np.fft.fft2(img)
col, row = f.shape[:2]
A = np.zeros((row, col))

for i in range(row):
    for j in range(col):
        a = A
        a[i][j] = f[i][j]
        mag = 20 * np.log(np.abs(a))
        freal = mag.real
        freal = np.uint8(freal)
        cv2.imshow('', freal)
        cv2.waitKey()

mag = 20 * np.log(np.abs(f))
freal = mag.real
freal = np.uint8(freal)
cv2.imshow('', freal)
cv2.waitKey()
