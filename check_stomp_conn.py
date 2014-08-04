#!/usr/bin/python
import sys
import os
import traceback
import argparse
import time
import stomp
import logging

logging.basicConfig(level=logging.DEBUG)
exit_code = 3
exit_message = 'UNKNOWN - Unable to get info for stomp connections'
debug = False

def dprint(message):
    global debug
    if debug:
        print message


class MyListener(object):

    def on_connecting(self, host_and_port):
        dprint(host_and_port)
        global exit_code
        global exit_message
        exit_code = 1
        exit_message = 'WARNING - stuck in connection state to'

    def on_error(self, headers, message):
        dprint(message)
        global exit_code
        global exit_message
        exit_code = 2
        exit_message = 'CRITICAL - error connecting to stomp server'

    def on_connected(self, headers, body):
        dprint(body)
        global exit_code
        global exit_message
        exit_code = 0
        exit_message = 'OK - successfully connected to stomp server'


if __name__ == '__main__':

    # parse out command args to override connection settings
    parser = argparse.ArgumentParser(description='A Nagios plugin to monitor stomp message servers')
    parser.add_argument('-H', '--host')
    parser.add_argument('-P', '--port', type=int)
    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--password')
    parser.add_argument('-t', '--topic')
    parser.add_argument('--debug', action="store_true")
    args = parser.parse_args()

    # connection defaults
    sthost = 'localhost'
    stport = 61613
    stuser = 'admin'
    stpass = 'admin'
    stopic = 'default_topic'

    # if args were passed in use them rather than defaults
    if args.debug:
        debug = True
        dprint('debug output enabled')
    else:
        # we are not in debug mode so override the logging level
        logging.disable(logging.CRITICAL)

    if args.host != None:
        sthost = args.host
        dprint('using host: ' + sthost)

    if args.port != None:
        stport = args.port
        dprint(('using port: ' + str(stport)))

    if args.user != None:
        stuser = args.user
        dprint(('using user: ' + stuser))

    if args.password != None:
        stpass = args.password
        dprint(('using password: ' + stpass))

    if args.topic != None:
        stopic = args.topic
        dprint(('using topic: ' + stopic))

    try:
        dprint('attempting to setup connection to stomp server')
        conn = stomp.Connection([(sthost, stport)])
        conn.set_listener('', MyListener())
        conn.start()
        conn.connect(stuser, stpass)

        conn.subscribe(destination='/topic/' + stopic, id=1, ack='auto')

        # give it a moment to make the connection and then disconnect
        time.sleep(0.1)
        conn.disconnect()
    except KeyboardInterrupt:
        print "Shutdown requested...exiting"
    except Exception as e:
        exit_code = 2
        exit_message = 'CRITICAL - exception raised while connecting to stomp server'
        traceback.print_exc(file=sys.stdout)

    # exit with exit_message and exit_code for nagios
    print exit_message
    sys.exit(exit_code)
