import threading, time, cfg, picamera, cv2, bluetooth
import RPi.GPIO as GPIO
import numpy as np

# -------- GPIO SETUP -------- #
GPIO.setmode(GPIO.BOARD)
GPIO.setup(cfg.InputPin, GPIO.IN)

# -------- System Flags -------- #
__pirFlag = 0
__camFlag = 0
__fsrFlag = 0

pirThread_start = 0
camThread_start = 0
fsrThread_start = 0

# -------- Bluetooth Setup -------- #

bd_addr = "98:D3:31:FC:A9:EB"
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

def pir(pirTrig):

    global __pirFlag
    
    while not pirTrig.is_set():
        if GPIO.input(cfg.InputPin):
            __pirFlag = 1
            pirTrig.set()
            print('PIR Event Triggered')
            time.sleep(1)
        else:
            __pirFlag = 0
            time.sleep(1)
        print(__pirFlag)
    print('Exiting PIR Thread')

def cam(camTrig, pirTrig):

    global pirThread_start
    global __camFlag
    global __pirFlag

    camera = picamera.PiCamera()
    camera.resolution = (1024, 768)

    counter = 0
    __length = 0

    while counter < 10:

        camera.start_preview()
        time.sleep(1)
        camera.capture('test.jpg')
        camera.stop_preview()

        img = cv2.imread('test.jpg',1)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        path = "haarcascade_frontalface_default.xml"
        face_cascade = cv2.CascadeClassifier(path)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(40,40))

        #Debug frame output to visualize FR positive/negative capture
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)        
        cv2.imshow("Image", img)

        cv2.waitKey(1000)
        cv2.destroyAllWindows()

        __length = len(faces)

        counter +=1
        print('On Iteration {} of Camera detection loop'.format(counter))

        if __length > 0:
            __camFlag = 1
            camTrig.set()
            print('Camera Trigger is Set, Cam Flag is {}'.format(__camFlag))
            time.sleep(0.5)
            break
        else:
            __camFlag = 0
            time.sleep(1)

    if counter == 10:
        pirThread_start = 0
        print('Loop exited with Cam flag as {}, PIR Thread start reset'.format(__camFlag))
        time.sleep(0.5)

    camera.close()
    print('Camera closed, Thread closing')
    time.sleep(0.5)

def fsr(fsrTrig):

    global __fsrFlag

    data = ""
    weight = 0.0

    while 1:
        try:
            data = sock.recv(1024)
            data = data.decode('utf-8')
            data_end = data.find('\n')

            if data_end != -1:
                weight = float(data)
                print('FSR Records: {}'.format(weight))

                if weight > 20.0:
                    __fsrFlag = 1
                    time.sleep(1)
                    break
        except:
            pass

    print('Exiting FSR Thread')

def timeout():
    global pirThread_start
    global camThread_start
    global fsrThread_start
    global __pirFlag
    global __camFlag
    global __fsrFlag

    counter = 5
    
    while counter > 0:
        print('Restarting in ...{}'.format(counter))
        counter -= 1
        time.sleep(1)

    pirThread_start = camThread_start = fsrThread_start = __pirFlag = __camFlag = __fsrFlag = 0

def main():

    global pirThread_start
    global camThread_start
    global fsrThread_start

    pirTrig = threading.Event()
    camTrig = threading.Event()
    fsrTrig = threading.Event()

    while True:

        if pirThread_start == 0:
            pirThread = threading.Thread(target=pir, args=(pirTrig,))
            print('PIR Thread Created')
            pirThread_start = 1
            pirThread.start()
            print('PIR Thread Started')

        if fsrThread_start == 0:
            fsrThread = threading.Thread(target=fsr, args=(fsrTrig,))
            print('FSR Thread Created')
            fsrThread_start = 1
            fsrThread.start()
            print('FSR Thread Started')

        if pirTrig.is_set():
            pirTrig.clear()
            print('PIR Trigger reset')
            camThread = threading.Thread(target=cam, args=(camTrig,pirTrig,))
            print('Cam Thread Created')
            camThread_start = 1
            camThread.start()
            print('Cam Thread Started')

        if __pirFlag == 1 and __camFlag == 1 and __fsrFlag == 1:
            threading.Timer(10, timeout).start()
            print('...waiting on reset...')
            time.sleep(15)

        time.sleep(5)
        print('Cam Flag is {}, Pir Flag is {}, FSR Flag is {}'.format(__camFlag, __pirFlag, __fsrFlag))

if __name__ == '__main__':
    main()
    