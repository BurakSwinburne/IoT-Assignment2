import requests
from datetime import time
import json
import statistics




def ryanSTD():
    arduino = "ryansArduino"

    r = requests.get("http://ec2-52-87-21-173.compute-1.amazonaws.com/devices/" + arduino + "/state")
    print(r.status_code, r.reason)

   

    if r.status_code == 200:
        json_data = json.loads(r.text)
        json_data
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
                    
            print("the standard deviation for Humidity in ryan's office is: ", stdHum)
            print("the standard deviation for Temperature in ryan's office is: ", stdTemp)
            print("the standard deviation for Light in ryan's office is: ", stdLight)

            r = requests.post("http://ec2-52-87-21-173.compute-1.amazonaws.com/analytics", data={'humidity': stdHum, 'temperature': stdTemp, 'light': stdLight})
            print(r.status_code, r.reason)

def nicholasSTD():
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


def meanRyan():
    arduino = "ryansArduino"

    r = requests.get("http://ec2-52-87-21-173.compute-1.amazonaws.com/devices/" + arduino + "/state")
    print(r.status_code, r.reason)

   

    if r.status_code == 200:
        json_data = json.loads(r.text)
        json_data
        humidity = []
        temperature = []
        light = []
        date_time = []

        for data in json_data:
            humidity.append(data[2])
            temperature.append(data[3])
            light.append(data[4])
            date_time.append(data[5])
                    
            meanHum = statistics.mean(data[2])
            meanTemp = statistics.mean(data[3])
            meanLight = statistics.mean(data[4])
                    
            print("the mean for Humidity in ryan's office is: ", meanHum)
            print("the mean for Temperature in ryan's office is: ", meanTemp)
            print("the mean for Light in ryan's office is: ", meanLight)

            r = requests.post("http://ec2-52-87-21-173.compute-1.amazonaws.com/analytics", data={'humidity': meanHum, 'temperature': meanTemp, 'light': meanLight})
            print(r.status_code, r.reason)

def meanNicholas():
        arduino = "Nicholas-Arduino"

    r = requests.get("http://ec2-52-87-21-173.compute-1.amazonaws.com/devices/" + arduino + "/state")
    print(r.status_code, r.reason)

   

    if r.status_code == 200:
        json_data = json.loads(r.text)
        json_data
        humidity = []
        temperature = []
        light = []
        date_time = []

        for data in json_data:
            humidity.append(data[2])
            temperature.append(data[3])
            light.append(data[4])
            date_time.append(data[5])
                    
            meanHum = statistics.mean(data[2])
            meanTemp = statistics.mean(data[3])
            meanLight = statistics.mean(data[4])
                    
            print("the mean for Humidity in nicholas' office is: ", meanHum)
            print("the mean for Temperature in nicholas's office is: ", meanTemp)
            print("the mean for Light in nicholas' office is: ", meanLight)

            r = requests.post("http://ec2-52-87-21-173.compute-1.amazonaws.com/analytics", data={'humidity': meanHum, 'temperature': meanTemp, 'light': meanLight})
            print(r.status_code, r.reason)

def varianceNicholas():
         arduino = "Nicholas-Arduino"

    r = requests.get("http://ec2-52-87-21-173.compute-1.amazonaws.com/devices/" + arduino + "/state")
    print(r.status_code, r.reason)

   

    if r.status_code == 200:
        json_data = json.loads(r.text)
        json_data
        humidity = []
        temperature = []
        light = []
        date_time = []

        for data in json_data:
            humidity.append(data[2])
            temperature.append(data[3])
            light.append(data[4])
            date_time.append(data[5])
                    
            varHum = statistics.pvariance(data[2])
            varTemp = statistics.pvariance(data[3])
            varLight = statistics.pvariance(data[4])
                    
            print("the variance for Humidity in nicholas' office is: ", varHum)
            print("the variance for Temperature in nicholas's office is: ", varTemp)
            print("the variance for Light in nicholas' office is: ", varLight)

            r = requests.post("http://ec2-52-87-21-173.compute-1.amazonaws.com/analytics", data={'humidity': varHum, 'temperature': varTemp, 'light': varLight})
            print(r.status_code, r.reason)


def varianceRyan():
         arduino = "ryansArduino"

    r = requests.get("http://ec2-52-87-21-173.compute-1.amazonaws.com/devices/" + arduino + "/state")
    print(r.status_code, r.reason)

   

    if r.status_code == 200:
        json_data = json.loads(r.text)
        json_data
        humidity = []
        temperature = []
        light = []
        date_time = []

        for data in json_data:
            humidity.append(data[2])
            temperature.append(data[3])
            light.append(data[4])
            date_time.append(data[5])
                    
            varHum = statistics.pvariance(data[2])
            varTemp = statistics.pvariance(data[3])
            varLight = statistics.pvariance(data[4])
                    
            print("the variance for Humidity in ryan's office is: ", varHum)
            print("the variance for Temperature in ryans's office is: ", varTemp)
            print("the variance for Light in ryan's office is: ", varLight)

            r = requests.post("http://ec2-52-87-21-173.compute-1.amazonaws.com/analytics", data={'humidity': varHum, 'temperature': varTemp, 'light': varLight})
            print(r.status_code, r.reason)

ryanSTD()
nicholasSTD()
meanRyan()
meanNicholas()