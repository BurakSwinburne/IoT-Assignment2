from flask import Flask
from flask import render_template
from datetime import time
import requests
import json

 
app = Flask(__name__)
 
 
@app.route("/")
def chart():

    # TODO: USE THE ROUTING TO SELECT WHAT ARDUINO WE USE
    arduino = "ryansArduino"

# TODO: MAKE SURE THIS SECTION PULLS DATA CORRECTLY, MIGHT WANT IT TO DIRECTLY PULL FROM DB... UP TO YOU
    r = requests.get("http://ec2-52-87-21-173.compute-1.amazonaws.com/devices/" + arduino + "/state")
    print(r.status_code, r.reason)
# ~~~~~~~~~~~~~~

    if r.status_code == 200:

        # MIGHT HAVE TO CHANGE THIS DEPENDING ON HOW THE DB DATA IS OBTAINED
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

        print(r.status_code, r.reason)
        return render_template('chart.html',arduino=arduino, humidity=humidity, temperature=temperature, light=light, labels=date_time)
    else:
        return "There was an error getting the arduino data :("
 
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)