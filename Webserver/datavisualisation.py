import db
from flask import Flask, render_template

def display_chart_data(arduino_name):
  results = db.get(arduino_name)

  # there are rows returned
  if (len(results) > 0):

      humidity = []
      temperature = []
      light = []
      date_time = []

      for row in results:
          humidity.append(row[2]) # OR humidity.append(row['humidity'])
          temperature.append(row[3])
          light.append(row[4])
          date_time.append(row[5])

      return render_template('chart.html', arduino=arduino_name, humidity=humidity, temperature=temperature, light=light, labels=date_time)
  else:
      return "There was an error getting the arduino data :(", 400