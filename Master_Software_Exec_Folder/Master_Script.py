# Master Script Execution

from modules import *

#PIR and Camera Flags
pirFlag = 0
camFlag = 0

#create PIR class and set the PIR flag
myPIR = PIR()
pirFlag = myPIR.returnFlag()

#debug print
print('PIR flag returned ', pirFlag)

#placeholder behavior execution
if pirFlag == 1:
    #create camera class and set camera flag
    myCam = FacialRec()
    camFlag = myCam.returnFlag()
    #debug print
    print('Camera Flag is ', camFlag)
else:
    #debug print
    print('no PIR Flag, no Cam Flag')

#release GPIO
myPIR.destroy()



    
