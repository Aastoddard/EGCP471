#-------------------------------------------------------------------#
#                                                                   #
# Facial Recognition Class Code                                     #
#                                                                   #
# Contriubutors:                                                    #
#   Aaron Stoddard                                                  #
#                                                                   #
# Developed using Facial Recognition code from:                     #
#   Aaron Stoddard                                                  #
#                                                                   #
# Last Updated: 10 March 2018                                       #
#                                                                   #
# This script is designed to execute a facial recognition algorithm #
# in order to drive a useable signal. The script uses a pre-trained #
# haar cascade algorithm to determine a positive/negative match for #
# a face within a single frame of input capture. If a positive      #
# match is established a software flag is set which can be used to  #
# drive other software executions within the master script.         #
#                                                                   #
#-------------------------------------------------------------------#

import picamera
import time
import cv2
import numpy as np

class FacialRec:

    #------------------------  __init__  ------------------------#
    # will run when class FacialRec is first created             #
    # sets up the camera and captures an initial frame           #
    #------------------------------------------------------------#
    def __init__(self):

        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.start_preview()
            time.sleep(2)
            camera.capture('test.jpg')

    #------------------------  process  ------------------------#
    # process imports the capture image, converts the image to  #
    # grayscale and then applies HAAR cascade FR detection      #
    # algorithm to the still image to process a pos/neg 'hit'   #
    # the flag is determined the len(faces) function which will #
    # either return 0 for no faces detected to x > 0 for        #
    # positive FR hit.                                          #
    #-----------------------------------------------------------#
    def process(self):

        img = cv2.imread("test.jpg",1)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        path = "haarcascade_frontalface_default.xml"
        face_cascade = cv2.CascadeClassifier(path)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(40,40))

        #Debug frame output to visualize FR positive/negative capture
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)        
        cv2.imshow("Image", img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        __length = len(faces)

        #debug print
        print("---------------------------- TEST ----------------------------")
        print("__length = ", __length)

        return __length

    #------------------------  returnFlag  ------------------------#
    # call process function to set and return the FR flag          #
    #--------------------------------------------------------------#
    def returnFlag(self):
        flag = self.process()

        return flag
