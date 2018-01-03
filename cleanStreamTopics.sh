#!/bin/bash
# filename: cleanStreamTopics.sh

echo "Restart kafka-rest to clear up memory ..."
maprcli node services -nodes maprdemo -name kafka-rest -action restart
echo "Deleting the stream /user/user01/iot_stream ..."
maprcli stream delete -path /user/user01/iot_stream
echo "Stream deleted."
echo "Creating the stream /user/user01/iot_stream ..."
maprcli stream create -path /user/user01/iot_stream -produceperm p -consumeperm p -topicperm p
echo "Stream created."
echo "Creating the topic iot_stream:sensor_data ..."
maprcli stream topic create -path /user/user01/iot_stream -topic sensor_data
echo "Topic created."
echo "Goodbye."