# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 00:16:16 2024

@author: kitty
"""

import logging
import conf


logging.basicConfig(filename=conf.LOG_FILE, encoding='utf-8',level=logging.DEBUG,format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
