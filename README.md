nagios-stomp
============

A Nagios Stomp Message Protocol Monitor
-------------------------------------

A Nagios NRPE script that allows you to monitor a message queue server using
the STOMP protocol. While it is fairly easy with Nagios to monitor whether
or not your server proccess is running, unfortunately that can't tell us
if that server is available and accepting connections.

With nagios-stomp you can actually open a connection to your queue servers and
have the confidence of knowing that they are responding correctly to your systems.

This script is designed to be run on Nagios client servers using the NRPE daemon.

For more information on using Nagios and NRPE visit the following link:

[http://nagios.sourceforge.net/docs/nrpe/](http://nagios.sourceforge.net/docs/nrpe/)

Installation and Usage
----------------------

###Download and Install nagios-stomp

####Clone Source and Install Manually
This is a pretty simple option for this small codebase. We will clone the  source into
the directory where we want to keep our Nagios plugins, install the required libraries,
and finally set proper permissions.

	cd /path/to/where/you/want/it
	git clone git@github.com:camronlevanger/nagios-stomp.git
	cd nagios-stomp
	pip install -r requirements.txt
	chmod +x check_stomp_conn.py

Then restart the NRPE service, on Ubuntu that looks like:

	service nagios-nrpe-server restart

####Install Using Pip
Coming Soon

###Add nagios-stomp Command to NRPE Client
Now we need to edit our nrpe.cfg file and add our new plugin command.

	vim /etc/nagios/nrpe.cfg

Now add the check_stomp_conn command to the list.

	 command[check_stomp_conn]=/path/to/where/you/put/it/check_stomp_conn.py

By default nagios-stomp connects to localhost on port 61613, with a username and
password of admin, and subscribes to default_topic. If this works for your setup
(doubtful) then the above command config is all that is needed. If that does not reflect
the location of the message server you need to monitor, you can also pass in the
variables as args to the command.

To pass args to the command make sure you set in nrpe.cfg

	dont_blame_nrpe=1

And then the args are

	-H host_uri
	-P port_number
	-u username
	-p password
	-t topic_name

###Add nagios-stomp to Nagios Checks on Your Nagios Monitoring Server
Define a new service for nagios-stomp

	define service {
		use	generic-service (or your appropriate defined service)
		host_name	name_of_your_client_host
		service_description	Web Socket Server Monitor
		check_command	check_stomp_conn
	}

Resart the Nagios host.
