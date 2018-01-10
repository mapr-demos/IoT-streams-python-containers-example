import config
# import requests
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
import webbrowser
from telnetlib import Telnet
from time import sleep

# count = 0
# MAX_ITERATIONS = 31
# success = False
#
#
# def requests_retry_session(
#         retries=30,
#         backoff_factor=1.5,
#         status_forcelist=(500, 502, 504),
#         session=None,
# ):
#     session = session or requests.Session()
#     retry = Retry(
#         total=retries,
#         read=retries,
#         connect=retries,
#         backoff_factor=backoff_factor,
#         status_forcelist=status_forcelist,
#     )
#     adapter = HTTPAdapter(max_retries=retry)
#     session.mount('http://', adapter)
#     return session
#
#
# print('Dashboard Readiness:DEBUG Waiting for dashboard to be ready... Dashboard UI should show up in a new tab of your browser at {url} in 30-60 seconds'.format(url=config.BOKEH_DASHBOARD_URL))
# resp = requests_retry_session().get(config.BOKEH_DASHBOARD_URL)
# if resp.status_code == 200:
#     webbrowser.open_new_tab(config.BOKEH_DASHBOARD_URL)
#     print("Dashboard Readiness:DEBUG Success! Dashboard UI is ready at {url}".format(url=config.BOKEH_DASHBOARD_URL))
#
# exit()



keep_trying = True
count = 0
MAX_ITERATIONS = 30
while count < MAX_ITERATIONS:
    try:
        tn = Telnet('localhost', 5006)
        tn.close()
        count = 30
        sleep(1)
        webbrowser.open_new_tab(config.BOKEH_DASHBOARD_URL)
        print(
            "Demo dashboard UI is ready at {url}".format(url=config.BOKEH_DASHBOARD_URL))
    except ConnectionRefusedError:
        count += 1
        sleep(1.5)

exit()
