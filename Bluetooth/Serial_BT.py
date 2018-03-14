#python 2.x.x - BT serial connection to HC-06
#sends to Arduino and receives back from device
import serial
from time import sleep

bluetoothSerial = serial.Serial("/dev/rfcomm1", baudrate=9600)

count = None
while count == None:
    try:
        count = int(raw_input("Please Enter the number of times to blink the LED: "))
    except:
        pass

bluetoothSerial.write(str(count))
print (bluetoothSerial.readline())
