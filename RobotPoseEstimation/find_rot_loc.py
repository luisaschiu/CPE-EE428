import cv2
import numpy as np
import argparse
from arucode_functions import arucode_angle, angle_difference, show_arucode_param, draw_gridlines, arucode_location, find_grid_position
import glob

# Rotation
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
argparser = argparse.ArgumentParser()
argparser.add_argument('filePath', help='path to image folder')
args = argparser.parse_args()
inputImg = args.filePath
images = glob.glob('robot_steps/*.jpg')
frame_num = 0
filePath = 'robot_steps/'
while frame_num < (len(images)-1):
    # print(str(frame_num) + ' to ' + str(int(frame_num + 1)))
    img1 = cv2.imread(filePath+str(frame_num)+'.jpg')
    img2 = cv2.imread(filePath+str(frame_num+1)+'.jpg')
    ang1 = arucode_angle(dictionary, img1)
    ang2 = arucode_angle(dictionary, img2)
    angle_diff = angle_difference(ang1, ang2)
    print(angle_diff)
    frame_num += 1

# Location
empty_maze = cv2.imread('empty_maze.jpg')

images = glob.glob('robot_steps/*.jpg')
frame_num = 0
filePath = 'robot_steps/'
while frame_num < (len(images)):
    # print(str(frame_num) + ' to ' + str(int(frame_num + 1)))
    img = cv2.imread(filePath+str(frame_num)+'.jpg')
    location = arucode_location(dictionary, img)
    draw_gridlines(img)
    print(find_grid_position(img, location[0], location[1]))
    frame_num += 1

# # Code for writing arucode paremeters on image and saving it in robot_steps_arucode folder
# argparser = argparse.ArgumentParser()
# argparser.add_argument('imagePath', help='path to image file')
# args = argparser.parse_args()
# inputImg = args.imagePath
# origImg = cv2.imread(inputImg)
# angle = arucode_angle(dictionary, origImg)
# arucode_img = show_arucode_param(dictionary, origImg)
# print(angle)
# cv2.imwrite("robot_steps/robot_steps_arucode/4.jpg", arucode_img)


# # Test angle_difference function
# print(angle_difference(0.0, 268.81, 5))     # 0 to 1
# print(angle_difference(268.81, 267.66, 5))  # 1 to 2
# print(angle_difference(267.66, 356.5, 5))   # 2 to 3
# print(angle_difference(356.5, 356.42, 5))   # 3 to 4
# print(angle_difference(356.42, 87.61, 5))   # 4 to 5
# print(angle_difference(87.61, 88.81, 5))    # 5 to 6
# print(angle_difference(88.81, 356.42, 5))   # 6 to 7
# print(angle_difference(356.42, 356.42, 5))  # 7 to 8
# print(angle_difference(356.42, 87.61, 5))   # 8 to 9
# print(angle_difference(87.61, 88.78, 5))    # 9 to 10
# print(angle_difference(88.78, 357.56, 5))   # 10 to 11
# print(angle_difference(357.56, 356.42, 5))  # 11 to 12