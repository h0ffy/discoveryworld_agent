# -*- coding: utf-8 -*-
#!/usr/bin/env python
#	DiscoveryWorld Agent
#	Written by A.... / JennySec

import sys,os,socket
import re
import urllib, urllib2
import logging
from geoip import geolite2
from ../../..conf import *
from ../../..debug import *




class GeoIP:
	def __init__(self,ip):
        logging.logger(__name__)
		self.ip = ip
		self.country = None
        self.continent = None
        self.timezone = None
		self.run()
	def __enter__(self):
		return(self)
	def __del__(self):
		self.__exit__()
	def __exit__(self):
        return(0)
    
    
    def run(self):
        result  = geolite2.lookup(self.ip)
        if result is not None:
           self.country = result.country
           self.continent = result.continent
           self.timezone = result.timezone
           
           