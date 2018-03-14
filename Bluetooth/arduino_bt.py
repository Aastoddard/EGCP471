#python 2.x.x - Serial connection between RPi and HC-06
#Receives input from the Arduino Device
#First iteration of the the FSR receive code
import serial
from time import sleep

bluetoothSerial = serial.Serial("/dev/rfcomm1", baudrate=9600)

count = None
escape = raw_input()
while count == None:
    try:
        if escape == 'q':
            break
        else:
            count = bluetoothSerial.readline()
    except:
        pass

print("Pi code exited with count as: ", count)
