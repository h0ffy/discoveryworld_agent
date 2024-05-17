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
from agent_scan.modules.geoip import * 
from agent_scan.modules.subdomains import *


class DiscoveryAgent:
    @staticmethod
    def banner():
    	print("\t*****************************************************************")
    	print("\t*\t\t\t\t\t\t\t\t*")
    	print("\t*\t\t\tDiscoveryWorld Agent\t\t\t*")
    	print("\t*\t\t\t\t\t\t\t\t*")
    	print("\t*****************************************************************")
    
    @staticmethod  
    def agent_scan(queue,scan_type,scan_data):
        if scan_type == "domain-reverse":
            ip = scan_data
            domains_result = ip2domain.IP2Domain(ip)
            domains_result.domains = list(set(newIP2Domain.domains))
            if domains.result is not None:
                if domains.result.domains is not None:
                    for domain in domains.result.domains:
                        queue.output('{ "agent" : "null" , "plugin" : "agent_scan.ip2domain", "ip" : "{}", "domain" : "{}" }'.format(ip,domain))
        elif scan_type == "geoip":
            ip = scan_data
            result = GeoIP(ip)
            if result is not None:
                skelDict = [{ "agent" : "null", "plugin" : "agent_scan.geoip", "ip" : ip, "country" : result.country, "continent" : result.continent, "timezone" : result.timezone }]
                resultDict = skelDict.update(result)
                queue.output(resultDict)
        
        elif scan_type == "subdomain-wordlist":
            objSubDomain = SubDomains(scan_data))
            objSubDomain.run(bruteforce=False)
            strDomains = None
            if objSubDomain.result is not None:
                for subdomain in objSubDomain.result:
                    strDomains+=str("{};".format(subdomain))
                
                strDomains =strDomains.removesuffix(';')
                queue.output({"agent" : "null", "plugin" : "agent_scan.subdomain-wordlist",  "domain": scan_data, "subdomains" : strDomains})
        elif scan_type == "subdomain-bruteforce":
            objSubDomain = SubDomains(scan_data))
            objSubDomain.run(bruteforce=True)
            strDomains = None
            if objSubDomain.result is not None:
                for subdomain in objSubDomain.result:
                    strDomains+=str("{};".format(subdomain))
                
                strDomains=strDomains.removesuffix(';')
                queue.output({"agent" : "null", "plugin" : "agent_scan.subdomain-bruteforce",  "domain": scan_data, "subdomains" : strDomains})
        else:
            nop=0x90
                
            
                
                
                

#### MAIN #####
    @staticmethod
    def main():
        print("Starting discoveryworld agent\t\t")
        task = BeanStackQueue(conf.BEANSTALK_SERVER,conf.BEANSTALK_PORT)
        print("[OK]")
        PDEBUG.log("Main: Starting discoveryworld agent\t\t OK")
        
        task.test_task({"scan_type" : "geoip", "scan_data" : "8.8.8.8" })
        
        while 1:      
            tasks = task.recv("agent.scan")
            print("\n\n\n\n")
            print(tasks)
            print("\n\n\n")
            if tasks.job_data is not None:
                PDEBUG.log("Main: recv\t\t OK")
                data = dict(json.loads(tasks.job_data))
                print(data)
                scan_type = data.get("scan_type")
                scan_data = data.get("scan_data")
                PDEBUG.log("Main: Init scan job {} with data {}".format(scan_type,scan_data))
                DiscoveryAgent.agent_scan(task,scan_type,scan_data)
                #done
                
            time.sleep(2)
        
        sys.exit(0)
        return(0)
    

