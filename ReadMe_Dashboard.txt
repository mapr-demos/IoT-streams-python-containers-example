=============================================================================
                            streamDemo.zip

     A "Bare Bones" Python Demo that illustrates how to use MapR Streams
     from a Python program via the 'mapr_kafka_rest.py' module, which provides
     a 'pythonesque' wrapper around some of the MapR Kafka REST API calls.  
     
     This demo illustrates how to accomplish the following using Python:
     
      * Simulate a sensor in software  (sw_sensor.py)
      * Publish events to a MapR topic (sw_sensor.py)
      * Consume events from a MapR topic (event_filter.py and dashboard.py)
      * Create new MapR topics dynamically on the fly (event_filter.py)
      * Plot MapR Streams data on a live graph using Matplotlib (dashboard.py)
      
=============================================================================

Author:  Michael F. Aube
Email:   maube@mapr.com
Version: 1.1
Date:    29-AUG-2017
=============================================================================

Here are the files you should have as part of 'streamDemo.zip:
-----------------------------------------------------------------------------
 Dashboard.pdf            A picture of this demo's architecture.
 ReadMe_Dashboard.txt     (this file)
 config.py                Demo settings and configuration bits, in Python.
 dashboard.py             The demo's user interface, using matplotlib and Python.
 event_filter.py          The "fan out" filter for sensor events, in Python.
 mapr_kafka_rest.py       A module that wraps Kafka REST API for POST and GET.
 startSensorDemo.sh       Shell script that starts the demo processes,
                          and generates the stopSensorDemo.sh file.
 <stopSensorDemo.sh>      The generated shell script that stops the demo processes.
 sw_sensor.py             A simulated software sensor, in Python.
=============================================================================

                       *** PLEASE NOTE: *** 

The Python files included in this demo package assume that you have installed
Python 3.5.2 AND the "Requests HTTP Library for Python".

I cheated by installing the Anaconda environment on my laptop, which 
included Python 3.5.2 and the "Requests HTTP Library for Python". 

If you would like to cheat too, please see 'Appendix A' below for the quick
and dirty Anaconda installation instructions!  :>)

=============================================================================

1. Create a new MapR Sandbox VM inside VirtualBox by importing the file named:
   
   MapR-Sandbox-For-Hadoop-5.2.1.ova
   
   
2. Before you start your new "Sandbox" VM, add the following line to
   the Port Forwarding rules for the NAT network interface.  If you are
   running the gateway on a different port, please substitute your port
   number for '8082' below:  
   -----------------------------------------------------------------------------
   |    Name         Protocol  Host IP       Host Port   Guest IP   Guest Port |
   -----------------------------------------------------------------------------
   Kafka_REST        TCP       127.0.0.1     8082                   8082
   
   This will allow you to connect to the Kafka REST gateway from processes that
   are running outside of your MapR Sandbox.
   

3. Start your new Sandbox VM, and let it come up all the way.


4. Login as the ‘root’ user, install the Kafka REST Gateway, set the flush timeout 
   for the Kafka REST gateway buffer, and then restart the Warden service:

   $ ssh -p 2222 root@localhost
   password: mapr

   [root@maprdemo ~]# yum install mapr-kafka-rest
   [root@maprdemo ~]# echo 'streams.buffer.max.time.ms=100' >> /opt/mapr/kafka-rest/kafka-rest-2.0.1/config/kafka-rest.properties
   [root@maprdemo ~]# service mapr-warden restart
   [root@maprdemo ~]# exit


5. Login as the 'user01' user, create the MapR Stream and Topic for this demo:
# Create the MapR Stream 'iot_stream':

   $ ssh -p 2222 user01@localhost
   password: mapr

   [user01@maprdemo ~]$ maprcli stream create -path /user/user01/iot_stream -produceperm p -consumeperm p -topicperm p

# Create the main MapR Topic 'sensor_data':

   [user01@maprdemo ~]$ maprcli stream topic create -path /user/user01/iot_stream -topic sensor_data
   
   -------------------------------------------------------------------------------
   FYI:  If you want to delete the topic to start over, issue this command:
   [user01@maprdemo ~]$ maprcli stream topic delete -path /user/user01/iot_stream -topic sensor_data

   To see the information about a given topic:
   [user01@maprdemo ~]$ maprcli stream topic info -path /user/user01/iot_stream -topic sensor_data -json

   To see a list of all topics defined in a stream:
   [user01@maprdemo ~]$ maprcli stream topic list -path /user/user01/iot_stream  -json
   
   Use the following command to list all of the topics within a given stream:
   [user01@maprdemo ~]$ curl -X GET http://localhost:8082/streams/%2Fuser%2Fuser01%2Fiot_stream/topics

   -------------------------------------------------------------------------------

6. Create a new directory on your host machine (NOT the SandBox!), and unzip the 
   demo files into it, and set the shell script files as 'executable':
   (Assumes you have copied the file 'streamDemo.zip' into your current directory)

   [maube@mac13 ~]$ mkdir streamDemo
   [maube@mac13 ~]$ cd streamDemo
   [maube@mac13 ~/streamDemo] $ unzip ../streamDemo.zip 
   [maube@mac13 ~/streamDemo] $ chmod u+x *.sh
   
   
7. Open a second terminal window, cd into the same directory, and start the demo:f

   [maube@mac13 ~]$ cd streamDemo
   [maube@mac13 ~/streamDemo] $ ./startSensorDemo.sh
   
   
8. From the first terminal window, stop the demo:

   [maube@mac13 ~]$ cd streamDemo
   [maube@mac13 ~/streamDemo] $ ./stopSensorDemo.sh
   
   

#############################################################################
   Appendix A - Install Anaconda (with Python 3.5.2 and 'requests' library).
#############################################################################

A1. Start your Sandbox VM.


A2. Login with your preferred user account (I will use 'user01'):

    $ ssh -p 2222 user01@localhost
    password: mapr


A3. Download the Anaconda installer:

    [user01@maprdemo ~]$ wget https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh


A4. Run the installer, and follow the prompts.  Let Anaconda modify your PATH within your
    login script ( ~/.bashrc ) to make things easy:

    [user01@maprdemo ~]$ bash Anaconda2-4.1.1-Linux-x86_64.sh


A5. Source your login script file to reset your environment:

    [user01@maprdemo ~]$ source ~/.bashrc


A6. Check your Python version for Python 3.5.2:

    [user01@maprdemo ~]$ python --version

    This should return:  Python 3.5.2 :: Anaconda 4.2.0 (64-bit)

 
A7. You can now run the example scripts to learn how to publish/consume messages to/from
    MapR Streams using Python and the MapR Kafka REST Gateway.  Have fun!!!

   
