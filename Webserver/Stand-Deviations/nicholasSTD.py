
import numpy as np
import requests
from datetime import time


    r = requests.get("http://ec2-52-87-21-173.compute-1.amazonaws.com/devices/" + arduino + "/state")
    print(r.status_code, r.reason)

    arduino = "Nicholas-Arduino"

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
            
            print("the standard deviation for Humidity in Nicholas' office is: ", npass.std(data[2]))
            print("the standard deviation for Temperature in Nicholas' office is: ", npass.std(data[3]))
            print("the standard deviation for Light in Nicholas' office is: ", npass.std(data[4]))
