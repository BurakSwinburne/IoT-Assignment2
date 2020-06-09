# By Huseyin Erozkan 101546770

# This script is used to connect to and interface with the DB
import MySQLdb
from config import DB_PASSWORD # import the db password via the config.py file - to prevent leaking the password again
 
dbConn = MySQLdb.connect('db-iot-101546770-assignment2.cr5by9cixfkc.us-east-1.rds.amazonaws.com', 'webserver', DB_PASSWORD, 'assign2')

# First set the session time zone, since the mysql db's global time zone cannot be changed, due to lack of SUPER priveleges
with dbConn:
  cursor = dbConn.cursor()
  cursor.execute('SET time_zone = \"+10:00\"')
  dbConn.commit()
  cursor.close()


# Insert a new record into the database. Return True if DB insertion work, otherwise False
def insert(arduino_name, humidity, temperature, light):
  
  try:
    with dbConn:
      cursor = dbConn.cursor()
      affected_count = cursor.execute("""
        INSERT INTO state (arduinoName, humidity, temperature, light, timestamp)
        VALUES (%s, %s, %s, %s, NOW());
        """
        , (arduino_name, humidity, temperature, light))
      dbConn.commit()
    return True
  except MySQLdb.IntegrityError:
  #except Exception:
    return False
  finally: # This will always run, even if there is a return statement in the try/catch block
    cursor.close()
  


# Get all records for a specified Arduino
def get(arduino_name):
  try:
    with dbConn:
      cursor = dbConn.cursor()
      cursor.execute("""
        SELECT * FROM state
        WHERE arduinoName = %s AND archive = 0;
        """, [arduino_name])
      dbConn.commit()
      result = cursor.fetchall()
      return result
  except MySQLdb.IntegrityError:
    return None
  finally: # This will always run, even if there is a return statement in the try/catch block
    cursor.close()


# Get the state via id. Return none if a record of the given id isn't found
def get_state_by_id(id):
  try:
    with dbConn:
      cursor = dbConn.cursor()
      cursor.execute("""
        SELECT * FROM state
        WHERE id = %s
        """, [id])
      dbConn.commit()
      result = cursor.fetchall()
      return result
  except MySQLdb.IntegrityError:
    return None
  finally: # This will always run, even if there is a return statement in the try/catch block
    cursor.close()



# Get the latest state of a specified Arduino.
# Return the state if the arduino of specified name exists, otherwise return none
def get_latest_state(arduino_name):
  try:
    with dbConn:
      cursor = dbConn.cursor()
      cursor.execute("""
        SELECT * FROM state
        WHERE arduinoName = %s AND archive = 0
        ORDER BY id
        DESC LIMIT 1;
        """, [arduino_name])
      dbConn.commit()
      result = cursor.fetchall()
      return result
  except MySQLdb.IntegrityError:
    return None
  finally: # This will always run, even if there is a return statement in the try/catch block
    cursor.close()


def update_state(humidity, temperature, light, id):
  #return id

  try:
    with dbConn:
      cursor = dbConn.cursor()
      cursor.execute("""
        UPDATE state
        SET humidity = %s, temperature = %s, light = %s
        WHERE id = %s;
        """, [humidity, temperature, light, id])
      dbConn.commit()
      return cursor.rowcount == 1
  except MySQLdb.IntegrityError:
    return False
  finally: # This will always run, even if there is a return statement in the try/catch block
    cursor.close()

# Delete a record of an Arduino state. Note that this doesn't actually delete the record,
# but rather sets the record's archive value to true, meaning that SELECT and UPDATE
# operations will ignore will the record
def delete(arduino_name, id):
  try:
    with dbConn:
      cursor = dbConn.cursor()
      cursor.execute("""
        UPDATE state 
        SET archive = 1
        WHERE archive = 0 AND arduinoName = %s AND id = %s
        """, [arduino_name, id])
      dbConn.commit()
      return cursor.rowcount == 1
  except MySQLdb.IntegrityError:
    return false
  finally: # This will always run, even if there is a return statement in the try/catch block
    cursor.close()




def insert_rule(rule_name, ruledesc, min_val, max_val):
  try:
    with dbConn:
      cursor = dbConn.cursor()
      affected_count = cursor.execute("""
        INSERT INTO rules (rulename, ruledesc, minval, maxval)
        VALUES (%s, %s, %s, %s);
        """
        , (rule_name, ruledesc, min_val, max_val))
      dbConn.commit()
    return True
  except MySQLdb.IntegrityError:
  #except Exception:
    return False
  finally: # This will always run, even if there is a return statement in the try/catch block
    cursor.close()


# Get the rule of given id
def get_rule(id):
  try:
    with dbConn:
      cursor = dbConn.cursor()
      cursor.execute("""
        SELECT * FROM rules
        WHERE id = %s;
        """, id)
      dbConn.commit()
      result = cursor.fetchall()
      return result
  except MySQLdb.IntegrityError:
    return None
  finally: # This will always run, even if there is a return statement in the try/catch block
    cursor.close()


# Get all active rules (rules that aren't archived)
def get_all_rules():
  try:
    with dbConn:
      cursor = dbConn.cursor()
      cursor.execute("""
        SELECT * FROM rules
        WHERE archive = 0;
        """)
      dbConn.commit()
      result = cursor.fetchall()
      return result
  except MySQLdb.IntegrityError:
    return None
  finally: # This will always run, even if there is a return statement in the try/catch block
    cursor.close()


# Update a rule
def update_rule(id, rule_name, rule_desc, min_val, max_val):
  try:
    with dbConn:
      cursor = dbConn.cursor()
      cursor.execute("""
        UPDATE rules
        SET rulename = %s, ruledesc = %s, minval = %s, maxval = %s
        WHERE id = %s;
        """, [rule_name, rule_desc, min_val, max_val, id])
      dbConn.commit()
      return True
  except MySQLdb.IntegrityError:
    return False
  finally: # This will always run, even if there is a return statement in the try/catch block
    cursor.close()


def delete_rule(id):
  try:
    with dbConn:
      cursor = dbConn.cursor()
      cursor.execute("""
        UPDATE rules
        SET archive = 1
        WHERE id = %s;
        """, [id])
      dbConn.commit()
      return True
  except MySQLdb.IntegrityError:
    return False
  finally: # This will always run, even if there is a return statement in the try/catch block
    cursor.close()


# Find what the current setting of the actuator arduino should be, based on what the average value is.
# In our case, what the average temperature is between the 2 sensor arduinos.
def get_setting_from_rule(rule_name, current_value):
  try:
    with dbConn:
      cursor = dbConn.cursor()

      param = rule_name + "%" # Need to format it as so in order to insert parametised wildcard
      # Find what heater setting should currently be running
      cursor.execute("""
        SELECT * from rules
        WHERE rulename LIKE %s
        AND archive = 0
        AND minval <= %s
        AND maxval > %s
        LIMIT 1;
        """, [param, current_value, current_value])
      dbConn.commit()
      result = cursor.fetchall()
      return result
  except MySQLdb.IntegrityError:
    return None
  finally: # This will always run, even if there is a return statement in the try/catch block
    cursor.close()