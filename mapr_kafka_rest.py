"""
The mapr_kafka_rest module implements a simplified Python wrapper for selected
calls in the MapR Kafka REST API.

Most of the actual 'boiler plate' details for these REST API calls have been 
abstracted out of the Python functions as parameters with default values.
This allows users of this module to focus on the message and topic details.  

"""

import config   # for global variable config.master_offset
import requests
import json
import warnings
import urllib3
import os

warnings.simplefilter('ignore', urllib3.exceptions.SecurityWarning)
KAFKA_REST_URL = os.environ.get('KAFKA_REST_URL', config.MAPR_KAFKA_REST_URL)

# The above warnings.simplefilter(...) ignores the below errors until mapr-kafka-rest package fixes the SSL cert
# Error 1:
# ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:748)
#
# Error 2:
# /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/urllib3/connection.py:344:
# SubjectAltNameWarning: Certificate for maprdemo has no `subjectAltName`, falling back to check for a `commonName`
# for now. This feature is being removed by major browsers and deprecated by RFC 2818.
# (See https://github.com/shazow/urllib3/issues/497 for details.)
#
# See https://maprdrill.atlassian.net/browse/KAFKA-39

def post_topic_message(
        a_mapr_topic,
        a_message,
        a_kafka_rest_url=KAFKA_REST_URL,
        a_content_type='application/vnd.kafka.json.v1+json'):
    """

    POSTs a_message to a_mapr_topic via the MapR Kafka REST API Gateway.

    --------------------
    Function Parameters:
    --------------------

    a_mapr_topic     - the full name of the destination MapR Streams topic.  
                       An example is:  '/user/user01/iot_stream:sensor_data'.

    a_message        - the message to be published on a_mapr_topic

    a_kafka_rest_url - OPTIONAL - The URL of the Kafka REST gateway.
                       The default value is: 'http://maprdemo:8082/topics/'.

    a_content_type   - OPTIONAL - the content type of a_message.
                       The default value is: 'application/vnd.kafka.json.v1+json'.  
    """

    # assemble the full JSON for this record
    json = {}
    json['value'] = a_message
    # json-> { 'value': {'mac':'18-FE-34-17-BF-C2', 'amplitude':452109} }

    # add this record to a list of records (it is "possible" to send N messages per POST)
    records = []
    records.append(json)
    # records-> [ {'value': {'mac':'18-FE-34-17-BF-C2', 'amplitude':452109}} ]

    # construct the requests 'POST' payload
    payload = {}
    payload['records'] = records
    # payload-> { 'records': [{'value': {'mac':'18-FE-34-17-BF-C2', 'amplitude':452109}}] }

    # URL-Encode the topic name: / becomes %2F and : becomes %3A
    encoded_mapr_topic = a_mapr_topic.replace('/', '%2F').replace(':', '%3A')
    url = a_kafka_rest_url + encoded_mapr_topic

    headers = {}
    headers['Content-Type'] = a_content_type

    # Now send the HTTP POST request to the Kafka REST Gateway
    # credentials = {'username': 'user01', 'password': 'mapr'}
    response = requests.post(url, json=payload, headers=headers,
                             auth=(config.MAPR_KAFKA_REST_USER, config.MAPR_KAFKA_REST_PASSWORD), verify=False)

    return response


