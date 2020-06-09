# By Huseyin Erozkan 101546770

from flask import Flask, render_template, request, redirect
from flask import jsonify

import db # The db script

app = Flask(__name__)

###################
#
# Displayable pages
#
###################
@app.route('/')
def main_page():
  # Display what the average temperature is to the user, and then state what setting
  # the heater should be on depending on the rule. Note that the returned value is a
  # tuple, so get the 1st result (at index 0) and the temperature (at index 3)
  temp1 = db.get_latest_state("ryansArduino")[0][3]
  temp2 = db.get_latest_state("Nicholas-Arduino")[0][3]

  avg_temperature = (temp1 + temp2) / 2

  # Get the expected heater setting for the current temperature by getting the first returned
  # row and then the rule name
  setting_result = db.get_setting_from_rule("heater", avg_temperature)[0][1]
  
  return render_template('main.html', sensor_avg_temp=avg_temperature, actuator_setting=setting_result)
  

# Create a UI displaying all the rules and allowing them to be configurable
@app.route('/app/rules')
def rules_page():
  data = db.get_all_rules()
  return render_template('rules.html', data=data)

# Display the arduino's data in table form for the user
@app.route('/app/devices/<arduino_name>')
def device_history_page(arduino_name):
  data = db.get(arduino_name)
  return render_template('devices.html', name=arduino_name, data=data)



###################################################
#
# REST API
# Routing for CRUD operations for the Arduino state
#
###################################################

# Get all the records regarding the Arduino's state, that are stored in the database
# for the specified Arduino. Return all data in JSON form
@app.route('/devices/<arduino_name>/state', methods=['GET'])
def get_device_history(arduino_name):
  result = db.get(arduino_name)
  if not (len(result) > 0):
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
    if not (len(result) > 0):
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



####################################################
#
# REST API
# Routing for CRUD operations for configurable rules
#
####################################################

@app.route('/rules/', methods=['POST', 'GET'])
def rule_add_or_get():

  # Add a new rule to the list of configurable rules
  # This will just be a name, and a threshold value
  if (request.method == "POST"):
    if not ('rulename' in request.values and 'ruledesc' in request.values and 'minval' in request.values and 'maxval' in request.values):
      return "Invalid arguments received. Please add a rulename, ruledesc and thresholdvalue as key-value pairs in the request.", 400  

    rulename = request.values.get('rulename')
    ruledesc = request.values.get('ruledesc')
    minval = request.values.get('minval')
    maxval = request.values.get('maxval')

    if (db.insert_rule(rulename, ruledesc, minval, maxval)):
      return redirect('/app/rules', 200)
    else:
      return "Could not add rule to db", 400

  # Get all rules from DB
  if (request.method == "GET"):
    result = db.get_all_rules()
    if not (len(result) > 0):
      return "Couldn't retrieve any rules", 400
    else:
      return jsonify(result)


@app.route('/rules/<id>', methods=['GET', 'UPDATE', 'DELETE'])
def rule_crud(id):

  # Get rule with current id
  if (request.method == "GET"):
    result = db.get_rule(id)
    if not (len(result) > 0):
      return "Couldn't retrieve rule of given id", 400
    else:
      return jsonify(result[0])

  # Update a rule's name or threshold value
  if (request.method == "UPDATE"):
    if not ('rulename' in request.values and 'ruledesc' and 'minval' in request.values and 'maxval' in request.values):
      return "Invalid arguments received. Please add a rulename and thresholdvalue as key-value pairs in the request.", 400
    
    rulename = request.values.get('rulename')
    ruledesc = request.values.get('ruledesc')
    minval = request.values.get('minval')
    maxval = request.values.get('maxval')
    
    result = db.update_rule(id, rulename, ruledesc, minval, maxval)

    if (result):
      return "Successfully updated rule in db", 200
    else:
      return "Could not update rule in db", 400
  

  # 'Delete' a rule by flipping it's archive value to true
  if (request.method == "DELETE"):
    result = db.delete_rule(id)

    if (result):
      return "Successfully delete rule from db", 200
    else:
      return "Could not delete rule from db", 400



####################################################################################
#
# Routing for CRUD operations, SPECIFICALLY built to allow the website to perform 
# UPDATE and DELETE operations, since browsers and forms don't support those methods
#
####################################################################################

# Browsers don't support UPDATE requests via forms. Therefore, the form used to update
# rule details will call this page, which will then process and update all rules according
# to the values the user gave
@app.route('/processform', methods=['POST'])
def process_form_update_rules():
  id = request.form.getlist('id[]')
  rulename = request.form.getlist('rulename[]')
  ruledesc = request.form.getlist('ruledesc[]')
  minval = request.form.getlist('minval[]')
  maxval = request.form.getlist('maximumval[]')

  # Perform a for-loop to update all values in the db
  i = 0
  amt = len(request.form.getlist('id[]'))
  while i < amt:
    db.update_rule(id[i], rulename[i], ruledesc[i], minval[i], maxval[i])
    i += 1
  
  return redirect('/app/rules')


# Browsers also don't support DELETE requests, therefore we need to create another route
# specifically to provide the ability for the website to delete rules
# Note that this goes against RESTful principles in a way, but there is really no other
# simple option, when it comes to performing a DELETE request via the website itself
@app.route('/deleterule/<id>')
def form_delete_rule(id):
  result = db.delete_rule(id)
  return redirect('/app/rules')



if __name__ == '__main__':
  app.run()