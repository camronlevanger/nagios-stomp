#!/usr/bin/python
import sys
import os
import traceback
import argparse
import time

import stomp
import ConfigParser

log = logging.getLogger(__name__);

exit_code = 3
exit_message = 'UNKNOWN - Unable to get info for stomp connections'


class MyListener(object):
	def on_connecting(self, host_and_port):
		print host_and_port
		global exit_code
		global exit_message
		exit_code = 1
		exit_message = 'WARNING - stuck in connection state to: %s', host_and_port

    def on_error(self, headers, message):
        global exit_code
		global exit_message
		exit_code = 2
		exit_message = 'CRITICAL - error connecting to stomp server: %s, %s', headers, message

	def on_connected(self, headers, body):
        global exit_code
		global exit_message
		exit_code = 0
		exit_message = 'OK - successfully connected to stom server: %s', message


if __name__ == '__main__':

    # parse out command args to override connection settings
    parser = argparse.ArgumentParser(description='A Nagios plugin to monitor WAMP servers')
    parser.add_argument('-H', '--host')
    parser.add_argument('--debug', action="store_true")
    parser.add_argument('-t', '--timeout', type=int)
    args = parser.parse_args()

	# connection defaults
	sthost = 'localhost'
	stport = 61680
	stuser = 'admin'
	stpass = 'admin'
	stopic = 'ps_notifications'

	conn = stomp.Connection([(sthost, stport)])
	conn.set_listener('', MyListener())
	conn.start()
	conn.connect(stuser, stpass)

	conn.subscribe(destination='/topic/' + stopic, id=1, ack='auto')

	time.sleep(2)
	conn.disconnect()