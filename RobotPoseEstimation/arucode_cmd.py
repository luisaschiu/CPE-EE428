import cv2
import numpy as np
import argparse
from arucode_functions import find_grid_position
# import time

marker_image = None
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250) 
marker_image = cv2.aruco.generateImageMarker(dictionary, 8, 200, marker_image, 1)
argparser = argparse.ArgumentParser()
argparser.add_argument('imagePath', help='path to image file')
args = argparser.parse_args()

inputImg = args.imagePath

origImg = cv2.imread(inputImg)
gray = cv2.imread(inputImg, cv2.IMREAD_GRAYSCALE)

detectorParams = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, detectorParams)
markerCorners, markerIds, _ = detector.detectMarkers(gray)

if markerIds is not None and len(markerIds) > 0:
    frame = cv2.aruco.drawDetectedMarkers(origImg, markerCorners, markerIds, (0, 0,255))

    for markerRect in markerCorners:
        bottomLeft = markerRect[0][1]
        bottomRight = markerRect[0][0]
        topRight = markerRect[0][3]
        topLeft = markerRect[0][2]
        diff = (topRight[0] - topLeft[0], topLeft[1] - topRight[1])
        angle = np.arctan2(diff[1], diff[0]) * 180 / np.pi
        # normalize values to 0 - 360 degrees
        if angle < 0:
            angle += 360
        # draw text angle of the marker
        angle = round(angle, 2)
        # draw position in pixels
        center = (bottomRight + topLeft) / 2
        cv2.putText(frame,
                    str(angle) + 'deg ',
                    (int(center[0] - 40), int(center[1] + 60)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 0, 255),
                    2,
                    cv2.LINE_AA)
        cv2.putText(frame,
                    str(center),
                    (int(center[0] - 40), int(center[1] + 90)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 0, 255),
                    2,
                    cv2.LINE_AA)
        length = 50
        # change angle back to radians
        angle = angle * np.pi / 180
        cv2.line(
            frame, 
            (int(center[0]), int(center[1])), 
            (int(center[0] + length * np.cos(angle)), int(center[1] - length * np.sin(angle))),
            (0, 255, 255), 
            5
        )
print(find_grid_position(frame, center[0], center[1]))
# draw_gridlines(frame)
cv2.imshow('ArUco Marker Angle', frame)

cv2.waitKey(0)
cv2.destroyAllWindows()