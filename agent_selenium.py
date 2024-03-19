# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import readchar
import sys, os, platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.expected_conditions import *
import chromedriver_binary
from selenium_google import SeleniumGoogle

import logging

__type__ = "Selenium"
__path__ =  os.path.dirname(os.path.abspath(__file__))

if platform.system() == "win32":
    __chromedriver_path__ = "{}{}".format(__path__,"/chromedriver.exe")
else:
    __chromedriver_path__ = "{}{}".format(__path__,"/chromedriver")


if __type__ == "Selenium":
    driver = webdriver.Chrome()
    driver.get("about:blank")
    
    """ // Functional call to selenium_google plugin
    google = SeleniumGoogle(driver)
    google.load_google()
    google.bypass_policy()
    google.search_google("JennyLab")
    
    for result in google.results:
        print(result)
    """
    
    
    print("Press key to end [s/n]:", end="")
    sys.stdout.flush()
    print(readchar.readchar())
    driver.close()
    