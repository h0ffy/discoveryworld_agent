# -*- coding: utf-8 -*-
#!/usr/bin/env python
#    DiscoveryWorld Agent
#    Written by A.... / JennySec

import sys,os
import re
import urllib, urllib3
import logging
from geoip import geolite2
from geoip import open_database
from ..config import *




class GeoIP:
    def __init__(self,ip):
        self.ip = ip
        self.country = None
        self.continent = None
        self.timezone = None
        self.db = open_database(GEOIP_DB)
        self.run()
    def __enter__(self):
        return(self)
    def __del__(self):
        self.__exit__()
    def __exit__(self):
        return(0)
    
    
    def run(self):
        result  = self.db.lookup(self.ip)
    
        
        if result is not None:
           self.country = result.country
           self.continent = result.continent
           self.timezone = result.timezone
           
           
