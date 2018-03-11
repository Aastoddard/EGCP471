#-------------------------------------------------------------------#
#                                                                   #
# Facial Recognition Script with Signal Driver Code                 #
#                                                                   #
# Contriubutors:                                                    #
#   Aaron Stoddard                                                  #
#                                                                   #
# Last Updated: 20 February 2018                                    #
#                                                                   #
# This script is designed to execute a facial recognition algorithm #
# in order to drive a useable signal. The script uses a pre-trained #
# haar cascade algorithm to determine a positive/negative match for #
# a face within a single frame of video input capture. If a         #
# positive match is found the script them generates a signal which  #
# is used in this case to drive a simple LED circuit. In this way   #
# we can turn a positive facial recognition match into a useable    #
# signal driver.                                                    #
#                                                                   #
# In actual use the script will not need to open a window to        #
# display the frame output capture and thus the code associated     #
# with video frame output and drawing a visible rectangle will be   #
# removed. It is present in the script at this time to visibly      #
# identify that a positive facial recognition "hit" has occurred.   #
#                                                                   #
#-------------------------------------------------------------------#

import picamera
import numpy as np
import cv2
import RPi.GPIO as GPIO
import time

#----------  GPIO SETUP  ----------#
LedPin = 11  #pin11

def setup():
    GPIO.setmode(GPIO.BOARD)       # numbers GPIOs by physical location
    GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin to out
    GPIO.output(LedPin, GPIO.HIGH) # set LedPin high(+3.3V) to off led

#----------   CLEANUP  ----------#
def destroy():
    GPIO.output(LedPin, GPIO.HIGH) # led off
    GPIO.cleanup()                 # release GPIO resources
    cv2.destroyAllWindows()        # close out opened cv2 windows    

#----------  CAMERA SETUP  ----------#
camera = picamera.PiCamera()  # assign camera to PiCam
camera.resolution = (640, 480) 
camera.framerate = 32
output = np.empty((480, 640, 3), dtype=np.uint8)  # raw numpy array data

path = "haarcascade_frontalface_default.xml"  # FR algorithm path

face_cascade = cv2.CascadeClassifier(path)  # FR algorithm classifier

#----------   MAIN  ----------#
setup()  # execute GPIO setup

while(True):

    camera.capture(output, format="bgr")  # capture frames from camera

    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)  # convert to grayscale img

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(40,40))  # faces is the FR cascade

    print(len(faces))  # dummy print function to ensure capture positive

    for (x, y, w, h) in faces:
        cv2.rectangle(output, (x, y), (x+w, y+h), (0, 255, 0), 2)  #draw rectangle on captured img

    frame = cv2.resize(output, (0, 0), fx=0.5, fy=0.5)    

    cv2.imshow("Frame", frame)
    
    if (len(faces) > 0):
        GPIO.output(LedPin, GPIO.LOW)  # led on
    else:
        GPIO.output(LedPin, GPIO.HIGH)  # led off

    ch = cv2.waitKey(1)
    if ch == ord('q'):  # if 'q' is pressed then our while loop breaks 
        break
    
destroy()  #execute cleanup


