import config   # for global variable config.master_offset
import mapr_kafka_rest as mapr_kafka
import matplotlib as mpl
mpl.use('WebAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.style as style
import requests
import webbrowser
from time import sleep

# """
# Generate some random x,y plot data.
# In a real demo, we would pull these
# data points from a MapR Stream topic,
# or a file, database, etc...
# """
# def create_data(a_count=10, a_max_y=10):
#     xs = []
#     ys = []
#     for i in range(a_count):
#         x = i
#         y = random.randrange(a_max_y)
#         xs.append(x)
#         ys.append(y)
#     return xs, ys


# def update_graph_data(xlist, ylist):
#    """
#    Shifts the given lists left one element, in place,
#    and then appends a new data element to produce the 
#    next set of data to plot.
#    """
#    # Fake it for now - just make the graph "cycle"
#    y = ylist[0]
#    # shift the given lists left by one element
#    del xlist[0]
#    del ylist[0]
#    # Add the newest data point on the right...
#    xlist.append(xlist[-1] + 1)
#    ylist.append(y)

### USE THE STREAM,LUKE!!!
"""
Consume the first a_count events from the given topic, parse out the x and y values,
and append them to the locally declared xs and ys arrays.

Returns two arrays that hold the x and y values parsed from the sensor events. 
"""
def init_event_data(a_topic_name, an_offset, a_count=10):
   offset = an_offset
   xs = []
   ys = []

   for i in range(a_count):
      # Consume the next event from the given MapR topic...
      sensor_event = mapr_kafka.get_topic_message(a_topic_name, offset)
      
      x = int(sensor_event['x'])
      y = int(sensor_event['value'])
      print('Dashboard:DEBUG i: ' + str(i) + ' from topic: ' + a_topic_name + ' x: ' + sensor_event['x'] + ' y: ' + sensor_event['value'] + ' \n')
      xs.append(x)
      ys.append(y)
      # go get the next event
      offset += 1
   
   # initialize the master offset here?   
   master_offset = 10
   return xs, ys


### USE THE STREAM,LUKE!!!
def append_event_data(a_topic_name, an_offset, xlist, ylist):
   """
   Consumes the next sensor event from the given topic, parses out the x and y values,
   deletes the oldes x and y values from the given xlist anf ylist arrays, then appends
   the new x and y values to the given xlist and ylist arrays.  This results in the
   next set of data to plot.
   """
   #---------------------------------------------------------
   # Consume the next sensor event data from a topic.
   #---------------------------------------------------------
   sensor_event = mapr_kafka.get_topic_message(a_topic_name, an_offset)
   
   new_x = int(sensor_event['x'])
   new_y = int(sensor_event['value'])
   print('Dashboard:DEBUG: offset ' + str(an_offset) + ' from topic: ' + a_topic_name + ' x: ' + sensor_event['x'] + ' y: ' + sensor_event['value'] + ' \n')

   # Add the newest data point on the right...
   xlist.append(new_x)
   ylist.append(new_y)

   # Delete the oldest data point on the given lists
   del xlist[0]
   del ylist[0]

      


def animate(i):
    # Update the data to be plotted.
    
    #print('DEBUG animate(): config.master_offset = ' + str(config.master_offset) + '\n')
       
    # Get the next event per MapR topic, and append it to the
    # given x's and y's arrays; then trim off the the left-most
    # event so that the array size remains constant.
    #
    # This will cause the subplots to "move" one x-value to the right
    # each time through this function.   
    try:
        append_event_data(topic_name1, config.master_offset, xs1, ys1)
        append_event_data(topic_name2, config.master_offset, xs2, ys2)
        append_event_data(topic_name3, config.master_offset, xs3, ys3)
        append_event_data(topic_name4, config.master_offset, xs4, ys4)
        #
        config.master_offset += 1
    except KeyError:
        pass   # one or more topics are currently out of data...
    
    # Clear the previous plot, including labels, titles, etc.
    axes1.clear()
    axes2.clear()
    axes3.clear()
    axes4.clear()
    
    # Redraw the subplot titles, labels, etc.
    axes1.set_title('Sensor-01', color='black', fontsize=12)
    axes1.set_ylabel('Alternator mAmps', color='black', fontsize=12)
    axes2.set_title('Sensor-02', color='green', fontsize=12)
    axes2.set_ylabel('MPG', color='green', fontsize=12)
    axes3.set_title('Sensor-03', color='red', fontsize=12)
    axes3.set_ylabel('Temp. Degrees F', color='red', fontsize=12)
    axes4.set_title('Sensor-04', color='blue', fontsize=12)
    axes4.set_ylabel('Engine RPM', color='blue', fontsize=12)

    # Plot the new data to be displayed
    axes1.plot(xs1,ys1,'black', label='Sensor-1')
    axes2.plot(xs2,ys2,'green', label='Sensor-2')
    axes3.plot(xs3,ys3,'red', label='Sensor-3')
    axes4.plot(xs4,ys4,'blue', label='Sensor-4')

    
# Set up some reusable values
topic_name0 = '/user/user01/iot_stream:sensor_data'
topic_name1 = '/user/user01/iot_stream:sensor_01' 
topic_name2 = '/user/user01/iot_stream:sensor_02' 
topic_name3 = '/user/user01/iot_stream:sensor_03' 
topic_name4 = '/user/user01/iot_stream:sensor_04' 
	
# Data Init: use an offset of 0, and an event count of 10.
# Consume the first 10 sensor events for sensor 1, "Alternator mAmps"
xs1, ys1 = init_event_data(topic_name1, 0, 10)

# Consume the first 10 sensor events for sensor 2, "MPG"
xs2, ys2 = init_event_data(topic_name2, 0, 10)

# Consume the first 10 sensor events for sensor 3, "Temperature Degrees F"
xs3, ys3 = init_event_data(topic_name3, 0, 10)

# Consume the first 10 sensor events for sensor 4, "Engine RPM"
xs4, ys4 = init_event_data(topic_name4, 0, 10)


style.use('fivethirtyeight')

fig = plt.figure()

# Create a 2 row by 2 column grid and place 4 subplots on it.
axes1 = plt.subplot2grid( (2,2), (0,0), rowspan=1, colspan=1)
axes1.set_title('Sensor-01', color='black', fontsize=12)
axes1.set_ylabel('Alternator mAmps', color='black', fontsize=12)

axes2 = plt.subplot2grid( (2,2), (0,1), rowspan=1, colspan=1)
axes2.set_title('Sensor-02', color='green', fontsize=12)
axes2.set_ylabel('MPG', color='green', fontsize=12)

axes3 = plt.subplot2grid( (2,2), (1,0), rowspan=1, colspan=1)
axes3.set_title('Sensor-03', color='red', fontsize=12)
axes3.set_ylabel('Temp. Degrees F', color='red', fontsize=12)

axes4 = plt.subplot2grid( (2,2), (1,1), rowspan=1, colspan=1)
axes4.set_title('Sensor-04', color='blue', fontsize=12)
axes4.set_ylabel('Engine RPM', color='blue', fontsize=12)

plt.subplots_adjust(left=0.14, bottom=0.20, right=0.94, top=0.85, wspace=0.50, hspace=0.50)
   
# Let the animation begin! 
ani = animation.FuncAnimation(fig, animate, interval=50)
plt.suptitle('Streaming Data Dashboard');
plt.show()

ready = False
print('Waiting for dashboard to be ready... Dashboard UI should show up in a new tab of your browser at {url} in 30-60 seconds'.format(url=config.MATPLOTLIB_DASHBOARD_URL))
while not ready:
    try:
        resp = requests.get(config.MATPLOTLIB_DASHBOARD_URL)
        if resp.status_code == 200:
            webbrowser.open_new_tab(config.MATPLOTLIB_DASHBOARD_URL)
            ready = True
        else:
            sleep(1)
    except Exception:
        value = True  # Do nothing
