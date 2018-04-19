import asyncio, time, functools, cfg, picamera, cv2
import RPi.GPIO as GPIO
import numpy as np

GPIO.setmode(GPIO.BOARD)
GPIO.setup(cfg.InputPin, GPIO.IN)

pirFlag = 0
camFlag = 0

@asyncio.coroutine
def pirSim(myQueue):
    __pirIn = 0
    while True:
        if GPIO.input(cfg.InputPin):
            __pirIn = 1
        else:
            __pirIn = 0
        print('PIR Input is {}'.format(__pirIn))
        yield from myQueue.put(__pirIn)
        yield from asyncio.sleep(2)

@asyncio.coroutine
def pirFlag(event, myQueue):

    global pirFlag
    
    while True:
        __pirOut = yield from myQueue.get()
        print('Grabbed {} from the PIR'.format(pirFlag))
        if __pirOut == 1:
            pirFlag = 1
            event.set()
            print('Event set is {}'.format(event.is_set()))
            print('PIR Flag is {}'.format(pirFlag))
        else:
            pirFlag = 0
            print('PIR Flag is {}'.format(pirFlag))


async def camSim(event):

    global camFlag

    camera = picamera.PiCamera()
    camera.resolution = (1024, 768)

    while True:

        __length = 0

        print('Camera waiting for the pir flag event to occur...')
        await event.wait()
        print('Flag triggered, running camera script...')

        #camera.start_preview()
        time.sleep(2)
        camera.capture('test.jpg')
        #camera.stop_preview()

        img = cv2.imread('test.jpg',1)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        path = "haarcascade_frontalface_default.xml"
        face_cascade = cv2.CascadeClassifier(path)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(40,40))

        #Debug frame output to visualize FR positive/negative capture
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)        
        cv2.imshow("Image", img)

        cv2.waitKey(5000)
        cv2.destroyAllWindows()

        __length = len(faces)

        if __length > 0:
            camFlag = 1
            print('Camera flag is set')
            #time.sleep(0.5)
        else:
            event.clear()
            print('Event Cleared and reset')
            print('Event set is {}'.format(event.is_set()))

async def main(loop):
    event = asyncio.Event()
    print('Event created, start state is: {}'.format(event))
    await asyncio.wait([pirSim(myQueue), pirFlag(event, myQueue), camSim(event)])

myQueue = asyncio.Queue(maxsize=2)
event_loop = asyncio.get_event_loop()
event_loop.create_task(main(event_loop))
try:
    print('Starting Event Loop')
    event_loop.run_forever()
finally:
    print('Closing Event Loop')
    event_loop.close()
