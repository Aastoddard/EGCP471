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

bd_addr = "98:D3:31:FC:A9:EB"   #define mac address of unit
port = 1    #default port
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)  #define the socket comm protocol
sock.connect((bd_addr, port))   #establish connection

data = ""

while 1:
    try:
        #If we want to append data, rewrite data as: data += sock.recv(1024)
        data = sock.recv(1024)  #socket.receive(buffer size)
        data_end = data.find('\n')  #end of data is newline char
        #if not end of data - print data
        if data_end != -1:
            print (data)
            #uncomment below for append data: start of data is current char if not sentinel
            #data = data[data_end+1:]
        #uncomment below for digital high/low signal
        #if data == '1':
            #debug print
            #print "Software Flag Set"
    except KeyboardInterrupt:   #ctrl + c
        break
sock.close()    #close the socket connect and free the bluetooth device
