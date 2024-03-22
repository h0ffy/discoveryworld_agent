#!/usr/bin/env python
#	DiscoveryWorld Agent
#	Written by A.... / JennySec

import sys,os,socket
import re
import urllib, urllib2
import logging
from ../../..conf import *
from ../../..debug import *
#import ip2domain



class IP2Domain:
	def __init__(self,ip):
        logging.logger(__name__)
		self.ip = ip
		self.domains = []
		self.run()
	def __enter__(self):
		return(self)
	def __del__(self):
		self.__exit__()
	def __exit__(self):
		i=0
		for domain in self.domains:
			self.domains[i] = ""
			i+=1
	def run(self):
		#self.ip2host()
        PDEBUG.log("IP2Domain: Bing2IP {}".format(self.ip))
		self.bing2ip()
        PDEBUG.log("IP2Domain: crt.sh {}".format(self.ip))
        self.crt_sh()

	def bing2ip(self):
			page = 0
			uri_format = 'https://www.bing.com/search?q=IP%%3A{ip}&qs=n&FORM=PQRE&pq=IP%%3A{ip}&first={page}'	
			i = 0	

			for i in range(0,4):
				uri = uri_format.format(ip=self.ip,page=page)
				response = urllib2.urlopen(uri)
				raw_html = response.read()
				response.close()
				page = int((page/10+1) + (page+10))
				extracted = re.findall('<li\sclass="b_algo".*?href="(.*?)".*?</a>',raw_html)
				
				for extracted_url in extracted:
					domain = re.findall(r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}',extracted_url)
					final = domain[0].strip("\n").strip("\r")
					self.domains.append(final)
			
				i+=1	

							

			

	def ip2host(self):
			uri = "http://www.ip2hosts.com/csv.php?ip={}".format(self.ip)
			response = urllib2.urlopen(uri)
			raw_csv = response.read()
			response.close()
			domains_list = raw_csv.split(",")
			for domain in domains_list:
				if(domain!=""):
					domain = domain.strip("\n").strip("\r").strip("http:\/\/").strip("https:\/\/")
					self.domains.append(domain)		
			


    def crt_sh(self):
		uri = 'https://crt.sh/?q={}'.format(self.ip)
		response = urllib3.request("GET",uri)
		html = resp.data
        soup = BetifoulSoup(html,'html.parser')
        soup.find('table')
		for row in table.find_all('tr'):
            cols = row.find_all('td')
            if cols[4] != self.ip
                self.domains.append(cols[4])
            for domain in cols[5].split("<BR>"):
                if domain != self.ip    
                    self.domains.append(domain)


