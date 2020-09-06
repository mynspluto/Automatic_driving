import cv2  
import numpy as np
import time
import os
os.system('sudo modprobe bcm2835-v4l2') 
c = cv2.VideoCapture('/dev/video0') 

w=320
h=240

c.set(3,w) 
c.set(4,h)
c.set(cv2.CAP_PROP_FPS,20)


roiRect = [0,0,0,0]
flag  = 0
count = 0

def mouse_callback(event,x,y,flags,param):
    global count, roiRect , flag
    if event == cv2.EVENT_LBUTTONDOWN:
        if count == 0:
            roiRect[0] = x
            roiRect[1] = y
        elif count == 1:
            roiRect[2] = x
            roiRect[3] = y
            cv2.destroyWindow("capture")
        count += 1


cv2.namedWindow('capture')
cv2.setMouseCallback('capture', mouse_callback)

     
while (True):
    _, img = c.read()
    img= cv2.resize(img, dsize=(320, 240), interpolation=cv2.INTER_AREA)
    cv2.imshow('capture', img)
    k = cv2.waitKey(5) & 0xFF 
    if count == 2:
        #img1 = img[0:120,0:160]
        img1 = img[roiRect[1]:roiRect[3],roiRect[0]:roiRect[2]]
        cv2.imwrite('temp1.jpg',img1) 
        print(roiRect)
        break
    if k == 27:
        break
cv2.destroyAllWindows()


