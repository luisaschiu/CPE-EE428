import rawpy
from raw import *
import numpy as np
import cv2
import imageio


#img1 = cv2.imread('Processed_Image.jpeg', IMREAD_UNCHANGED)
#img2 = cv2.imread('L1004432.jpg')
#img1 = imageio.imread("Processed_Image.jpeg", as_gray=False, pilmode="RGB")
#img2 = imageio.imread("L1004432.jpg", as_gray=False, pilmode="RGB")
#print(img_diff)
#img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
#img_diff = img1-img2

#cv2.imshow('diff', img_diff)
#cv2.waitKey(0)
#print(np.min(img_diff))
'''
img1 = cv2.imread('Processed_Image.png')
img2 = cv2.imread('L1004432.jpg')
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

h, w = img1.shape
diff = cv2.subtract(img1, img2)
err = np.sum(diff**2)
mse = err/(float(h*w))
print(mse)
'''