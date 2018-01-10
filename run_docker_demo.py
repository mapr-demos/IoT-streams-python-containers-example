import os
import sys
import shutil
from telnetlib import Telnet
import warnings
import urllib3
import config
warnings.simplefilter('ignore', urllib3.exceptions.SecurityWarning)

if shutil.which('docker'):
    if shutil.which('docker-compose'):
        mapr_vm_or_ip = input('What is your MapR 6.0 VM hostname or IP address? ')

        if len(mapr_vm_or_ip) <= 0:
            print("ERROR: Your hostname or IP input of '{hostname}' is invalid. Please input a valid hostname or IP address.".format(hostname=mapr_vm_or_ip))
            exit(1)

        else:

            cmd = 'ping -c 1 {hostname} > /dev/null'.format(hostname=mapr_vm_or_ip)
            result = os.system(cmd)

            if result > 0:
                print("ERROR: Unable to ping {hostname}. Is it up and running?".format(hostname=mapr_vm_or_ip))
                exit(1)

            else:
                print("Ping to {hostname} status: success".format(hostname=mapr_vm_or_ip))

                try:
                    kafka_rest_url = '{base}{hostname}{suffix}'.format(base=config.MAPR_KAFKA_REST_URL_BASE, hostname=mapr_vm_or_ip, suffix=config.MAPR_KAFKA_REST_URL_SUFFIX)

                    tn = Telnet(mapr_vm_or_ip, 8082)
                    tn.close()

                    print("Kafka REST Proxy status: available".format(hostname=mapr_vm_or_ip))

                    # This ssh command will prompt for the 'mapr' user's ssh password
                    print("Please input your SSH password for the 'mapr' user at the prompt below so we can set up the stream and topics for you. This will take a few minutes.")
                    cmd = "ssh mapr@{hostname} 'bash -s' < cleanStreamTopics.sh > /dev/null".format(hostname=mapr_vm_or_ip)
                    result = os.system(cmd)

                    if result > 0:
                        print("ERROR: Something went wrong trying to run the below command. Please investigate. Do you need to renew your ticket for the 'mapr' user?\n\t{cmd}".format(cmd=cmd))
                        exit(1)
                    else:
                        print("Streams and topics status: created")
                        print('Building the docker images. This will take a few minutes.')

                        result = os.system('docker-compose build > /dev/null')

                        if result > 0:
                            print("ERROR: Something went wrong trying to run 'docker-compose build'. Try running it manually to investigate.")
                            exit(1)
                        else:
                            print("docker-compose build status: successful")

                            cmd = 'docker-compose up -e KAFKA_REST_URL={kafka_rest_url}'.format(kafka_rest_url=kafka_rest_url)
                            # cmd = 'docker-compose run -e KAFKA_REST_URL={kafka_rest_url} -p 5006:5006 -d dashboard > /dev/null'.format(
                            #     kafka_rest_url=kafka_rest_url)  # For easy Debugging
                            result = os.system(cmd)

                            if result > 0:
                                print("ERROR: Something went wrong trying to run the below command. Try running it manually to investigate.\n\t{cmd}".format(cmd=cmd))
                                exit(1)
                            else:
                                print("docker-compose up status: successful")

                                cmd = '{exe} {script}'.format(exe=sys.executable, script='dashboard_readiness.py')
                                result = os.system(cmd)

                                if result > 0:
                                    print(
                                        "ERROR: Something went wrong trying to run the below command. Try running it manually to investigate.\n\t{cmd}".format(
                                            cmd=cmd))
                                    exit(1)
                                else:
                                    print("Dashboard ready to view in browser status: available")

                                    stop_request = input('Press ENTER to shut down the demo: ')
                                    cmd = 'docker-compose down > /dev/null'
                                    os.system(cmd)
                                    print('All done. Good bye!')

                except ConnectionRefusedError:
                    print(
                        "ERROR: Unable to reach {kafka_url}. Is Kafka REST Proxy installed on your MapR host '{hostname}'?".format(
                            url=kafka_rest_url, hostname=mapr_vm_or_ip))
                    exit(1)
                except urllib3.exceptions.MaxRetryError:
                    print(
                        "ERROR: Unable to reach {kafka_url}. Is Kafka REST Proxy installed on your MapR host '{hostname}'?".format(
                            url=kafka_rest_url, hostname=mapr_vm_or_ip))
                    exit(1)

    else:
        print("ERROR: docker-compose doesn't exist on this machine. Is it installed?")
        exit(1)
else:
    print("ERROR: docker doesn't exist on this machine. Is it installed?")
    exit(1)
