# By Huseyin Erozkan 101546770

from flask import Flask, render_template, request, redirect
from flask import jsonify
import json
import analytics # The analytics script
import db # The db script
import sensors as states # Script for CRUD operations for sensors and arduino states
import datavisualisation as dataviz # Script for data visualisation

app = Flask(__name__)

###################
#
# Displayable pages
#
###################

# Main page. Display the approximate temperature and the current setting
# that the actuator should be on depending on the rule's value
@app.route('/')
def main_page():
  # Get approximate temperature of office
  approx_temp = states.get_approximate_temperature()

  # Get the expected heater setting for the current temperature by getting the first returned
  # row and then the rule name
  setting_result = db.get_setting_from_rule("heater", approx_temp)[0][1]
  
  return render_template('main.html', sensor_avg_temp=approx_temp, actuator_setting=setting_result)
  

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


# Display the visualised data of a given device
@app.route('/devices/<arduino_name>/display', methods=['GET'])
def chart(arduino_name):
  return dataviz.display_chart_data(arduino_name)


# Display the analytics page
@app.route('/analytics')
def statistical_analysis(methods=['GET']):  
  return render_template('analytics.html', data=analytics.get_analytics())


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


# Routing used for CREATE and READ operations
@app.route('/devices/<arduino_name>/state/', methods=['GET', 'POST'])
def create_or_get_state(arduino_name):

  # Add a new record regarding the current state of a specified Arduino
  if (request.method == 'POST'):
    if (states.insert_new_state(arduino_name, request)):
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


# Routing used for GET, PUT and DELETE operations. This route, unlike the previous, 
# also includes an id as a variable
@app.route('/devices/<arduino_name>/state/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def crud_by_id(arduino_name, state_id):

  # Retrieve state by id
  if (request.method == 'GET'):
    result = db.get_state_by_id(state_id)

    if (result):
      return jsonify(result)
    else:
      return "Could not get record of state of given id", 400
    

  # The client device wants to update a specific entry in the database
  if (request.method == 'PUT'):
    result = states.update_state(arduino_name, state_id, request)
    
    if (result):
      return "Record was successfully updated", 200
    else:
      return "Error, could not update record", 400
  

  # Delete a record of arduino's state from the DB
  elif (request.method == 'DELETE'):
    if (db.delete(arduino_name, state_id)):
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

  # Add a new rule to the list of configurable rules. This will just be a name, and a threshold value
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

  # Get details of rule with current id
  if (request.method == "GET"):
    result = db.get_rule(id)
    if not (len(result) > 0):
      return "Couldn't retrieve rule of given id", 400
    else:
      return jsonify(result[0])

  # Update a rule of given id
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


# Get what 'mode' the actuator arduino should be in, depending on the set or category of rules
# the rulename passed in should be a string formatted as so: '<rulename>:', so for exampled: 'heater:'
# This is used so that the actuator Pi can retrieve the configurable threshold values from the server
@app.route('/rules/<rulename>/mode/', methods=['GET'])
def get_mode_from_rule(rulename):

  # NOTE: Currently only rules for the heater are implmented
  if (rulename == "heater:"):
    # Get avg temperature to see what setting the heater should be in, depending
    # on the min temperature and max temperature values in the database
    temp1 = db.get_latest_state("ryansArduino")[0][3]
    temp2 = db.get_latest_state("Nicholas-Arduino")[0][3]
    avg_temperature = (temp1 + temp2) / 2

    setting_result = db.get_setting_from_rule(rulename, avg_temperature)[0]
    
    return jsonify(setting_result)

  return "Rulename not recognised", 400

####################################################################################
#
# Routing for CRUD operations, SPECIFICALLY built to allow the website to perform 
# PUT and DELETE operations, since browsers and forms don't support those methods
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