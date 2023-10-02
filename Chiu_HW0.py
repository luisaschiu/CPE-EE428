import cv2 as cv
import numpy as np


# Part I.
img = cv.imread("frames/000000.jpg")
cv.imshow("image1", img)
cv.waitKey(0)
grayscale1 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Grayscale', grayscale1)
cv.waitKey(0)
cv.imwrite("grayscale.png", grayscale1)

# Part II.
grayscale2_frames = []
capture = cv.VideoCapture('frames/%06d.jpg')
while capture.isOpened():
    # Capture frame-by-frame
    ret, frame = capture.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Display the resulting frame
    grayscale2 = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    grayscale2_frames.append(grayscale2)
    cv.imshow('frame', frame)
    if cv.waitKey(25) == ord('q'):
        break
capture.release()
background = np.mean(grayscale2_frames, axis = 0).astype(np.uint8)
cv.imshow('background', background)
cv.waitKey(0)
cv.imwrite('background.png', background)


# Part III.
img1 = cv.imread('background.png', cv.IMREAD_GRAYSCALE)
img2 = cv.imread('grayscale.png', cv.IMREAD_GRAYSCALE)
absdiff_img = cv.absdiff(img1, img2)
cv.imshow('absdiff_img', absdiff_img)
cv.waitKey(0)
ret1,th1 = cv.threshold(absdiff_img,25,255,cv.THRESH_BINARY)
ret2,th2 = cv.threshold(absdiff_img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
cv.imshow('th1', th1)
cv.waitKey(0)
cv.imshow('th2', th2)
cv.waitKey(0)

# Bonus.
background_img = cv.imread('background.png', cv.IMREAD_GRAYSCALE)
capture1 = cv.VideoCapture('frames/%06d.jpg')
while capture1.isOpened():
    ret, frame = capture1.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    grayscale2 = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    absdiff_img = cv.absdiff(background_img, grayscale2)
    ret1, thresh = cv.threshold(absdiff_img,25,255,cv.THRESH_BINARY)
    cv.imshow('thresholding_imgs', thresh)
    if cv.waitKey(25) == ord('q'):
        break
capture1.release()

capture2 = cv.VideoCapture('frames/%06d.jpg')
while capture2.isOpened():
    ret, frame = capture2.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    grayscale2 = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    absdiff_img = cv.absdiff(background_img, grayscale2)
    ret1, thresh = cv.threshold(absdiff_img,25,255,cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for contour in contours:
        cv.drawContours(frame, contour, -1, (0,255,0), 2)
        cv.imshow('frame', frame)
    if cv.waitKey(25) == ord('q'):
        break
capture2.release()
