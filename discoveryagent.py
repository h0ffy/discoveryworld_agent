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
import json
#import ip2domain
#from agent import ClientAgent
from debug import * 
from beanstalk import *
from agent_scan.modules.ip2domain import *
from agent_scan.modules.discoverygeoip import * 


class DiscoveryAgent:
    @staticmethod
    def banner():
    	print("\t*****************************************************************")
    	print("\t*\t\t\t\t\t\t\t\t*")
    	print("\t*\t\t\tDiscoveryWorld Agent\t\t\t*")
    	print("\t*\t\t\t\t\t\t\t\t*")
    	print("\t*****************************************************************")
    
    @staticmethod  
    def agent_scan(taskqueue,scan_type,scan_data):
        if scan_type == "reverse-domain":
            ip = scan_data
            domains_result = ip2domain.IP2Domain(ip)
            domains_result.domains = list(set(newIP2Domain.domains))
            if domains.result is not None:
                if domains.result.domains is not None:
                    for domain in domains.result.domains:
                        task.output('{ "agent" : "null" , "plugin" : "agent_scan.ip2domain", "ip" : "{}", "domain" : "{}" }'.format(ip,domain))
        elif scan_type == "geoip":
            ip = scan_data
            result = DiscoveryGeoIP(ip)
            if result is not None:
                skelDict = { "agent" : "null", "plugin" : "agent_scan.geoip", "ip" : ip, "country" : result.country, "continent" : result.continent, "timezone" : result.timezone }
                #taskqueue.report(skelDict)
                return(skelDict) 
    

#### MAIN #####
    @staticmethod
    def main():
        print("Starting discoveryworld agent\t\t")
        taskqueue = BeanStackQueue(conf.BEANSTALK_SERVER,conf.BEANSTALK_PORT)
        print("[OK]")
        PDEBUG.log("Main: Starting discoveryworld agent\t\t [OK]")
        
        #taskqueue.test_task({"scan_type" : "geoip", "scan_data" : "8.8.8.8" })
        
        while 1:      
            job = taskqueue.recv("agent.scan")
            if job is not None:
                if job.job_data is not None:
                    PDEBUG.log("Main: recv\t\t OK")
                    data = dict(json.loads(job.job_data))
                    scan_type = data.get("scan_type")
                    scan_data = data.get("scan_data")
                    PDEBUG.log("Main: Init scan job {} with data {}".format(scan_type,scan_data))
                    result = DiscoveryAgent.agent_scan(taskqueue,scan_type,scan_data)
                    taskqueue.report(result)
                    taskqueue.release(int(job.job_id))
                #done
                #taskqueue.report(result)

            time.sleep(2)
        
        sys.exit(0)
        return(0)
    

