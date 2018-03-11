#-------------------------------------------------------------#
#                                                             #
# PIR I/O Signal Driver Code                                  #
#                                                             #
# Contributors:                                               #
#   Aaron Stoddard                                            #
#   Troy Wise                                                 #
#                                                             #
# Last Updated: 20 February 2018                              #
#                                                             #
# The PIR outputs a steady 3.3v when it receives a positive   #
# hit from the on board sensor. This code acts as a working   #
# model of how we will handle the PIR output as a main module #
# input. We will use the active signal to drive a number of   #
# CRON wakeups and script executions.                         #
#                                                             #
# The PIR has a 5v power input, a 3.3v output and a ground    #
# pin. The unit is given power and ground from the RPi module #
# The output is connected to physical pin 11 on the RPI GPIO  #
# breakout. Pin 12 is used as an output pin to drive a simple #
# LED circuit.                                                #
#                                                             #
#-------------------------------------------------------------#

import RPi.GPIO as GPIO

#----------  GPIO SETUP  ----------#
InputPin = 11  #pin11
LedPin = 12    #pin12

def setup():
    GPIO.setmode(GPIO.BOARD)       #numbers GPIOs by physical location
    GPIO.setup(InputPin, GPIO.IN)  #Set InputPin to in
    GPIO.setup(LedPin, GPIO.OUT)   #Sets LedPin to out

#----------   CLEANUP  ----------#
def destroy():
    GPIO.cleanup()                 #release GPIO resources
 

#----------   MAIN  ----------#

setup()  # execute GPIO setup 

try:
    while True:
        if GPIO.input(InputPin):    # if input pin 12 is high from PIR output
            print('PIR is on.')
            GPIO.output(LedPin, 1)  # set our LED output pin to high
        else:
            print('PIR is off')
            GPIO.output(LedPin, 0)  # else, LED pin is low
        
finally:
    destroy()





