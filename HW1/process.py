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
    demosaiced_img = demosaic(raw_image)
    white_balanced_img = white_balance(demosaiced_img)
    processed_img = curve_and_quantize(white_balanced_img, 0.85)
    imageio.imwrite("Processed_Image.png", processed_img)
    imageio.imwrite("Processed_Image.jpeg", processed_img)