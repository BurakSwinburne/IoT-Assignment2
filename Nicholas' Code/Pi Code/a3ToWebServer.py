import serial
import MySQLdb as mdb
import time
from datetime import datetime
import requests



device = "/dev/ttyACM0"
#device = "/dev/ttyAMA0"


arduino = serial.Serial(device,9600)
arduinoName = "Nicholas-Arduino"

Now= datetime.now()
current = Now.strftime("%H%M%S")

Start = time.time()


dataStart = arduino.readline()
data = arduino.readline()
#intdata = int(data)
#print(intdata)
print(dataStart)
print(data)

time.sleep(2)
data = arduino.readline()
dataset = data.split("\t")
time.sleep(2)
data = arduino.readline()
dataset=data.split("\t")

humidity = dataset[0]
temperature = dataset[1]
light = dataset[2]

intTemp = ''.join(x for x in temperature if x.isdigit())
intHum = ''.join(x for x in humidity if x.isdigit())
intLight = ''.join(x for x in light if x.isdigit())

print(intTemp)
print(intHum)
print(intLight)

print(temperature)


print("Time is " + current)

r = requests.post("http://ec2-52-87-21-173.compute-1.amazonaws.com/devices/Nicholas-Arduino/state", data={'humidity': '65', 'temperature': '15', 'light': '255'})
print(r.status_code, r.reason)


