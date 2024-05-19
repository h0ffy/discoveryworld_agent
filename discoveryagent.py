#!/usr/bin/env python
#	DiscoveryWorld Agent
#	Written by h0ffy / JennyLab
#   GNU GPL 3.0 CopyLeft 2024 @JennyLab

import sys,os
#import urllib, urllib2
import time
import threading
import conf
import logging
import logger
import json
import base64
#import ip2domain
#from agent import ClientAgent
from debug import * 
from beanstalk import *
from agent_scan.modules.ip2domain import *
from agent_scan.modules.discoverygeoip import *
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
    def agent_scan(taskqueue,scan_type,scan_data):
        result = None

        if scan_type == "reverse-domain":
            ip = scan_data
            domains_result = ip2domain.IP2Domain(ip)
            domains_result.domains = list(set(newIP2Domain.domains))
            if domains.result is not None:
                if domains.result.domains is not None:
                    for domain in domains.result.domains:
                        bdata="eyAiZGF0YV90eXBlIiA6ICJzdWJkb21haW5zIiwgIkRPTUFJTiIgOiAiamVubnlsYWIubWUiLCAiU1VCT0RPTUFJTlMiIDogInZwbi5qZW5ueWxhYi5tZSIsICJJUCIgOiAiMS4xLjEuMSIgfQ=="
                        taskqueue.output({ "type" : "subdomains", "data" : bdata,  "agent" : "null" , "plugin" : "agent_scan.ip2domain", "ip" : ip, "domain" : domain })
        elif scan_type == "geoip":
            ip = scan_data
            result = dict({ "country" : "US", "continent" : "ANY", "timezone" : "ANY" , "IP" : "0.0.0.0" })
            #result = DiscoveryGeoIP(ip)
            #if result is not None:
            #print(ip,result.country)
            continent = "ANY" # result.continent
            country = "ANY" # result.country
            timezone = "ANY" # result.timezone
            bdata="eyAiZGF0YV90eXBlIiA6ICJzdWJkb21haW5zIiwgIkRPTUFJTiIgOiAiamVubnlsYWIubWUiLCAiU1VCT0RPTUFJTlMiIDogInZwbi5qZW5ueWxhYi5tZSIsICJJUCIgOiAiMS4xLjEuMSIgfQ=="
            taskqueue.output({ "type" : "geoip", "data" : bdata, "agent" : "null", "plugin" : "agent_scan.geoip", "ip" : ip, "country" : country, "continent" : continent, "timezone" : timezone })

        
        elif scan_type == "subdomain-wordlist":
            objSubDomain = SubDomains(scan_data)
            objSubDomain.run(bruteforce=False)
            strDomains = None
            if objSubDomain.result is not None:
                for subdomain in objSubDomain.result:
                    strDomains+=str("{};".format(subdomain))
                
                strDomains =strDomains.removesuffix(';')
                taskqueue.output({"agent" : "null", "plugin" : "agent_scan.subdomain-wordlist",  "domain": scan_data, "subdomains" : strDomains})
        elif scan_type == "subdomain-bruteforce":
            objSubDomain = SubDomains(scan_data)
            objSubDomain.run(bruteforce=True)
            strDomains = None
            if objSubDomain.result is not None:
                for subdomain in objSubDomain.result:
                    strDomains+=str("{};".format(subdomain))
                
                strDomains=strDomains.removesuffix(';')
                taskqueue.output({"agent" : "null", "plugin" : "agent_scan.subdomain-bruteforce",  "domain": scan_data, "subdomains" : strDomains})
        else:
            nop=0x90
                

        return(result)
            #skelDict = { "agent" : "null", "plugin" : "agent_scan.geoip", "ip" : ip, "country" : result.country, "continent" : result.continent, "timezone" : result.timezone }
            #taskqueue.report(skelDict)
            #print(skelDict)
            #return(skelDict)


#### MAIN #####
    @staticmethod
    def main():
        print("Starting discoveryworld agent\t\t")
        taskqueue = BeanStackQueue(conf.BEANSTALK_SERVER,conf.BEANSTALK_PORT)
        print("[OK]")
        PDEBUG.log("Main: Starting discoveryworld agent\t\t [OK]")
        
       
        for i in range(0,200000):
            #taskqueue.test_task({"scan_type" : "geoip", "scan_data" : "8.8.8.8" })
            bdata="eyAiZGF0YV90eXBlIiA6ICJzdWJkb21haW5zIiwgIkRPTUFJTiIgOiAiamVubnlsYWIubWUiLCAiU1VCT0RPTUFJTlMiIDogInZwbi5qZW5ueWxhYi5tZSIsICJJUCIgOiAiMS4xLjEuMSIgfQ=="
            taskqueue.output({ "type" : "test", "data" : bdata })
        sys.exit(0)

        """
        taskqueue.test_task({"scan_type": "geoip", "scan_data": "8.8.8.8"})
        taskqueue.test_task({"scan_type": "geoip", "scan_data": "8.8.8.8"})
        taskqueue.test_task({"scan_type": "geoip", "scan_data": "8.8.8.8"})
        taskqueue.test_task({"scan_type": "geoip", "scan_data": "8.8.8.8"})
        taskqueue.test_task({"scan_type": "geoip", "scan_data": "8.8.8.8"})
        taskqueue.test_task({"scan_type": "geoip", "scan_data": "8.8.8.8"})
        """

        while 1:      
            job = taskqueue.recv("agent.scan")
            if job is not None:


                if job.job_data is not None:
                    PDEBUG.log("Main: recv\t\t OK")
                    data = dict(json.loads(job.job_data))
                    try:
                        scan_type = data.get("scan_type")
                    except:
                        scan_type = "error"
                        pass

                    try:
                        scan_data = data.get("scan_data")
                    except:
                        scan_data = "error"
                        pass

                    PDEBUG.log("Main: Init scan job {} with data {}".format(scan_type,scan_data))
                    result = DiscoveryAgent.agent_scan(taskqueue,scan_type,scan_data)
                    print("RESULT: ",end="")
                    print(result)
                    result_encoded = base64.b64encode(bytes(str(result),'utf-8'))

                    result_send = dict({ "type" : "result", "data" : result_encoded.decode('utf-8') })
                    taskqueue.report(result_send)

                    taskqueue.release(int(job.job_id))
                #done
                #taskqueue.report(result)

            time.sleep(2)
        
        sys.exit(0)
        return(0)
    

