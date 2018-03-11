#-------------------------------------------------------------#
#                                                             #
# PIR I/O Class Code                                          #
#                                                             #
# Contributors:                                               #
#   Aaron Stoddard                                            #
#                                                             #
# Developed using PIR Code from:                              #
#   Aaron Stoddard                                            #
#   Troy Wise                                                 #
#                                                             #
# Last Updated: 10 March 2018                                 #
#                                                             #
# The PIR outputs a steady 3.3v when it receives a positive   #
# hit from the on board sensor. This code acts as a working   #
# model of how we will handle the PIR output as a main module #
# input. We will use the active signal to drive a number of   #
# CRON wakeups and script executions.                         #
#                                                             #
# The class is designed to encapsulate the PIR functionality  #
# from the master script. It's basic functions are to         #
# initialize the GPIO required to operate the PIR, poll for a #
# PIR 'hit' and then return a software flag that will be used #
# to drive other functions within the master script.          #
#                                                             #
#-------------------------------------------------------------#

import RPi.GPIO as GPIO
import cfg

class PIR:

    #-------------------------  __init__  -------------------------#
    # will run when class first created, initializes the GPIO      #
    # setup for the board.                                         #
    #--------------------------------------------------------------#
    def __init__(self):        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(cfg.InputPin, GPIO.IN)
        GPIO.setup(cfg.OutputPin, GPIO.OUT)
        
        print(cfg.InputPin, cfg.OutputPin) #debug print

    #-------------------------  destroy  -------------------------#
    # releases and clears the GPIO resources                      #
    #-------------------------------------------------------------#
    def destroy(self):
        GPIO.cleanup()

    #-------------------------  runMode  -------------------------#
    # executes the PIR into a polling state waiting for a         #
    # positive hit from the PIR to return a 'hit' flag            #
    #-------------------------------------------------------------#
    def runMode(self):
        __returnFlag = 0

        try:
            while True:
                if GPIO.input(cfg.InputPin):
                    print('PIR captured movement') #debug print
                    GPIO.output(cfg.OutputPin, 1)
                    __returnFlag = 1
                    break
                else:
                    GPIO.output(cfg.OutputPin, 0)
        finally:
            print('returned from run mode') #debug print
            return __returnFlag

    #-------------------------  returnFlag  ------------------------#
    # calls runMode to set and return the value for returnFlag      #
    # ideally returnFlag will always return a '1'                   #
    #---------------------------------------------------------------#
    def returnFlag(self):
         flag = self.runMode()

         return flag
        
        
            
    
