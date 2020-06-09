import numpy as np
from flask import jsonify
from datetime import time
import json

import db # The db script

def get_analytics():
  ryans_analytics = get_analytics_for_device("ryansArduino")
  nicholas_analytics = get_analytics_for_device("Nicholas-Arduino")

  all_analytics = [ryans_analytics, nicholas_analytics]

  return all_analytics


def get_analytics_for_device(arduino_name):

  data = db.get(arduino_name)

  humidity = []
  temperature = []
  light = []
  date_time = []

  for row in data:
    humidity.append(row[2])
    temperature.append(row[3])
    light.append(row[4])
    date_time.append(row[5])

  # Get the std, mean and variance for each sensor and format them to 3 decimal places
  
  # Get the std deviation of each sensor
  stdHum = '{0:.3f}'.format(np.std(humidity))
  stdTemp = '{0:.3f}'.format(np.std(temperature))
  stdLight = '{0:.3f}'.format(np.std(light))

  # Get the mean of each sensor's values
  meanHum = '{0:.3f}'.format(np.mean(humidity))
  meanTemp = '{0:.3f}'.format(np.mean(temperature))
  meanLight = '{0:.3f}'.format(np.mean(light))

  # Get the variance of each sensor's values
  varHum = '{0:.3f}'.format(np.var(humidity))
  varTemp = '{0:.3f}'.format(np.var(temperature))
  varLight = '{0:.3f}'.format(np.var(light))
  
  
  return { "arduino_name": arduino_name, \
    "std": { "temp": stdTemp, "humidity": stdHum, "light": stdLight}, \
      "mean": { "temp": meanTemp, "humidity": meanHum, "light": meanLight}, \
        "variance": { "temp": varTemp, "humidity": varHum, "light": varLight }}

  # return { arduino_name: { \
  #   "std": { "temp": stdTemp, "humidity": stdHum, "light": stdLight}, \
  #     "mean": { "temp": meanTemp, "humidity": meanHum, "light": meanLight}, \
  #       "variance": { "temp": varTemp, "humidity": varHum, "light": varLight }}}
  