import threading, time, cfg, picamera, cv2
import RPi.GPIO as GPIO
import numpy as np

GPIO.setmode(GPIO.BOARD)
GPIO.setup(cfg.InputPin, GPIO.IN)

__pirFlag = 0
__camFlag = 0

resourceLock = threading.Lock()

def pir():

    global __pirFlag
    
    while True:
        if GPIO.input(cfg.InputPin):
            __pirFlag = 1
            time.sleep(1)
        else:
            __pirFlag = 0

def cam():

    global __camFlag
    global __pirFlag
    counter = 0
    flag = 0

    camera = picamera.PiCamera()

    while True:

        if __pirFlag == 1:
            resourceLock.acquire()
            print('Lock Acquired')
            __pirFlag = 1
            while counter < 10 and __camFlag == 0:
                counter += 1
                
                camera.resolution = (1024, 768)
                #camera.start_preview()
                time.sleep(1)
                camera.capture('test.jpg')
                #camera.close()

                img = cv2.imread("test.jpg",1)
                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                path = "haarcascade_frontalface_default.xml"
                face_cascade = cv2.CascadeClassifier(path)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(40,40))

                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)        
                cv2.imshow("Image", img)

                __camFlag = len(faces)

                print('--DEBUG-- flag = {}'.format(__camFlag))

                cv2.waitKey(1500)
                cv2.destroyAllWindows()
                time.sleep(2)

        if __camFlag == 1:
            print('Out of Loop')
            resourceLock.release()
            print('Lock Released')
            break

def main():
    pirThread = threading.Thread(target=pir)
    #pirThread.setDaemon(True)

    camThread = threading.Thread(target=cam)

    pirThread.start()
    camThread.start()

    while True:
        print('PIR flag is: {}'.format(__pirFlag))
        print('Camera flag is: {}'.format(__camFlag))
        time.sleep(1)

if __name__ == '__main__':
    main()
    
