#!/usr/bin/env python
#	DiscoveryWorld Agent
#	Written by A.... / JennySec

import sys,os
import conf
import tldextract 
import urllib3
import bs4
import sublist3r
from conf import *


class SubDomains:
    def __init__(self,domain):
        self.tld = tldextract.extract(domain)
        self.domain = self.tld.registered_domain
        self.domains = []
    def __enter__(self):
        return(self)
    def __del__(self):
        self.__exit__()
    def __exit__(self):
        self.domain = ""
    def run(self,scan_type="wordlist"):
        self.scan_type = scan_type

        if self.scan_type == "wordlist":
            self.sublister(False)
        elif self.scan_type == "bruteforce":
            self.sublister(True)
        else:
            nop = 0x90

            		
    def sublister(self,bruteforce=False):
        if bruteforce == True:
            subdomains = sublist3r.main(self.domain, 20, "{}_subdomains.lst".format(self.tld.domain), ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)
        else:
            subdomains = sublist3r.main(self.domain, 20, "{}_subdomains.lst".format(self.tld.domain), ports=None, silent=True, verbose=False, enable_bruteforce=True, engines=None)
                
        return(subdomains)
		
        
    # extract domains from crt.sh ( thank you 0xd0m7 )
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