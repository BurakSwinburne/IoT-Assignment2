# By Huseyin Erozkan 101546770

# # This script is used to connect to and interface with the DB
import MySQLdb

dbConn = MySQLdb.connect('db-iot-101546770-assignment2.cr5by9cixfkc.us-east-1.rds.amazonaws.com', 'webserver', '<password goes here>', 'assign2')

# First set the session time zone, since the mysql db's global time zone cannot be changed, due to lack of SUPER priveleges
with dbConn:
  cursor = dbConn.cursor()
  cursor.execute('SET time_zone = \"+10:00\"')
  dbConn.commit()
  cursor.close()



# Insert a new record into the database
# Return True if DB insertion work, otherwise False
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
        WHERE arduinoName = %s;
        """, [arduino_name])
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
        WHERE arduinoName = %s
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



# Get all records of a specific sensor from a specified Arduino
def get_sensor(arduino_name, sensor):
  return "get"



# Delete a record of an Arduino state. Note that this doesn't actually delete the record,
# but rather sets the record's archive value to true, meaning that SELECT and UPDATE
# operations will ignore will the record
def delete(arduino_name, id):
  try:
    with dbConn:
      cursor = dbConn.cursor()

      # If no id was specified, archive the latest entry that isn't already archived
      if (id is none):
        affected_count = cursor.execute("""
          UPDATE assign2 SET archive = 1
          WHERE archive = 0 AND arduinoName = %s
          ORDER BY id DESC
          LIMIT 1;
          """, [arduino_name])
        dbConn.commit()
        return affected_count == 1
      
      # Id was specified, so update that particular entry
      else:
        affected_count = cursor.execute("""
          UPDATE assign2 SET archive = 1
          WHERE archive = 0 AND arduinoName = %s AND id = $s
          ORDER BY id DESC
          LIMIT 1;
          """, [arduino_name, id])
        dbConn.commit()
        return affected_count == 1

  except MySQLdb.IntegrityError:
    return false
  finally: # This will always run, even if there is a return statement in the try/catch block
    cursor.close()