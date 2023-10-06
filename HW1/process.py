import rawpy
from raw import *
import numpy as np
import argparse
import imageio
import os

parser = argparse.ArgumentParser()
parser.add_argument('path',help='path to DNG file')
args = parser.parse_args()

# this is the path to the output JPEG
path_out = os.path.basename(args.path).split('.')[0]+'.JPG'

with rawpy.imread(args.path) as raw:
    # raw_image contains the raw image data in 16-bit integer format.
    raw_image = raw.raw_image
    normalized_img = raw_image.astype(np.float32) / (2**16 - 1)
    original = np.array([[100, 20, 30, 40], [80, 10, 70, 20], [10, 20, 30, 20], [200, 70, 80, 90]])
    padded = np.pad(original, pad_width=1, mode='constant', constant_values=0)
    print("Padded Array:")
    print(padded)
    row = padded.shape[0] # num of rows
    col = padded.shape[1] # num of col
    Red = []
    Blue = []
    Green = []
    Red_array= np.empty((original.shape[0], original.shape[1]))
    Blue_array= np.empty((original.shape[0], original.shape[1]))
    Green_array= np.empty((original.shape[0], original.shape[1]))
    for i in range(1, row-1, 1): 
        for j in range(1, col-1, 1):
            # At red pixel
            if i%2 != 0 and j%2 != 0:
                Red.append(padded[i, j])
                Red_array[i-1 ,j-1] = padded[i, j]
                Green.append((1/4)*(padded[i+1, j] + padded[i-1, j] + padded[i, j-1] + padded[i, j+1]))
                Green_array[i-1 ,j-1] = (1/4)*(padded[i+1, j] + padded[i-1, j] + padded[i, j-1] + padded[i, j+1])
                Blue.append((1/4)*(padded[i+1, j+1] + padded[i-1, j-1]+ padded[i-1, j+1] + padded[i+1, j-1]))
                Blue_array[i-1 ,j-1] = (1/4)*(padded[i+1, j+1] + padded[i-1, j-1]+ padded[i-1, j+1] + padded[i+1, j-1])
            # At green pixel with red adjacent
            elif i%2 != 0 and j%2 == 0:
                Red.append((1/2)*(padded[i, j-1] + padded[i, j+1]))
                Red_array[i-1,j-1] = (1/2)*(padded[i, j-1] + padded[i, j+1])
                Green.append(padded[i,j])
                Green_array[i-1 ,j-1] = padded[i,j]
                Blue.append((1/2)*(padded[i-1, j]+padded[i+1, j]))
                Blue_array[i-1 ,j-1] = (1/2)*(padded[i-1, j]+padded[i+1, j])
            # At green pixel with blue adjacent
            elif i%2 == 0 and j%2 != 0:
                Red.append((1/2)*(padded[i-1, j]+padded[i+1, j]))
#                np.append(Red_array, (1/2)*(padded[i-1, j]+padded[i+1, j]))
                Red_array[i-1,j-1] = (1/2)*(padded[i-1, j]+padded[i+1, j])
                Green.append(padded[i,j])
                Green_array[i-1 ,j-1] = padded[i,j]
                Blue.append((1/2)*(padded[i, j-1] + padded[i, j+1]))
                Blue_array[i-1 ,j-1] = (1/2)*(padded[i, j-1] + padded[i, j+1])
            # At blue pixel
            elif i%2 == 0 and j%2 == 0:
                Red.append((1/4)*(padded[i+1, j+1] + padded[i-1, j-1]+ padded[i-1, j+1] + padded[i+1, j-1]))
#                np.append(Red_array, (1/4)*(padded[i+1, j+1] + padded[i-1, j-1]+ padded[i-1, j+1] + padded[i+1, j-1]))
                Red_array[i-1,j-1] = (1/4)*(padded[i+1, j+1] + padded[i-1, j-1]+ padded[i-1, j+1] + padded[i+1, j-1])
                Green.append((1/4)*(padded[i+1, j] + padded[i-1, j] + padded[i, j-1] + padded[i, j+1]))
                Green_array[i-1 ,j-1] = (1/4)*(padded[i+1, j] + padded[i-1, j] + padded[i, j-1] + padded[i, j+1])
                Blue.append(padded[i, j])
                Blue_array[i-1 ,j-1] = padded[i, j]
#print(Red)
#print(np.array(Red))
print()
print("Red array:")
print(Red_array)
print("Blue array:")
print(Blue_array)
print("Green array:")
print(Green_array)
c = np.stack((Red_array, Green_array, Blue_array), axis = 2)
print("Stacked array:")
print(c)
print(c.shape)
#    for i in 
#    print(normalized_img)
#    print(normalized_img.size)
#    print(normalized_img.shape)

