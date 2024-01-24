import cv2 as cv

grey_img = cv.imread('input_img.jpg', cv.IMREAD_GRAYSCALE)
cv.imshow('grey_img', grey_img)
cv.waitKey(0)
# ret2,th1 = cv.threshold(grey_img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
ret2,th2 = cv.threshold(grey_img,0,255,cv.THRESH_OTSU) # this one looked better than adding cv.THRESH_BINARY
# cv.imshow('th1', th1)
# cv.waitKey(0)
cv.imwrite('BW_img.jpg', th2)
# cv.imshow('th2', th2)
# cv.waitKey(0)