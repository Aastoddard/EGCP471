#python 2.x.x - Serial connection between RPi and HC-06
#Receives input from the Arduino Device
#First iteration of the the FSR receive code
import serial
from time import sleep

bluetoothSerial = serial.Serial("/dev/rfcomm1", baudrate=9600)

count = None
flag = 0
while count == None:
    try:
        count = int(raw_input("Send a value greater than zero to handshake. "))
    except:
        pass

bluetoothSerial.write(str(count))
flag = bluetoothSerial.readline()

print flag

try:
    if int(flag) == 1:
        print "Our flag was converted to an INT"
finally:
    print "Our flag couldn't be converted."
