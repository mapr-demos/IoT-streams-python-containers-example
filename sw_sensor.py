#!
"""
sw_sensor.py

Author: Michael F. Aube, 
Email:  maube@mapr.com,  m.f.aube@gmail.com

Developed and tested using Python3, and MapR Sandbox 5.2.1.

Run this file to simulate a sensor that publishes simple events to 
a given MapR Stream topic once every 25 milliseconds.  See the file 
named 'conf.py' to configure the specific name of the MapR Stream 
and topic you wish to use.  This sensor is designed to run forever,
or until you kill it with Ctrl-C.

The default MapR Stream is named:    '/user/user01/iot_stream'
and the default MapR topic is named: 'sensor_data'.

The simple events are representative of an (x,y) point on a graph.
The X-axis represents time (simple integers are used by default), and
the Y-axis represents values that are randomly generated from the
range(1, max_Y).

The JSON form of these simple events is shown below:

   {'id':'sensor_01', 'x':'1', value:'329'}


You can start a sensor in two ways:

   1. Automatically via command line arguments (launch with a script):
      
      user@host$ python3 sw_sensor.py  sensor_id  starting_X  max_Y
      
   2. Interactively, via prompts for sensor_id, starting_X and max_Y:
   
      user@hostname$ python3 sw_senor.py
"""
import sys
import time 
import json
import random
import mapr_kafka_rest as mapr_kafka
    

def initialize_arguments():
   # Check for command line arguments 
   arg_count = len(sys.argv)
   if (arg_count < 2):
      # Interactive start; Prompt operator for sensor specifics...	
      print('DEBUG: Interactive Start...\n')
      sensor_id  = input("Sensor ID (sensor_01|02|03|04) ? ")
      starting_x = int(input("Starting X value (usually 1) ? "))
      max_y_val  = int(input("Max Y value (5000|35|120|6500) ? "))
   elif (arg_count == 4):
      # Grab the command line arguments
      print('DEBUG: Automatic Start...\n')
      sensor_id  = str(sys.argv[1])
      starting_x = int(sys.argv[2])
      max_y_val  = int(sys.argv[3])
   else:
      sys.exit("Usage error, try:  python3 sw_sensor.py  sensor_id  starting_X  max_Y \n")

   return str(sensor_id), int(starting_x), int(max_y_val)


# Set up some reusable values
sensor_data_topic = '/user/user01/iot_stream:sensor_data'
FIVE_MS = 0.05

# Get startup argument values
sensor_id, starting_x, max_y_val = initialize_arguments()

x = starting_x
# Generate and POST random sensor events forever...
while (True):
    # Create a sensor event as "JSON" using a Python dictionary
    event = {}
    event['id']    = sensor_id
    event['x']     = str(x)
    event['value'] = str(random.randint(1, max_y_val))

    # Publish the sensor event to the MapR Stream topic
    response = mapr_kafka.post_topic_message(sensor_data_topic, event)
    if (response.status_code == 200):
        print(sensor_id + " Has POSTed an event: " + str(event))
    else:
        print('ERROR: %d "%s"' % (response.status_code,response.reason))
    time.sleep(FIVE_MS)
    x += 1 


