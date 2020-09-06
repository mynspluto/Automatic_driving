from Bluetin_Echo import Echo
import RPi.GPIO as GPIO
import time
import cv2 , os
import threading
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
p1 = GPIO.PWM(12,50)
p2 = GPIO.PWM(16,50)
p3 = GPIO.PWM(20,50)
p4 = GPIO.PWM(21,50)

p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)




#cap = cv2.VideoCapture(1)
#print(cap.isOpened())

os.system("sudo modprobe bcm2835-v4l2")  #result : create /dev/video0
os.system("rm -rf avi/rec.avi")  #result : create /dev/video0
video_capture = cv2.VideoCapture(0)  # load /dev/video0

#카메라 설정
video_capture.set(cv2.CAP_PROP_FPS,20)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH ,320)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

from flask import Flask, render_template, request
from flask import send_file
from werkzeug import secure_filename
import os

PEOPLE_FOLDER = os.path.join('avi')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/', methods=['GET', 'POST'])
def download():
    return send_file('avi/rec.avi', as_attachment=True)
def filesend():
    app.run(host = '0.0.0.0')


sp = 40

def back(sp):
    p1.ChangeDutyCycle(sp)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(sp)
    p4.ChangeDutyCycle(0)

def go(sp):
    p2.ChangeDutyCycle(sp)
    p1.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(sp)
    p3.ChangeDutyCycle(0)
def right(sp):
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(sp)
    p3.ChangeDutyCycle(sp)
    p4.ChangeDutyCycle(0)

def left(sp):
    p2.ChangeDutyCycle(0)
    p1.ChangeDutyCycle(sp)
    p4.ChangeDutyCycle(sp)
    p3.ChangeDutyCycle(0)

def stop(sp = 0):
    p2.ChangeDutyCycle(0)
    p1.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(0)

stop()


data =Echo(23, 24, 315)
ultra = 0
def echoThread():
    global ultra
    while True:
        ultra = data.read('cm',3)
        print(ultra)
        time.sleep(0.5)


t1 = threading.Thread(target = echoThread)
t1.daemon = True
t1.start()

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

template1 = cv2.imread('temp1.jpg',0) 
template2 = cv2.imread('temp2.jpg',0) 
w1, h1 = template1.shape[::-1] #
w2, h2 = template2.shape[::-1] #
mode = 'go'
fourcc = cv2.VideoWriter_fourcc(*'XVID')  
output = cv2.VideoWriter('avi/rec.avi', fourcc, 20.0, (320,240))

def Matching(frame):
    global template1, template2, mode , w1 , w2 , h1 , h2
    if mode == 'go':
        res1 = cv2.matchTemplate(frame,template1,cv2.TM_SQDIFF)
        min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res1)
        print("min1", min_val1)
        if(min_val1  < 3000000):
            #print("people")
            mode = 'stop'
            stop()
            top_left1 = min_loc1
            bottom_right1 = (top_left1[0] + w1, top_left1[1] + h2) 
            cv2.rectangle(frame1,top_left1, bottom_right1, 255, 2) #사각형을 그림
    else:
        res2 = cv2.matchTemplate(frame,template2,cv2.TM_SQDIFF)
        min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(res2)
        print("min2", min_val2)
        if(min_val2  < 3000000):
            #print("go")
            mode = 'go'
            top_left2 = min_loc2
            bottom_right2 = (top_left2[0] + w1, top_left2[1] + h2) 
            cv2.rectangle(frame1,top_left2, bottom_right2, 255, 2) #사각형을 그림




count = 0

while True:
    ret, frame2 = video_capture.read() #카메라 읽어옴
    frame1 = cv2.resize(frame2, dsize=(320,240), interpolation=cv2.INTER_AREA)
    frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY) #흑백으로 변환
    threading.Thread(target = Matching,args=(frame,)).start()
    '''
    #cv2.imwrite('/home/pi/project/pic.jpg', frame)
    '''
    ret,img= cv2.threshold(frame,127,255,cv2.THRESH_BINARY) #흰,검 으로 변환
    img= cv2.Canny(img,200,400) #윤곽선 추출
    img = img[100:140,0:320]
    roi = frame1[100:140,0:320]

    print('------------------------')
    contours, hierarchy = cv2.findContours(img,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE) 
    xLoc = []
    for i in range(len(contours)): #윤곽선마다 반복문을 돌림
        cnt = contours[i]
        area = cv2.contourArea(cnt) #넓이를 구함
        perimeter = cv2.arcLength(cnt , False)
        x,y,w,h = cv2.boundingRect(cnt)
        cx =int(x + w/2)
        cy =int(y + h/2)
        #print(str(round(h/w , 1))+'\t:' + str(int(perimeter)) + "\t:" + str(cx))
        cv2.drawContours(roi, contours, -1, (0,255,0), 1)
        if perimeter>= 60 and perimeter< 10000 and h/w > 0.5: 
            xLoc.append(cx)
            cv2.drawContours(roi, contours, -1, (255,0,0), 1)
    cv2.imwrite('/home/pi/project/pic.jpg', frame1)
    output.write(frame1)
    re = ''
    if len(xLoc) > 0 and ultra >= 5:
        if max(xLoc) < 250 and max(xLoc) > 200 and mode == 'go':
            left(sp)
            re = 'left'
        elif min(xLoc) > 70 and min(xLoc) < 120 and mode == 'go':
            re = 'right'
            right(sp)
        elif mode=='go':
            re = 'go'
            go(sp)
        print("cxcxcxcx",mode,max(xLoc) , min(xLoc) , ultra, re)
        count = 0 

    else:
        stop()
        count += 1
    if count > 100:
        output.release()
        break
    '''
    point = -1

    print(int(ret), int(point))
    if point == -1:
        stop()
    elif int(point) < 150 :
        left(sp)
    elif int(point) < 170 :
        right(sp)
    else:
        go(sp)
    '''
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
video_capture.release()

filesend()
