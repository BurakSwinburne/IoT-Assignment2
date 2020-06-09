import requests
import serial
import time

try:
    ser = None
    ser = serial.Serial('/dev/ttyACM0',9600, timeout=0.500) #timeout=500 milliseconds
    time.sleep(2)

    ser.write("t".encode())
       
    results = ser.read_until(terminator=';', size=16).decode("utf-8")
    humidity, temperature, light = results.split(',')

    ser.close()
    
    r = requests.post("http://ec2-52-87-21-173.compute-1.amazonaws.com/devices/ryansArduino/state", data={'humidity': humidity, 'temperature': temperature, 'light': light})
    print(r.status_code, r.reason)
except:
    print("there was an exception...")
    
    


