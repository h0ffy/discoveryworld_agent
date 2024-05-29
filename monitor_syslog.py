import sys, os, platform
#from regex_log_parser import LogProcessor, HandlerBase
import hashlib
#import psutil
import time
import re

import conf
from conf import *
from beanstalk import *

import beanstalk


class MonitorLog():
    def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs):
        self.monitor=0

    @staticmethod
    def execution_timer(start_time=None):
        if start_time is None:
            return time.time()

        exe_time = time.time() - start_time
        return(exe_time)


    @staticmethod
    def agent_log(sensor,type,data):
        taskqueue = BeanStackQueue(conf.BEANSTALK_SERVER,conf.BEANSTALK_PORT)
        taskqueue.output({ "sensor" : sensor, "type" : type, "data" : data })

    @staticmethod
    def read_file(file_path):
        md5hash = hashlib.md5()
        t_md5 = []
        regex_list = [{ "id" : 0, "regex" : r"^(?P<moth>\w{3})\s(?P<day>\d{1,2})\s(?P<full_hour>\d{1,2}:\d{1,2}:\d{1,2})\s(?P<author>\S+)\s(?P<proc_name>\S+)\[(?P<pid>\d+)\]:\s(?P<agent_name>\S+)\|(?P<type>\S+)\|(?P<data>\S+)$", "plugin" : "Agent Query", "function" : MonitorLog.agent_log},
                      { "id" : 1, "regex" : r"", "plugin" : "None"}
                       ]
        regex_compile = []

        regex_compile.append(re.compile(regex_list[0]["regex"]))

        """
        statinfo = os.stat(file_path)
        mem = psutil.virtual_memory()
        swapmem = psutil.swap_memory()
        if statinfo.st_size > mem.available + swapmem.free:
            print("File is larger than memory space")
        """
        while True:
            start_time = MonitorLog.execution_timer()
            current_line = 0
            seek = 0



            executed=False
            with open(file_path, "r") as f:
                while True:
                    if executed==True:
                        time.sleep(1)
                    else:
                        executed=True

                    f.seek(0)
                    data = f.read(67108864)
                    if not data:
                        if t_md5.count != 0:
                            for digest in t_md5:
                                current_digest = hashlib.md5(data.encode('utf-8')).hexdigest()
                                if current_digest == digest:
                                    time.sleep(1)
                                    current_digest = hashlib.md5(data.encode('utf-8')).hexdigest()
                                    while current_digest == digest:
                                        time.sleep(5)
                                        current_digest = hashlib.md5(data.encode('utf-8')).hexdigest()
                                else:
                                    md5hash.update(data.encode('utf-8'))
                                    t_md5.append(md5hash.hexdigest())

                        else:
                            md5hash.update(data.encode('utf-8'))
                            t_md5.append(md5hash.hexdigest())
                    """
                    file_name = file_path.split("/")[len(file_path.split("/")) - 1]
                    if md5hash.hexdigest() in file_hashes[file_name]:
                        return ["File previously read..."]
                    else:
                        file_hashes[file_path.split("/")[len(file_path.split("/")) - 1]].append(md5hash.hexdigest())
                    """
                    f.seek(seek)
                    while True:
                        line_string = ""
                        old_line = ""
                        try:
                            line_string = f.readline()
                            if not line_string:
                                seek=f.tell()
                                break
                            elif line_string == old_line and seek >= current_line:
                                time.sleep(1000)
                                break
                            else:
                                print(line_string)
                                i = 0
                                for match_line in re.findall(regex_compile[0],line_string):
                                        regex_list[i]["function"](match_line[3],match_line[7],match_line[8])
                                        #print("{} {} {}".format(match_line[6],match_line[7],match_line[8]))
                                        i+=1

                                current_line += 1
                                old_line=line_string


                        except:
                            print("Log file read line error")












    def __run__(self):
        self.log_processor.run()
    def run(self):
        self.__run__()



