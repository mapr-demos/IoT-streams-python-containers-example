"""
event_filter.py

Use this file to run a "fan out" filter for the sensor events.
The filter will consume events from the main 'sensor_data' topic,
and then republish those sensor events on the four individual sensor
topics, according to the value of the 'sensor_id' attribute in each
event.
"""

import config
import time
import mapr_kafka_rest as mapr_kafka
    
# Set up some reusable values
FIVE_MS = 0.05
offset = 0

print('\nEvent filter started on topic: ' + config.MAPR_STREAM_PATH_TOPIC + '. \n')
print('Initializing event filter... Please wait.\n')

# Consume, filter and rePOST sensor events forever...
while (True):
    # Consume the next sensor event
    sensor_event = mapr_kafka.get_topic_message(config.MAPR_STREAM_PATH_TOPIC, offset)
    
    print('DEBUG: sensor_event: ' + str(sensor_event))
    # Determine the destination topic name based on the event source.
    # The destination topic will be AUTOMATICALLY CREATED if it does
    # not exist.  How cool is that?  Way cool!!!
    destination_topic = config.MAPR_STREAM_PATH + ":" + sensor_event['id']
    
    # Publish the sensor dataframe record to the destination topic
    response = mapr_kafka.post_topic_message(destination_topic, sensor_event)
    print("   FanOutFilter Has rePOSTed an event: " + str(sensor_event))

    time.sleep(FIVE_MS)
    offset += 1
       

