import numpy as np
import requests
from datetime import time
import json
import statistics

arduino =  "Nicholas-Arduino"

r = requests.get("http://ec2-52-87-21-173.compute-1.amazonaws.com/devices/" + arduino + "/state")
print(r.status_code, r.reason)

   

if r.status_code == 200:
   json_data = json.loads(r.text)
   humidity = []
   temperature = []
   light = []
   date_time = []

     
   for data in json_data:
       humidity.append(data[2])
       temperature.append(data[3])
       light.append(data[4])
       date_time.append(data[5])


       stdHum = statistics.pstdev(data[2])
       stdTemp = statistics.pstdev(data[3])
       stdLight = statistics.pstdev(data[4])
            
       print("the standard deviation for Humidity in Nicholas' office is: ", stdHum )
       print("the standard deviation for Temperature in Nicholas' office is: ",stdTemp)
       print("the standard deviation for Light in Nicholas' office is: ", stdLight)

       r = requests.post("http://ec2-52-87-21-173.compute-1.amazonaws.com/analytics", data={'humidity': stdHum, 'temperature': stdTemp, 'light': stdLight})
       print(r.status_code, r.reason)
