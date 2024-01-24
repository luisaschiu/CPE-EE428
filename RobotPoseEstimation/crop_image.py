import cv2 as cv

# Capture image from camera
# input_video = cv.VideoCapture(0) # video capture source camera
# while input_video.isOpened():
#     ret, frame = input_video.read()
#     frame = cv.flip(frame, -1)
#     cv.imshow("frame", frame)
#     if not ret:
#         break
#     if cv.waitKey(1) & 0xFF == ord('q'): #save on pressing 'q' 
#         cv.imwrite('images/camera_img.jpg', frame)
#         cv.destroyAllWindows()
#         break
# input_video.release()



# Crop image
# y=100
# x=10
# h=550
# w=455
# image = cv.imread("images/camera_img.jpg")
# # cv.imshow("original", image)
# crop_image = image[x:w, y:h]
# cv.imshow("Cropped", crop_image)
# cv.imwrite('images/cropped_img.jpg', crop_image)
# cv.waitKey(0)

# Crop image
y=303
x=13
h=980
w=678
image = cv.imread("robot_steps/old12.jpg")
# cv.imshow("original", image)
crop_image = image[x:w, y:h]
cv.imshow("Cropped", crop_image)
cv.imwrite('robot_steps/12.jpg', crop_image)
cv.waitKey(0)
