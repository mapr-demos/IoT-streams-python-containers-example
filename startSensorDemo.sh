#!/bin/bash

echo "*******************************"
echo "Starting sensor_01, 'Alternator'"
echo "*******************************"
python3 sw_sensor.py sensor_01 1 5000 &
pid1=$!

echo "*************************"
echo "Starting sensor_02, 'MPG'"
echo "*************************"
python3 sw_sensor.py sensor_02 1 35 &
pid2=$!

echo "********************************"
echo "Starting sensor_03, 'Thermostat'"
echo "********************************"
python3 sw_sensor.py sensor_03 1 120 &
pid3=$!

echo "******************************"
echo "Starting sensor_04, Engine RPM"
echo "******************************"
python3 sw_sensor.py sensor_04 1 6500 &
pid4=$!

echo "zzzzzzzzzzzzzzzzzzzzzzzzzz"
echo "Sleeping for 2 Seconds..."
echo "zzzzzzzzzzzzzzzzzzzzzzzzzz"
sleep 2s

echo "************************************"
echo "Starting the fan out Event Filter..."
echo "************************************"
python3 event_filter.py &
pid5=$!


echo "zzzzzzzzzzzzzzzzzzzzzzzzzz"
echo "Sleeping for 2 Seconds..."
echo "zzzzzzzzzzzzzzzzzzzzzzzzzz"
sleep 2s

echo "******************************"
echo "Starting the Dashboard GUI..."
echo "******************************"
python3 dashboard.py &
pid6=$!

echo "#!/bin/bash"  > stopSensorDemo.sh
echo "kill -9 " $pid1 >> stopSensorDemo.sh
echo "kill -9 " $pid2 >> stopSensorDemo.sh
echo "kill -9 " $pid3 >> stopSensorDemo.sh
echo "kill -9 " $pid4 >> stopSensorDemo.sh
echo "kill -9 " $pid5 >> stopSensorDemo.sh
echo "kill -9 " $pid6 >> stopSensorDemo.sh
echo " " >> stopSensorDemo.sh
echo "echo Be sure to log into your MapR Cluster to clean up stream topics..." >> stopSensorDemo.sh
echo "echo 'ssh user01@127.0.0.1 -p 2222' " >> stopSensorDemo.sh
echo "echo './cleanStreamTopics.sh' " >> stopSensorDemo.sh
echo " " >> stopSensorDemo.sh
echo "echo Goodbye. " >> stopSensorDemo.sh

chmod u+x stopSensorDemo.sh

