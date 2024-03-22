#!/usr/bin/env python
#	DiscoveryWorld Agent
#	Written by h0ffy / JennyLab
#   GNU GPL 3.0 CopyLeft 2024 @JennyLab

import sys,os
#import urllib, urllib2
import time
import threading
import conf
import daemon
import logging
import logger
#import ip2domain
#from agent import ClientAgent
from debug import * 
from beanstalk import *
from agent_scan.modules.ip2domain import *
from agent_scan.modules.geoip import * 

logger = logging.logger(__name__)

def banner():
	print("\t*****************************************************************")
	print("\t*\t\t\t\t\t\t\t\t*")
	print("\t*\t\t\tDiscoveryWorld Agent\t\t\t*")
	print("\t*\t\t\t\t\t\t\t\t*")
	print("\t*****************************************************************")


def agent_scan(queue,scan_type,scan_data):
    if scan_type == "reverse-domain":
        ip = scan_data.get_key("IP")
        domains_result = ip2domain.IP2Domain(ip)
        domains_result.domains = list(set(newIP2Domain.domains))
        if domains.result is not None:
            if domains.result.domains is not None:
                for domain in domains.result.domains:
                    queue.output('{ "agent" : "null" , "plugin" : "agent_scan.ip2domain", "ip" : "{}", "domain" : "{}" }'.format(ip,domain))
    elif scan_type == "geoip":
        ip = scan_data.get_key("IP")
        result = GeoIP(ip)
        if result is not None:
            skelDict = [{ "agent" : "null", "plugin" : "agent_scan.geoip", "ip" : ip, "country" : result.country, "continent" : result.continent, "timezone" : result.timezone }]
            resultDict = skelDict.update(result)
            queue.output(resultDict)



#### MAIN #####

def main():
    print("Starting discoveryworld agent\t\t")
    queue = BeanStackQueue(conf.BEANSTALK_SERVER,conf.BEANSTALK_PORT)
    print("[OK]")
    PDEBUG.log("Main: Starting discoveryworld agent\t\t OK")
    
    while 1:            
        for queue.recv("agent.scan") in job:
            PDEBUG.log("Main: rec\t\t OK")
            scan_type = job.job_data.get("scan_type")
            scan_data = job.job_data.scan_data("scan_data")
            PDEBUG.log("Main: Init scan job {} with data {}".format(scan_type,scan_data))
            agent_scan(queue,scan_type,scan_data)
        #done
        
        time.sleep(2)
    
	sys.exit(0)
	return(0)



if __name__ == "__main__":
	banner()
	#with daemon.DaemonContext():
	main()
	
