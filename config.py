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
YAXIS_LABEL_SENSOR_01 = 'Alternator mAmps'
YAXIS_LABEL_SENSOR_02 = 'MPG'
YAXIS_LABEL_SENSOR_03 = 'Temp. Degrees F'
YAXIS_LABEL_SENSOR_04 = 'Engine RPM'
MAPR_STREAM_TOPIC_NAME_DYNAMIC_01 = 'sensor01'
MAPR_STREAM_TOPIC_NAME_DYNAMIC_02 = 'sensor02'
MAPR_STREAM_TOPIC_NAME_DYNAMIC_03 = 'sensor03'
MAPR_STREAM_TOPIC_NAME_DYNAMIC_04 = 'sensor04'
MAPR_STREAM_TOPIC_PATH_DYNAMIC_01 = '{stream_name}:{topic_name}'.format(stream_name=MAPR_STREAM_PATH,
                                                             topic_name=MAPR_STREAM_TOPIC_NAME_DYNAMIC_01)
MAPR_STREAM_TOPIC_PATH_DYNAMIC_02 = '{stream_name}:{topic_name}'.format(stream_name=MAPR_STREAM_PATH,
                                                             topic_name=MAPR_STREAM_TOPIC_NAME_DYNAMIC_02)
MAPR_STREAM_TOPIC_PATH_DYNAMIC_03 = '{stream_name}:{topic_name}'.format(stream_name=MAPR_STREAM_PATH,
                                                             topic_name=MAPR_STREAM_TOPIC_NAME_DYNAMIC_03)
MAPR_STREAM_TOPIC_PATH_DYNAMIC_04 = '{stream_name}:{topic_name}'.format(stream_name=MAPR_STREAM_PATH,
                                                             topic_name=MAPR_STREAM_TOPIC_NAME_DYNAMIC_04)
