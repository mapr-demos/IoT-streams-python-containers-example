"""
read_from_topic.py

Utility to read a message off a given MapR topic.
"""

import time 
import json
import random
import mapr_kafka_rest as mapr_kafka
    
# Set up some reusable values
stream_name  = '/user/user01/iot_stream'
topic_name   = '/user/user01/iot_stream:sensor_data'
offset = 0

topic_name = input('Enter the full topic name (ex: "/user/user01/iot_stream:sensor_data" ? ')

# Consume the first message from topic
msg = mapr_kafka.get_topic_message(topic_name, 0)
    
print('Here is your message: \n' + str(msg))

       

