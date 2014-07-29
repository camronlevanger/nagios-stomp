#!/usr/bin/python
import sys
import os
import traceback
import argparse
import time
import stomp

exit_code = 3
exit_message = 'UNKNOWN - Unable to get info for stomp connections'
debug = False


class MyListener(object):

    def on_connecting(self, host_and_port):
        dprint(host_and_port)
        global exit_code
        global exit_message
        exit_code = 1
        exit_message = 'WARNING - stuck in connection state to: %s', host_and_port

    def on_error(self, headers, message):
        dprint(message)
        global exit_code
        global exit_message
        exit_code = 2
        exit_message = 'CRITICAL - error connecting to stomp server: %s, %s', headers, message

    def on_connected(self, headers, body):
        dprint(body)
        global exit_code
        global exit_message
        exit_code = 0
        exit_message = 'OK - successfully connected to stom server: %s', message


if __name__ == '__main__':

    # parse out command args to override connection settings
    parser = argparse.ArgumentParser(description='A Nagios plugin to monitor stomp message servers')
    parser.add_argument('-H', '--host')
    parser.add_argument('-p', '--port', type=int)
    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--password')
    parser.add_argument('-t', '--topic')
    parser.add_argument('--debug', action="store_true")
    args = parser.parse_args()

    # connection defaults
    sthost = 'localhost'
    stport = 61680
    stuser = 'admin'
    stpass = 'admin'
    stopic = 'ps_notifications'

    # if args were passed in use them rather than defaults
    if args.debug != None:
        global debug
        debug = True
        dprint('debug output enabled')
    if args.host != None:
        sthost = args.host
        dprint('using host: %s', sthost)
    if args.port != None:
        stport = args.port
        dprint('using port: %s', stport)
    if args.user != None:
        stuser = args.user
        dprint('using user: %s', stuser)
    if args.password != None:
        stpass = args.password
        dprint('using password: %s', stpass)
    if args.topic != None:
        stopic = args.topic
        dprint('using topic: %s', stopic)

    try:
        dprint('attempting to setup connection to stomp server')
        conn = stomp.Connection([(sthost, stport)])
        conn.set_listener('', MyListener())
        conn.start()
        conn.connect(stuser, stpass)

        conn.subscribe(destination='/topic/' + stopic, id=1, ack='auto')

        # give it a moment to make the connection and then disconnect
        time.sleep(5)
        conn.disconnect()
    except KeyboardInterrupt:
        print "Shutdown requested...exiting"
    except Exception:
        traceback.print_exc(file=sys.stdout)

    # exit with exit_message and exit_code for nagios
    global exit_code
    global exit_message
    print exit_message
    sys.exit(exit_code)

def dprint(message):
    global debug
    if debug:
        print message
