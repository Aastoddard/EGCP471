import threading, time, cfg, picamera, cv2, bluetooth
import logging, datetime, csv
import RPi.GPIO as GPIO
import numpy as np
from Adafruit_SHT31 import *


# -------- GPIO SETUP -------- #
GPIO.setmode(GPIO.BOARD)
GPIO.setup(cfg.InputPin, GPIO.IN)

# -------- System Flags -------- #
__pirFlag = 0
__camFlag = 0
__fsrFlag = 0
__temp = 0.0
__hum = 0.0

pirThread_start = 0
camThread_start = 0
fsrThread_start = 0
tempThread_start = 0


# -------- Bluetooth Setup -------- #

bd_addr = "98:D3:31:FC:A9:EB"
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

# -------- Log file Creation -------- #
logging.basicConfig(filename = 'log_file.log', format = '%(asctime)s - %(levelname)s - %(message)s', level = logging.INFO)
logging.info('Log Started')

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

"""def tempSensor_status(sensor):

    status = sensor.read_status()
    is_data_crc_error = sensor.is_data_crc_error()
    is_command_error = sensor.is_command_error()
    is_reset_detected = sensor.is_reset_detected()
    is_tracking_temperature_alert = sensor.is_tracking_temperature_alert()
    is_tracking_humidity_alert = sensor.is_tracking_humidity_alert()
    is_heater_active = sensor.is_heater_active()
    is_alert_pending = sensor.is_alert_pending()"""
    

def temp():

    global __temp
    global __hum
    
    while True: 
        sensor = SHT31(address = 0x44)
        now = datetime.datetime.now()

        degreesCelsius = sensor.read_temperature()
        degreesFahrenheit = 9.0/5.0 * degreesCelsius + 32
        __temp = degreesFahrenheit
        humidity = sensor.read_humidity()
        __hum = humidity
        date = time.strftime("%m-%d-%Y")
        currentDatetime = time.strftime("%m-%d-%Y %H:%M %p")
            
        #tempSensor_status(sensor)
        print (currentDatetime) #print current time and date; for logging
        print ('Temp             = {0:0.3f} deg F'.format(degreesFahrenheit)) #Fahrenheit
        print ('Humidity         = {0:0.2f} %'.format(humidity))
        #print 'Temp             = {0:0.3f} deg C'.format(degreesCelsius) #Celsius for troubleshooting

        #set temperature for flag
        if degreesFahrenheit > 85:
            print ("Warning! Temperature is above 85 Degrees!") 
            heatFlag = 1
                 
        else:
            heatFlag = 0
                
        print (heatFlag) #for troubleshooting
        time.sleep(20)



    #sensor.clear_status()
    #sensor.set_heater(True)
    #tempSensor_status(sensor)

    #sensor.set_heater(False)
    #tempSensor_status(sensor)

def periodic_log():

    global __pirFlag
    global __camFlag
    global __fsrFlag
    global __temp
    global __hum

    """phoneFile = open('phone_data.csv')
    writer = csv.writer(phoneFile)
    writer.writerow([__pirFlag, __camFlag__, __fsrFlag, __temp])"""

    logging.info('Temp = {0:0.3f} deg F'.format(__temp))
    logging.info('Humidity = {0:0.2f} %'.format(__hum))
    logging.info('System Flags: pir is {}, cam is {}, fsr is {}'.format(__pirFlag, __camFlag, __fsrFlag))
    

def timeout():
    global pirThread_start
    global camThread_start
    global fsrThread_start
    global tempThread_start
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
    global tempThread_start
    global __pirFlag, __camFlag, __fsrFlag
    global __temp, __hum

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

        if tempThread_start == 0:
            tempThread = threading.Thread(target=temp)
            print('Temp Sensor Thread Started')
            tempThread_start = 1
            tempThread.start()
            print('Temp Sensor Started')

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

        threading.Timer(60, periodic_log).start() 

        time.sleep(5)
        print('Cam Flag is {}, Pir Flag is {}, FSR Flag is {}'.format(__camFlag, __pirFlag, __fsrFlag))

if __name__ == '__main__':
    main()
    
