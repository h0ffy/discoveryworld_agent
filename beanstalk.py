# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 23:06:03 2024

@author: kitty
"""

from pystalk import BeanstalkClient
import json
import base64

from conf import *
from debug import *

class BeanStackQueue:
    def __init__(self,server,port,auto=True):
        self.status = auto
        self.client = None
        #self.output = None
        self.job_data = None
        self.job = None
        self.server = server
        self.port = port
        
        PDEBUG.log("BeanStackQueue::BeanStackQueue: Loading BeanStackQueue class (beantalk.py)")
        if auto == True:
            self.run()
    def __close__(self):
        self.__exit__()
    def __exit__(self):
        if self.status == True and self.client != None:
            self.status = False
            self.client.release()
            self.client = None

    def output(self,outline):
        print(outline)
        self.report(outline)

    def run(self):
        PDEBUG.log("Running BeanStackQueue::run()")
        self.status = True
        
        try:
            PDEBUG.log("BeanStackQueue::run(): Connecting to {} server on port {}".format(self.server,self.port))
            self.client = BeanstalkClient(self.server,self.port)    
            
        except:
            self.client = None
            PDEBUG.log("BeanStackQueue::run(): Error connect to {} server on port {}".format(self.server,self.port))
            #self.__exit__()
            
        
        PDEBUG.log("BeanStackQueue::run(): Connected found to {} server on port {}".format(self.server,self.port))
        
        

    def recv(self,queue_name):
        try:
            self.client.watch(queue_name)
            PDEBUG.log("BeanStackQueue::rev(): Watch jobs from {} [OK]".format(queue_name,self.job_data))
        except:
            PDEBUG.log("BeanStackQueue::recv(): Error loading {} queue name [ERROR]".format(queue_name))
        
        try:
            #for job in self.client.reserve_iter():
            for job in self.client.reserve_iter():
                self.job = job
                self.job_data=job.job_data
                self.job_id=job.job_id
                self.client.bury_job(self.job_id)
                #  self.client.execute_job(job)
                PDEBUG.log("BeanStackQueue::recv(): Job {} from {} data ({}) [OK]".format(self.job_id,queue_name,self.job_data))
                return(self.job)
            
        except:
            PDEBUG.log("BeanStackQueue::recv(): Error job from {} data ({}) [ERROR]".format(queue_name,self.job_data))
            return(None)

    def release(self,job_id):
        #self.client.release_job(job_id)
        self.client.delete_job(job_id)

    def test_task(self,event):
        PDEBUG.log("BeanStackQueue::test_task({})".format(event))
        self.client.use("agent.scan")
        with self.client.using("agent.scan") as inserter:
            inserter.put_job(json.dumps(event))    
    
    def report(self,event):
        PDEBUG.log("BeanStackQueue::report({})".format(event))
        self.client.use("master.output")
        with self.client.using("master.output") as inserter:
            inserter.put_job(json.dumps(event))

    @staticmethod
    def addReportRaw2Test(tqueue,ncount):
        for i in range(1,ncount):
            bdata="eyAiZGF0YV90eXBlIiA6ICJzdWJkb21haW5zIiwgIkRPTUFJTiIgOiAiamVubnlsYWIubWUiLCAiU1VCT0RPTUFJTlMiIDogInZwbi5qZW5ueWxhYi5tZSIsICJJUCIgOiAiMS4xLjEuMSIgfQ=="
            tqueue.output({ "type" : "test", "data" : bdata })


    @staticmethod
    def addTaskRaw2Text(tqueue,ncount):
        for i in range(1,ncount):
            tqueue.test_task({"scan_type": "geoip", "scan_data": "8.8.8.8"})



    @staticmethod
    def mkevent(type,data):
        return({'type' : type, 'data': str(base64.encode(data)) })


    @staticmethod
    def beanstalk_cli(cmd,data):
        try:
            cli_client = BeanstalkClient("127.0.0.1",13120)
            #task = cli_client.use("agent.scan")
            with cli_client.using("agent.scan") as inserter:
                inserter.put_job(json.dumps({ "scan_type" : cmd, "scan_data" : data }))
        except Exception as e:
            PDEBUG.log(f"{}")
