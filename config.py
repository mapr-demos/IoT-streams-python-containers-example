"""
config.py

for global variable declarations across other modules
"""
#
# initialized to 10 because we will init the graph data
# by consuming the first 10 sensor events off each sensor's
# dedicated topic.
#
master_offset = 10
MAPR_KAFKA_REST_URL = "https://maprdemo:8082/topics/"
MAPR_KAFKA_REST_USER = "user01"
MAPR_KAFKA_REST_PASSWORD = "mapr"
MATPLOTLIB_DASHBOARD_URL = "http://localhost:8988"
MAPR_STREAM_PATH = '/user/user01/iot_stream'
MAPR_STREAM_TOPIC_NAME = 'sensor_data'
MAPR_STREAM_PATH_TOPIC = '{stream_name}:{topic_name}'.format(stream_name=MAPR_STREAM_PATH,
                                                             topic_name=MAPR_STREAM_TOPIC_NAME)
