import serial
import time
import MySQLdb
import schedule # Use this to turn off the system every night
import datetime
import json
import urllib2


ser = serial.Serial()

ser.port = "/dev/ttyACM0"
ser.baudrate = 115200
ser.open()


# Retrieve the given Arduino's current state
def retrieve_latest_data(arduinoName):
    if (arduinoName == "HuseyinsArduino" \
        or arduinoName == "Nicholas-Arduino" \
            or arduinoName == "ryansArduino"):

        response = urllib2.urlopen("http://ec2-52-87-21-173.compute-1.amazonaws.com/devices/" + arduinoName + "/state/")
        data = json.loads(response.read())    
        return data
    else:
        print("unrecognised arduino name")


# This function runs routinely, to gather data from the MySQL DB
def routine_job():
    ryansData = retrieve_latest_data("ryansArduino")
    nicholasData = retrieve_latest_data("Nicholas-Arduino")
    
    # NOTE: below avg temp calculation is for debugging purposes only
    #[0]: record id
    #[1]: arduino name
    #[2]: Humidity
    #[3]: Temperature
    #[4]: Light
    #[5]: Timestamp
    #[6]: Whether it's been archived or not
    
    avgTemp = (ryansData[3] + nicholasData[3]) / 2
    print("Approximate temp right now is:")
    print(avgTemp)
    
    # Get the setting that the heater should be on from the web server
    response = urllib2.urlopen("http://ec2-52-87-21-173.compute-1.amazonaws.com/rules/heater:/mode/")
    setting = str(json.loads(response.read())[1])
    
    print(setting)
    ser.write(setting) # Tell the Arduino what setting the heater should be on
            
        
# Schedule a function to run every so often
schedule.every(3).seconds.do(routine_job)

while 1:
    schedule.run_pending()
    time.sleep(1)

ser.close()

