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
        if DEBUG == True:
            logging.log(logging.DEBUG, msg=text)
            print("{} DiscoveryAgent {}\t".format(strftime("%d %b %Y %H:%M:%S", gmtime()),text))
