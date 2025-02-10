#!/usr/bin/env python
#	DiscoveryWorld Agent
#	Written by Alberto Garcia de Dios a.k.a @h0ffy / JennyLab
#   CopyRight 2025 @JennyLab
#

import sys,os
import time
import threading
import conf
#import daemon
import logging
import logger
import json
from debug import * 
from beanstalk import *
import base64
from mysql.connector import connection
import mysql.connector
#from cassandra.cluster import Cluster
#from cassandra import ConsistencyLevel


class DiscoveryServ:
    """
    A class used to represent the Discovery Service.
    Methods
    -------
    banner():
        Prints the banner for the DiscoveryWorld Agent.
    out_mydb(sql_query, sql_data):
        Executes an SQL query with the provided data and commits the transaction.
    server_task(taskqueue, scan_type, scan_data):
        Processes the scan task based on the scan type and scan data, and inserts the results into the database.
    main():
        The main method to start the discovery world server, process tasks from the task queue, and handle scan jobs.
    """


    @staticmethod
    def banner():
        """This static methods to print banner"""
    	print("\t*****************************************************************")
    	print("\t*\t\t\t\t\t\t\t\t*")
    	print("\t*\t\t\tDiscoveryWorld Agent\t\t\t*")
    	print("\t*\t\t\t\t\t\t\t\t*")
    	print("\t*****************************************************************")

    @staticmethod
    def out_mydb(sql_query,sql_data):
        """
        @brief      Static method is to output data to MySQL
        @params      sql_query (query in mysql)
                    sql_data (data fill query)
        @return     None
        """ 
        cnx = connection.MySQLConnection(user="root", password="jennylab", host="127.0.0.1", database="DISCOVERY", port=3307)
        cursor = cnx.cursor()
        print("Insert SQL DATA: ", end="")
        print(sql_data)
        cursor.execute(sql_query, sql_data)
        cnx.commit()

    @staticmethod
    def server_task(taskqueue,scan_type,scan_data):
        """
        @brief      Static method is to process scan task
        @params      taskqueue (task queue to get the job)
                    scan_type (type of scan)
                    scan_data (data to be processed)
        @return     None
        """ 
        if scan_type is None:
            PDEBUG.log("DiscoveryServ::server_task: Invalid scan_type is None")
            #print("DiscoveryServ::server_task: Invalid scan_type is None")
        elif scan_data is None:
            PDEBUG.log(f"DiscoveryServ::server_task: Invalid {scan_type} scan_data is None")
            #print("DiscoveryServ::server_task: Invalid {} scan_data is None".format(scan_type))
        else:
            if scan_type == "subdomains":
                sql_query = ("INSERT INTO SUBDOMAINS (DOMAIN,SUBDOMAIN,IP) VALUES (%s,%s,%s)")
                data_plain = base64.b64decode(scan_data).decode('utf-8')
                print(data_plain)
                data_json = json.loads(data_plain)

                try:
                    str_domain = data_json["DOMAIN"]
                except:
                    str_domain = "ERROR"
                    pass

                try:
                    str_subdomain = data_json["SUBDOMAINS"]
                except:
                    str_subdomain = "ERROR"
                    pass

                try:
                    str_ip = data_json["IP"]
                except:
                    str_ip = "ANY"
                    pass

                print("DATA: {} {} {}".format(str_domain,str_subdomain,str_ip))

                sql_data = (str_domain,str_subdomain,str_ip)
                DiscoveryServ.out_mydb(sql_query,sql_data)


                """
                    ip = scan_data
                    domains_result = ip2domain.IP2Domain(ip)
                    domains_result.domains = list(set(newIP2Domain.domains))
                    if domains.result is not None:
                        if domains.result.domains is not None:
                            for domain in domains.result.domains:
                                task.output('{ "agent" : "null" , "plugin" : "agent_scan.ip2domain", "ip" : "{}", "domain" : "{}" }'.format(ip,domain))
                """
            elif scan_type == "ip" or scan_type == "geoip":
                print("SCAN_DATA")
                print(scan_data)
                sql_query = ("INSERT INTO IPV4 (IP,GEO) VALUES (%s,%s)")

                data_plain = base64.b64decode(scan_data).decode('utf-8')
                data_json = json.loads(data_plain)

                try:
                    str_ip  = data_json["IP"]
                except:
                    str_ip  = "0.0.0.0"

                try:
                    str_geo = data_json["COUNTRY"]

                except:
                    str_geo = "ANY"


                sql_data = (str_ip,str_geo)
                DiscoveryServ.out_mydb(sql_query,sql_data)

                print("DATA2: {} {}".format(str_ip,str_geo))


            else:
                nop = 0x90

                """
                elif scan_type == "subdomain-wordlist":
                    objSubDomain = SubDomains(scan_data)
                    objSubDomain.run(bruteforce=False)
                    strDomains = None
                    if objSubDomain.result is not None:
                        for subdomain in objSubDomain.result:
                            strDomains+=str("{};".format(subdomain))
                        
                        strDomains =strDomains.removesuffix(';')
                        queue.output({"agent" : "null", "plugin" : "agent_scan.subdomain-wordlist",  "domain": scan_data, "subdomains" : strDomains})
                elif scan_type == "subdomain-bruteforce":
                    objSubDomain = SubDomains(scan_data)
                    objSubDomain.run(bruteforce=True)
                    strDomains = None
                    if objSubDomain.result is not None:
                        for subdomain in objSubDomain.result:
                            strDomains+=str("{};".format(subdomain))
                        
                        strDomains=strDomains.removesuffix(';')
                        queue.output({"agent" : "null", "plugin" : "agent_scan.subdomain-bruteforce",  "domain": scan_data, "subdomains" : strDomains})
                """


                #skelDict = { "agent" : "null", "plugin" : "agent_scan.geoip", "ip" : ip, "country" : result.country, "continent" : result.continent, "timezone" : result.timezone }
                #taskqueue.report(skelDict)
                #print(skelDict)
                #return(skelDict)


