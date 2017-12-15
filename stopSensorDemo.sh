#!/bin/bash
kill -9  91518
kill -9  91519
kill -9  91520
kill -9  91521
kill -9  91531
kill -9  91535
 
echo Be sure to log into your MapR Cluster to clean up stream topics...
echo 'ssh user01@127.0.0.1 -p 2222' 
echo './cleanStreamTopics.sh' 
 
echo Goodbye. 
