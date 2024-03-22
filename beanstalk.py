# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 23:06:03 2024

@author: kitty
"""

from pystalk import BeanstalkClient
import json

from conf import *
from debug import *

class BeanStackQueue:
    def __init__(self,server,port,auto=True):
        self.status = auto
        self.client = None
        self.output = None
        self.job_data = None
        self.server = server
        self.port = port
        
        PDEBUG.log("BeanStackQueue: Loading BeanStackQueue class (beantalk.py)")
        if auto == True:
            self.run()
    def __close__(self):
        self.__exit__()
    def __exit__(self):
        if self.status == True and self.client != None:
            self.status = False
            self.client.release()
            self.client = None

    def run(self):
        PDEBUG.log("Running BeanStackQueue.run()")
        self.status = True
        
        try:
            PDEBUG.log("BeanStackQueue: Connecting to {} server on port {}".format(self.server,self.port))
            self.client = BeanstalkClient(self.server,self.port)    
            
        except:
            self.client = None
            PDEBUG.log("BeanStackQueue: Error connect to {} server on port {}".format(self.server,self.port))
            self.__exit__()
            
        
        PDEBUG.log("BeanStackQueue: Connected found to {} server on port {}".format(self.server,self.port))
        
        

    def recv(self,queue_name):
        try:
            self.client.watch(queue_name)
            PDEBUG.log("BeanStackQueue: watch jobs from {}".format(queue_name,self.job_data))
        except:
            PDEBUG.log("BeanStackQueue: Error loading {} queue name [ERROR]".format(queue_name))
        
        try:
            for job in self.client.reserve_iter():
                self.job_data=job.job_data
                PDEBUG.log("BeanStackQueue: job from {} data ({})".format(queue_name,self.job_data))
            
        except:
            PDEBUG.log("BeanStackQueue: error job from {} data ({}) [ERROR]".format(queue_name,self.job_data))
        
    def output(self,event):
        with self.client.using("master.output") as insterter:
            inserter.put_job(json.dumps(event))