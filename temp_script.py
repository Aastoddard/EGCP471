import datetime
import time

from Adafruit_SHT31 import *
#logging.basicConfig(filename='example.log',level=logging.DEBUG)

sensor = SHT31(address = 0x44)
#sensor = SHT31(address = 0x45)
now = datetime.datetime.now()

#Global Variables:
heatFlag = 0


#----------Sensor Initialization---------#
def print_status():
    status = sensor.read_status()
    is_data_crc_error = sensor.is_data_crc_error()
    is_command_error = sensor.is_command_error()
    is_reset_detected = sensor.is_reset_detected()
    is_tracking_temperature_alert = sensor.is_tracking_temperature_alert()
    is_tracking_humidity_alert = sensor.is_tracking_humidity_alert()
    is_heater_active = sensor.is_heater_active()
    is_alert_pending = sensor.is_alert_pending()

#-------------Temperature Reading Function-------------#
def temp_Reading():
    while(True):
        degreesCelsius = sensor.read_temperature()
        degreesFahrenheit = 9.0/5.0 * degreesCelsius + 32
        humidity = sensor.read_humidity()
        date = time.strftime("%m-%d-%Y")
        currentDatetime = time.strftime("%m-%d-%Y %H:%M %p")
        
        print_status()
        print currentDatetime #print current time and date; for logging
        print 'Temp             = {0:0.3f} deg F'.format(degreesFahrenheit) #Fahrenheit
        print 'Humidity         = {0:0.2f} %'.format(humidity)
        #print 'Temp             = {0:0.3f} deg C'.format(degreesCelsius) #Celsius for troubleshooting

        #set temperature for flag
        if degreesFahrenheit > 85:
            print "Warning! Temperature is above 85 Degrees!" 
            heatFlag = 1
             
        else:
            heatFlag = 0
            
        print heatFlag #for troubleshooting
        time.sleep(1)



        sensor.clear_status()
        sensor.set_heater(True)
        print_status()

        sensor.set_heater(False)
        print_status()
            
            
        
#-------------MAIN-------------#
temp_Reading()



