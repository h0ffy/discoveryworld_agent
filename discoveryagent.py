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
<<<<<<< HEAD
from agent_scan.modules.geoip import * 
from agent_scan.modules.subdomains import *
=======
from agent_scan.modules.discoverygeoip import * 
>>>>>>> a22c3020e9cd2285ab3aead8f2a02d91df40317a


class DiscoveryAgent:
    @staticmethod
    def banner():
    	print("\t*****************************************************************")
    	print("\t*\t\t\t\t\t\t\t\t*")
    	print("\t*\t\t\tDiscoveryWorld Agent\t\t\t*")
    	print("\t*\t\t\t\t\t\t\t\t*")
    	print("\t*****************************************************************")
    
    @staticmethod  
<<<<<<< HEAD
    def agent_scan(queue,scan_type,scan_data):
        if scan_type == "domain-reverse":
=======
    def agent_scan(taskqueue,scan_type,scan_data):
        if scan_type == "reverse-domain":
>>>>>>> a22c3020e9cd2285ab3aead8f2a02d91df40317a
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
<<<<<<< HEAD
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
                
            
                
                
                
=======
                skelDict = { "agent" : "null", "plugin" : "agent_scan.geoip", "ip" : ip, "country" : result.country, "continent" : result.continent, "timezone" : result.timezone }
                #taskqueue.report(skelDict)
                print(skelDict)
                return(skelDict) 
    
>>>>>>> a22c3020e9cd2285ab3aead8f2a02d91df40317a

#### MAIN #####
    @staticmethod
    def main():
        print("Starting discoveryworld agent\t\t")
        taskqueue = BeanStackQueue(conf.BEANSTALK_SERVER,conf.BEANSTALK_PORT)
        print("[OK]")
        PDEBUG.log("Main: Starting discoveryworld agent\t\t [OK]")
        
       

        taskqueue.test_task({"scan_type" : "geoip", "scan_data" : "8.8.8.8" })
       

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
    

