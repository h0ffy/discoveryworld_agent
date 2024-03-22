"""
Whois Resources

    Cloudcheck

    A simple Python utility to check whether an IP address belongs to a cloud provider.
    Domain Tools

    Find all the domains hosted on a given IP address.Track the domains that come and go.
    DREWS

    Ability to identify unauthorised domain registrations.
    Maxmind

    This link will take you to Maxmind's GeoIP2 search where you can enter upto 25 IP addresses.
    My IP

    Find Hosting Company On Any Website / Owner on Any IP Address
    RDAP

    The Registration Data Access Protocol (RDAP) is the successor to WHOIS. Like WHOIS, RDAP provides access to information about Internet resources.
    Robtex

    Robtex is used for various kinds of research of IP numbers, Domain names, etc.
    Seon

    Seon is a fraud prevention tool that allows you to check an emails, IP or telephone number.
    Synapsint

    Synapsint is a tool that allows you to collect information from different open sources on the Internet about a target such as a domain, an IP address, an email, a phone number and a Bitcoin wallet.
    Tor Whois

    TorWhois Onion Search.
    Whoisology

    Deep connections between domain names & their owners.
    WhoisXML Domain Suite

    This link will take you to the login page, where you can create a free account. The links below offer WhoisXML limited data without the need to log in.
    WhoisXML DNS

    A complete DNS records lookup product line to check the NS, MX, SPF, A, SOA, TXT, etc.
    WhoisXML IP Geolocation

    IP geolocation tools to find someone’s exact IP address location.
    WhoisXML IP Range

    Gather details about the IP range of a specific IP address such as its netblock borders, last update, organization name, country code, abuse contact information.
    WhoisXML Whois Overview

    WHOIS data domain name, IP address, or email account
    WhoisXML Whois History

    WHOIS History Lookup: Access domain name ownership history.
    Whoxy

    Search by domain, keyword, email address, company name.
"""
import sys,os
import random
from urllib import request
from ipwhois import IPWhois

from ../../..conf import *
from ../../..debug import *

class Whois:
	def __init__(self,ip):
		self.ip = ip
        self.proxy_index = random.randrange(0,len(conf.PROXY_LIST))
		self.handler = request.ProxyHandler(conf.PROXY_LIST[self.proxy_index])
    	self.run()
	def __enter__(self):
		return(self)
	def __del__(self):
		self.__exit__()
	def __exit__(self):
		self.domain = ""
	def run(self):
		self.obj = IPWhois(self.ip,proxy_opener = self.handler)
        self.results = self.obj.lookup_rdap(depth=1)
        return(self.results)
    
    
    
    


