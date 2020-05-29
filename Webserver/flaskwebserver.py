from flask import Flask
from flask import request
from flask import jsonify
import db # The db script

app = Flask(__name__)

@app.route('/')
def main_page():
  # TODO: Add a home page here
  return 'Hello from Flask!'

# Get all the records regarding the Arduino's state, that are stored in the database
# for the specified Arduino. Return all data in JSON form
@app.route('/devices/<arduino_name>/state', methods=['GET'])
def get_device_history(arduino_name):
  result = db.get(arduino_name)
  if (result is None):
    return "The specified device not exist in the database", 400
  else:
    return jsonify(result) # Return all the data stored for the specified arduino


# Routing used for the CRUD operations. 
@app.route('/devices/<arduino_name>/state/', methods=['GET', 'POST', 'UPDATE', 'DELETE'])
def sensor_crud(arduino_name):

  # Add a new record regarding the current state of a specified Arduino
  if (request.method == 'POST'):    
    # Ensure that the client has sent all the valid data required
    if not ('temperature' in request.values and 'light' in request.values and 'humidity' in request.values):
      return "Invalid arguments received. Please pass in all sensors and their values as key-value pairs in the request.", 400

    humidity = request.values.get('humidity')
    temperature = request.values.get('temperature')
    light = request.values.get('light')
    
    # If state successfully recorded
    if (db.insert(arduino_name, humidity, temperature, light)):
      return "Arduino's state was recorded in the database", 200
    else:
      return "Error. Could not store data in database", 400


  # Get the requested Arduino's latest state as recorded in the database 
  elif (request.method == 'GET'):
    result = db.get_latest_state(arduino_name)
    if (result is None):
      return "The specified device not exist in the database", 400
    else:
      return jsonify(result[0]) # Return the Arduino's current state


  # The client device wants to update a specific entry in the database
  elif (request.method == 'UPDATE'):
    return "ERROR"

  

  # The client device wants to delete an entry in the database
  # Note that this won't actually delete the entry. Instead, the database is designed
  # such that each entry has an 'archive' boolean value that's false by default, 
  # which will be flipped to true.
  elif (request.method == 'DELETE'):
    if (db.delete(arduino_name, None)):
      return "Record was deleted from the database", 200
    else:
      return "Error. Could not remove record from database", 400



if __name__ == '__main__':
  app.run()