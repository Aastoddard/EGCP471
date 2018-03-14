#Python 3.x.x - BT connection between Arduino HC-06 and Pi
#Sends input to Arduino, does not receive
import bluetooth

bd_addr = "98:D3:31:FC:A9:EB"
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

while 1:
    tosend = input()
    if tosend != 'q':
        sock.send(tosend)
    else:
        break

sock.close()
