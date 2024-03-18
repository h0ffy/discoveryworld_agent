# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import readchar
import sys, os, time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.expected_conditions import *
import chromedriver_binary

s

class SeleniumGoogle:
    def __init__(self,driver,bootstrap=False):
        self.driver = driver
        self.url = "https://www.google.com"
        self.policy = False
        self.loaded = False
        self.results = []
        
        if bootstrap == True:
            self.bootstrap_google()
        
    
    def search_google(self,search):
        self.url = "https://www.google.com/search?client=chrome&start=0&gws_rd=ssl&q={search}&filter=0&ip=1".format(search=search)        
        self.driver.get(self.url)
        
        self.scrapping_google()
        
    
    
    def more_results(self):
        try:
            element = self.driver.find_element(By.XPATH, '//*[@id="footcnt"]') #'//*[@id="botstuff"]/div/div[3]/div[4]/a[1]/h3/div/span[2]')
            return(True)
        except:
            pass
        
        print("more_results: NO")
        return(False)
        
    
    def scrapping_google(self):
        i=0
        
        for i in range(0,7):
            time.sleep(2)
            self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        
        try:
            while self.driver.find_element(By.XPATH,'//*[@id="botstuff"]/div/div[3]/div[4]/a[1]/h3/div') != None:
                self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
                self.driver.find_element(By.XPATH,'//*[@id="botstuff"]/div/div[3]/div[4]/a[1]/h3/div').click()
                time.sleep(2)
        except:
            pass
        
        
        search_elements = self.driver.find_elements(By.CLASS_NAME,'MjjYud')
        i = 0
        for element in search_elements:
            a = element.find_element(By.TAG_NAME,'a')
            #span = element.find_elements(By.TAG_NAME,'span')
            #print(span[0].get_attribute('innerHTML'))
            #div = element.find_element(By.CLASS_NAME,'ITZIwc')
            href = a.get_attribute('href'))
            self.results.append(href)
                    
        return(self.results)
    

    def bootstrap_google(self):
        if self.loaded == False:
            self.load_google()
        if self.policy == False:
            self.bypass_policy()
        
    def load_google(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(5)
        self.loaded = True
    
    def bypass_policy(self):
        try:
            self.driver.find_element(By.ID,'L2AGLb').click()
            self.driver.implicitly_wait(2)
            self.policy = True
            return(True)
        except:
            pass
    
        return(False)