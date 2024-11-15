import sys, os, platform
#from regex_log_parser import LogProcessor, HandlerBase
import hashlib
#import psutil
import time
import re
import json
import conf
import ifaddr 
from conf import *
from beanstalk import *

import beanstalk



class MonitorSystem():
    def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs):
        self.monitor=0

    @staticmethod
    def get_environ():
        result = ""
        for item in os.environ:
            result+=json.loads({ "name" : item, "value" : os.environ[item]})

        result.rstrip(result[-1])
        result.rstrip(result[-1])
        result=result.encode("utf-8")
        return(result)



    @staticmethod
    def start(sensor="any"):
        environ = json.dumps({ "sensor" : sensor, "type": "os.environ", "data" : str(base64.b64encode(MonitorSystem.get_environ()))})
        print(environ) # DEBUG
    



    @staticmethod
    def agent_log(sensor,type,data):
        taskqueue = BeanStackQueue(conf.BEANSTALK_SERVER,conf.BEANSTALK_PORT)
        taskqueue.output({ "sensor" : sensor, "type" : type, "data" : data })
    


    def __run__(self):
        self.start()
    def run(self):
        self.__run__()


