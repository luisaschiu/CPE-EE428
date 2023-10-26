import cv2

from magicwand import *

import argparse
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('video',help='path to input video file')
parser.add_argument('--output',help='path to output video file (optional)')
parser.add_argument('--calibration',default='iphone_calib.txt',help='path to calibration file')
parser.add_argument('--ball_radius',type=float,default=3,help='radius of ball in cm')
args = parser.parse_args()

wand = MagicWand(calibration_path=args.calibration,R=args.ball_radius)

cap = cv2.VideoCapture(args.video)

trajectory_lst = []
dist_lst = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    lst = wand.process_frame(frame)
    if len(lst) == 1:
        trajectory_lst.append(lst[0])
    if len(lst) == 2:
        dist_lst.append(lst)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) == ord('q'):
        break

ax = plt.axes(projection='3d')
x_array = np.empty((len(trajectory_lst)))
y_array = np.empty((len(trajectory_lst)))
z_array = np.empty((len(trajectory_lst)))
for i in range (0, len(trajectory_lst)):
    x_array[i] = trajectory_lst[i][0]
    y_array[i] = trajectory_lst[i][1]
    z_array[i] = trajectory_lst[i][2]
ax.plot3D(x_array, y_array, z_array, 'black')
plt.show()

if len(dist_lst) != 0:
    dist_array = np.empty((len(dist_lst)))
    for i in range (0, len(dist_lst)):
        x1 = dist_lst[i][0][0]
        x2 = dist_lst[i][1][0]
        y1 = dist_lst[i][0][1]
        y2 = dist_lst[i][1][1]
        z1 = dist_lst[i][0][2]
        z2 = dist_lst[i][1][2]
        dist_array[i] = ((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)**(1/2)
    avg_dst = np.mean(dist_array)
    print(avg_dst)