####################################################################################
#  TODO:
#
#  Need to "unwrap" the response.text to return ONLY the Python dictionary object
#  that represents the topic message that was retrieved....
####################################################################################
def get_topic_message(
        a_mapr_topic_name = config.MAPR_STREAM_PATH_TOPIC,
        a_topic_offset    = 0,
        a_topic_partition = 0,
        a_kafka_rest_url  = KAFKA_REST_URL,
        a_content_type    = 'application/vnd.kafka.json.v1+json' ) :
    """

    Returns a single message from a_mapr_topic_name using a_topic_partition
    number and a_topic offset number via the MapR Kafka REST API Gateway..

    --------------------
    Function parameters:
    --------------------

    a_mapr_topic_name - the complete MapR topic name: <stream-path>:<topic_name>
 
    a_topic_offset    - the message offset number - default value is 0

    a_topic_partition - the partition number - default value is 0

    a_kafka_rest_url  - OPTIONAL - the URL location of the MapR Kafka REST gateway.
                        The default value is: 'http://maprdemo:8082/topics/'.

    a_content_type    - OPTIONAL - the content type of the message.
                        The default value is: 'application/vnd.kafka.json.v1+json'

    """
    # This is an example of a command line "GET" using the MapR Kafka REST gateway:
    # curl -X GET -H "Accept: application/vnd.kafka.json.v1+json" /
    # "https://maprdemo:8082/topics/%2Fuser%2Fuser01%2Fiot_stream%3Asensor_data/partitions/0/messages?offset=0&count=1" /
    # -u "user01:mapr" --insecure
    
    # URL-Encode the topic name: / becomes %2F and : becomes %3A
    encoded_mapr_topic = a_mapr_topic_name.replace('/','%2F').replace(':','%3A')

    # Build the complete URL for the GET request 
    url = a_kafka_rest_url + encoded_mapr_topic + '/partitions/' + str(a_topic_partition) + '/messages'

    payload = {'offset':a_topic_offset, 'count':1}    # get a single message only
 
    req_headers = {'Accept':a_content_type}

    # Now send the HTTP GET request to the Kafka REST Gateway
    response = requests.get(url, params=payload, headers=req_headers, auth=(config.MAPR_KAFKA_REST_USER, config.MAPR_KAFKA_REST_PASSWORD), verify=False)

    # Unwrap the message payload from the response
    message = {}
    
    if (response.status_code == 200):
        # Reconstitute the message by unpacking the response...
        msg_list  = json.loads(response.text)
        if (len(msg_list) > 0) :
            json_dict = msg_list[0]
            message = json_dict['value']
    # TODO can uncomment this, but it is noisy.
    # else:
    #     print('*** Error *** in get_topic_message() : ' + str(response.status_code) )
    #     print(response.url)
    #     print(response.headers)
        
    return message
    #
    # End of Function: get_topic_message()


def get_topic_messages(
        a_mapr_topic_name=config.MAPR_STREAM_PATH_TOPIC,
        a_topic_offset=0,
        a_topic_partition=0,
        a_kafka_rest_url=KAFKA_REST_URL,
        a_content_type='application/vnd.kafka.json.v1+json',
        a_count=10):
    """

    Returns up to 10 messages from a_mapr_topic_name using a_topic_partition
    number and a_topic offset number via the MapR Kafka REST API Gateway.

    --------------------
    Function parameters:
    --------------------

    a_mapr_topic_name - the complete MapR topic name: <stream-path>:<topic_name>

    a_topic_offset    - the message offset number - default value is 0

    a_topic_partition - the partition number - default value is 0

    a_kafka_rest_url  - OPTIONAL - the URL location of the MapR Kafka REST gateway.
                        The default value is: 'http://maprdemo:8082/topics/'.

    a_content_type    - OPTIONAL - the content type of the message.
                        The default value is: 'application/vnd.kafka.json.v1+json'

    a_count           - OPTIONAL - the number of messages to retrieve.
                        The default value is: 10

    """

    # This is an example of a command line "GET" using the MapR Kafka REST gateway:
    # curl -X GET -H "Accept: application/vnd.kafka.json.v1+json" /
    # "https://maprdemo:8082/topics/%2Fuser%2Fuser01%2Fiot_stream%3Asensor_data/partitions/0/messages?offset=0&count=1" /
    # -u "user01:mapr" --insecure

    # URL-Encode the topic name: / becomes %2F and : becomes %3A
    encoded_mapr_topic = a_mapr_topic_name.replace('/', '%2F').replace(':', '%3A')

    # Build the complete URL for the GET request
    url = a_kafka_rest_url + encoded_mapr_topic + '/partitions/' + str(a_topic_partition) + '/messages'

    payload = {'offset': a_topic_offset,
               'count': a_count}

    req_headers = {'Accept': a_content_type}

    # Now send the HTTP GET request to the Kafka REST Gateway
    response = requests.get(url, params=payload, headers=req_headers,
                            auth=(config.MAPR_KAFKA_REST_USER, config.MAPR_KAFKA_REST_PASSWORD), verify=False)

    # Unwrap the message payload from the response
    messages = []

    if (response.status_code == 200):
        # Reconstitute the message by unpacking the response...
        msg_list = json.loads(response.text)
        for msg in msg_list:
            messages.append(msg['value'])

    # TODO can uncomment this, but it is noisy.
    # else:
    #     print('*** Error *** in get_topic_message() : ' + str(response.status_code) )
    #     print(response.url)
    #     print(response.headers)

    return messages

    #
    # End of Function: get_topic_messages()
