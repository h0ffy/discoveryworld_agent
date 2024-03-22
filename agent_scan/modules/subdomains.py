#!/usr/bin/env python
#	DiscoveryWorld Agent
#	Written by A.... / JennySec

import sys,os
import conf
import commands
import tldextract 
import urllib3
import beatifoulsoup
import panda as pd

class SubDomains:
	def __init__(self,domain):
		tld = tldextract.extract(domain)
		self.domain = tld.domain + "." + tld.suffix
		self.domains = []
		self.run()
	def __enter__(self):
		return(self)
	def __del__(self):
		self.__exit__()
	def __exit__(self):
		self.domain = ""
	def run(self):
		self.sublister()		
							
	def sublister(self):
		output_file = "/tmp/%s.txt" % (self.domain)
		command1_format1 = 'python dist/sublist3r/sublist3r.py -t 1 -o /tmp/%s.txt -d %s' % (self.domain,self.domain)
		try:
		        commands.getoutput(command1_format1)
		        f = open(output_file,'r')
		        subdomains = f.readlines()		
		        f.close()
		        os.remove(output_file)
			
			for subdomain in subdomains:
				self.domains.append(subdomain.strip("\n").strip("\r"))
		except:
		        pass
		        self.domains=[]
		
        
    # extract domains from crt.sh ( thasnk you 0xd0m7 )
    def crt_sh(self):
		uri = 'https://crt.sh/?q={}'.format(self.domain)
		response = urllib3.request("GET",uri)
		html = resp.data
        soup = BetifoulSoup(html,'html.parser')
        soup.find('table')
		for row in table.find_all('tr'):
            cols = row.find_all('td')
    
            self.domains.append(cols[4])
            for domain in cols[5].split("<BR>"):
                self.domains.append(domain)
         
            """
            i=0            
            for field in cols:
                if i==4:
                    self.domains.append(field)
                elif i==5:
                    for domain in field.split("<BR>")
                        self.domains.append(domain)
                i+=1
            """