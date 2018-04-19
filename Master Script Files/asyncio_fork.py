import asyncio, time, functools, cfg, picamera, cv2, bluetooth
import RPi.GPIO as GPIO
import numpy as np

GPIO.setmode(GPIO.BOARD)
GPIO.setup(cfg.InputPin, GPIO.IN)

pirFlag = 0
camFlag = 0
fsrFlag = 0

#-----------------------------------------------------------#
#   pirSim                                                  #
# Producer coroutine - grabs input from RPI GPIO and places #
# it into a queue. Yields output.                           #
#-----------------------------------------------------------#
@asyncio.coroutine
def pirSim(pir_Queue):
    __pirIn = 0
    while True:
        if GPIO.input(cfg.InputPin):
            __pirIn = 1
        else:
            __pirIn = 0
        print('PIR Input is {}'.format(__pirIn))
        yield from pir_Queue.put(__pirIn)
        yield from asyncio.sleep(2)

#-----------------------------------------------------------#
#   pirFlag                                                 #
# Consumer coroutine - grabs the high/low output from the   #
# queue and sets an appropriate 'event'.                    #
#-----------------------------------------------------------#
@asyncio.coroutine
def pirFlag(pir_event, pir_Queue):

    global pirFlag
    
    while True:
        __pirOut = yield from pir_Queue.get()
        print('Grabbed {} from the PIR'.format(_pirOut))
        if __pirOut == 1:
            pirFlag = 1
            pir_event.set()
            print('Event set is {}'.format(event.is_set()))
            print('PIR Flag is {}'.format(pirFlag))
        else:
            pirFlag = 0
            print('PIR Flag is {}'.format(pirFlag))

#-----------------------------------------------------------#
#   fsrSim                                                  #
# Producer coroutine - grabs the input from the fsr and     #
# places it into a queue. Yields output.                    #
#-----------------------------------------------------------#
#@asyncio.coroutine
#def fsrSim(fsr_Queue):

 #   pass # placeholder until BT testing
    
    """bd_addr = "98:D3:31:FC:A9:EB"   #define mac address of unit
    port = 1    #default port
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)  #define the socket comm protocol
    sock.connect((bd_addr, port))   #establish connection

    data = ""

    while True:
        try:
            data = sock.recv(1024)
            data_end = data.find('\n')

            if data_end != -1:
                print(data)
        yield from fsr_Queue.put(data)
        yield from asyncio.sleep(2)"""

#-----------------------------------------------------------#
#   fsrFlag                                                 #
# Consumer coroutine - grabs the output from the queue and  #
# sets an appropriate event.                                #
#-----------------------------------------------------------#
"""@asyncio.coroutine
def fsrFlag(fsr_event, fsr_Queue):

    pass # placeholder until BT testing

    global fsrFlag

    while True:
        __fsrOut = yield from fsr_Queue.get()
        print('Grabbed {} from the FSR'.format(__fsrOut))"""

        # --------- TODO ---------
        # 1. Implement FSR logic
        
#-----------------------------------------------------------#
#   middleMan                                               #
# Event traffic coordinator - Accepts events from raw       #
# sensor events. Compares current system status to behavior #
# states and sets or clears events based upon next behavior #
#-----------------------------------------------------------#
"""async def middleMan(pir_event, cam_event):

    --------- TODO ---------
    1. create the "signal controller", event manager
        
    global camFlag

    while True:
        print('Middle man waiting on pir event')
        await pir_event.wait()
        print('PIR Triggered')
        if camFlag == 0:
            cam_event.set()
            pir_event.clear()
        else:
            pir_event.clear()"""

#-----------------------------------------------------------#
#   camSim                                                  #
# Awaits a triggering event and then runs the facial        #
# recognition code.                                         #
#-----------------------------------------------------------#
async def camSim(cam_event):

    global camFlag

    camera = picamera.PiCamera()
    camera.resolution = (1024, 768)

    while True:

        __length = 0

        print('Camera waiting for the pir flag event to occur...')
        await cam_event.wait()
        print('Flag triggered, running camera script...')

        camera.start_preview()
        time.sleep(2)
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

        cv2.waitKey(5000)
        cv2.destroyAllWindows()

        __length = len(faces)

        if __length > 0:
            camFlag = 1
            print('Camera flag is set')
            cam_event.clear()
            print('Event Cleared and reset')
            print('Event set is {}'.format(event.is_set()))
        else:
            camFlag = 0
            cam_event.clear()
            print('Event Cleared and reset')
            print('Event set is {}'.format(event.is_set()))

async def main(loop):
    pirEvent = asyncio.Event()
    camEvent = asyncio.Event()
    
    await asyncio.wait([pirSim(pirQueue), pirFlag(pirEvent, pirQueue), camSim(pirEvent)])

pirQueue = asyncio.Queue(maxsize=2)
fsrQueue = asyncio.Queue(maxsize = 20)
event_loop = asyncio.get_event_loop()
event_loop.create_task(main(event_loop))
try:
    print('Starting Event Loop')
    event_loop.run_forever()
finally:
    print('Closing Event Loop')
    event_loop.close()