#### MAIN #####
    @staticmethod
    def main():
        print("Starting discoveryworld SERVER\t\t")
        taskqueue = BeanStackQueue(conf.BEANSTALK_SERVER,conf.BEANSTALK_PORT)
        print("[OK]")
        PDEBUG.log("Main: Starting discoveryworld SERVER\t\t [OK]")
        
        taskqueue.client.use("master.output")
        tmp_data = "eyAiZGF0YV90eXBlIiA6ICJzdWJkb21haW5zIiwgIkRPTUFJTiIgOiAiamVubnlsYWIubWUiLCAiU1VCT0RPTUFJTlMiIDogInZwbi5qZW5ueWxhYi5tZSIsICJJUCIgOiAiMS4xLjEuMSIgfQ=="
        taskqueue.output({"type" : "subdomains", "data" : tmp_data })
        taskqueue.output({"type": "subdomains", "data": tmp_data})
        taskqueue.output({"type": "subdomains", "data": tmp_data})
        taskqueue.output({"type": "subdomains", "data": tmp_data})
        #taskqueue.test_task({"type": "subdomains", "data": tmp_data})
        #taskqueue.test_task({"type": "subdomains", "data": tmp_data})

        task_data = None
        task_type = None
        while 1:
            job = taskqueue.recv("master.output")
            if job is not None and job != b"null":
                if job.job_data is not None:
                    PDEBUG.log("Main: recv\t\t OK")
                    print(job.job_data)
                    try:
                        data = dict(json.loads(job.job_data))
                        task_type = data.get("type")
                        task_data = data.get("data")
                    except:
                        data = dict({ "type" : "error", "data" : "error" })
                        pass

                    PDEBUG.log("Main: Init scan job {} with data {}".format(task_type,task_data))
                    result = DiscoveryServ.server_task(taskqueue,task_type,task_data)
                    #taskqueue.report(result)
                    taskqueue.release(int(job.job_id))
                #done
                #taskqueue.report(result)

            time.sleep(2)
        
        sys.exit(0)
        return(0)


