# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 23:15:50 2024

@author: kitty
"""

import os,sys
import logging
from time import gmtime, strftime
from conf import *


class PDEBUG:
    @staticmethod
    def log(text):
        if conf.DEBUG == True:
            logging.DEBUG(text)
            print("{}\tDiscoveryAgent\t{}\t".format(text,strftime("%d %b %Y %H:%M:%S", gmtime())))