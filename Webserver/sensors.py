import db

# Get the approximate temperature of the office by averaging out the current
# temperature of all Arduino temperature sensor values
def get_approximate_temperature():
  # Note that the returned value is a tuple, so get the 1st result (at index 0) 
  # and the temperature (at index 3)
  temp1 = db.get_latest_state("ryansArduino")[0][3]
  temp2 = db.get_latest_state("Nicholas-Arduino")[0][3]

  return (temp1 + temp2) / 2


# Insert a new state, which is a collection of an Arduino's sensor values,
# into the database.
def insert_new_state(arduino_name, request):
  # Ensure that the client has sent all the valid data required
  if not ('temperature' in request.values and 'light' in request.values and 'humidity' in request.values):
    return False

  humidity = request.values.get('humidity')
  temperature = request.values.get('temperature')
  light = request.values.get('light')
  
  # If state successfully recorded
  if (db.insert(arduino_name, humidity, temperature, light)):
    return True
  else:
    return False


# Update a state's sensor values
def update_state(arduino_name, id, request):
  # Ensure that the client has sent all the valid data required
  if not ('temperature' in request.values and 'light' in request.values and 'humidity' in request.values):
    return False

  humidity = request.values.get('humidity')
  temperature = request.values.get('temperature')
  light = request.values.get('light')
  
  # If state successfully recorded
  if (db.update_state(humidity, temperature, light, id)):
    return True
  else:
    return False
