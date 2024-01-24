import cv2

img=[]
for i in range(0,12+1):
    img.append(cv2.imread('robot_steps/'+str(i)+'.jpg'))

height,width,layers=img[1].shape

video=cv2.VideoWriter('robot_steps_vid.mp4',-1,1,(width,height))

for j in range(0,12+1):
    video.write(img[j])

cv2.destroyAllWindows()
video.release()