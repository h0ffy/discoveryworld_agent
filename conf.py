#!/usr/bin/env python
#	DiscoveryWorld Agent
#	Written by A.... / JennySec



LOG_PATH="/var/log/discoveryworld/discoveryagent.log"
TOKEN="1ca86108626d48815d5dbc58375a0495"
LISTEN_PORT=0xC0FE
LISTEN_IP=""
DEBUG=True
BEANSTALK_SERVER = "127.0.0.1"
BEANSTALK_PORT = 13120


#Internal use

#DBSM = "mysql" # or scylladb s
#DBHOST="127.0.0.1"
#DBPORT="3306"
#DBUSER="root"
#DBPASS="jennylab"
#DBNAME="discoveryworld"



import os,sys
#sys.path.insert(0, './dist/whatweb')
strCurrentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
