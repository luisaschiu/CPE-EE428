import cv2 as cv
import numpy as np

marker_image = None
dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
marker_image = cv.aruco.generateImageMarker(dictionary, 8, 200, marker_image, 1)
cv.imwrite("marker8.jpg", marker_image)

# markerIds = []
markerIds = np.array([])
markerCorners, rejectedCandidates = [], []

detectorParams = cv.aruco.DetectorParameters()
detector = cv.aruco.ArucoDetector(dictionary, detectorParams)

# Test marker detection on static image
# inputImage = cv.imread("test_marker_img.jpg")
# markerCorners, markerIds, _ = detector.detectMarkers(inputImage)
# outputImage = inputImage.copy()
# outputImage = cv.aruco.drawDetectedMarkers(outputImage, markerCorners, markerIds)
# cv.imshow("out", outputImage)
# cv.waitKey(0)

# Marker Detection using video input
input_video = cv.VideoCapture(0)
markerIds = np.array([])
y=100
x=10
h=550
w=455
while input_video.isOpened():
    ret, frame = input_video.read()
    frame = cv.flip(frame, -1)
    frame = frame[x:w, y:h]
    if not ret:
        break

    markerCorners, markerIds, _ = detector.detectMarkers(frame)
    outputImage = frame.copy()

    # If at least one marker detected
    if markerIds is not None and len(markerIds) > 0:
        outputImage = cv.aruco.drawDetectedMarkers(outputImage, markerCorners, markerIds)
    print(markerCorners)
    cv.imshow("out", outputImage)
    key = cv.waitKey(1)

    if key == 27:  # Press 'Esc' to exit
        break

input_video.release()
