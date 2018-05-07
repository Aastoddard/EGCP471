#-----------------------------------------------------------#
#                                                           #
#               FSR Analog Bluetooth Script                 #
#                                                           #
#  Contributors:                                            #
#       Aaron Stoddard                                      #
#                                                           #
#  Last Update: 15 March 2018                               #
#                                                           #
#  This script is designed to connect to a specific BT      #
#  device by passing in a mac address in order to create    #
#  a socket connection. Data being received is of type      #
#  string. In the final code variant this data will be      #
#  cast as type intand used to generate a software flag. At #
#  the originating point the data is a float value. The     #
#  data being sent has a sentinel value appended to it to   #
#  signify the end of useable data. The sentinel for this   #
#  setup is the newline character. Currently the program    #
#  runs in an infinite while loop and can only be           #
#  interrupted by the keyboard interrupt shorcut: ctrl + c. #                                      #
#                                                           #
#  The program can be modified to run with a digital input  #
#  instead of the current analog configuration. The code    #
#  can also be used to append the received information      #
#  rather than overwriting the data variable on each loop   #
#  iteration. The process to do this is outlined in the     #
#  code comments.                                           #
#                                                           #
#-----------------------------------------------------------#

import bluetooth
import time

bd_addr = "98:D3:51:FD:71:76"   #define mac address of unit
port = 1    #default port
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)  #define the socket comm protocol
sock.connect((bd_addr, port))   #establish connection

data = ""

while 1:
    try:
        data = input()
        if data == '1':
            sock.send(data)
        else:
            time.sleep(25)
            
    except KeyboardInterrupt:   #ctrl + c
        break
sock.close()    #close the socket connect and free the bluetooth device
