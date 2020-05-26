import serial
import MySQLdb as mdb
import time
from datetime import datetime



device = "/dev/ttyACM0"
#device = "/dev/ttyAMA0"


arduino = serial.Serial(device,9600)

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


conn = mdb.connect('localhost', 'root', 'root', 'assingment3DB') or die("Couldnt connect to db") ;


cursor = conn.cursor()
cursor.execute("""INSERT INTO log VALUES(NULL,%s,%s,%s,%s)""" % (current,intLight,intTemp,intHum))
conn.commit()
cursor.close()