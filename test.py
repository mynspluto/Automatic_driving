from Bluetin_Echo import Echo
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)


def back():
    GPIO.output(12,True)
    GPIO.output(16,False)
    GPIO.output(20,True)
    GPIO.output(21,False)

time.sleep(1)

def go():
    GPIO.output(16,True)
    GPIO.output(12,False)
    GPIO.output(21,True)
    GPIO.output(20,False)
time.sleep(1)

def stop():
    GPIO.output(16,False)
    GPIO.output(12,False)
    GPIO.output(21,False)
    GPIO.output(20,False)


data =Echo(23, 24, 315)
ret = data.read('cm',3)
print(ret)
