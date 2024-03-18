# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 17:29:16 2024

@author: kitty
"""

import httpx
import os,platform,sys



class HxGoogle:
    def __init__(self,query):
        self.url="https://www.google.com/?q={search}"
        self.url=self.url.format(search=query)
        self.load(self.url)
        
    
    def load(self,url):
        headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
        with httpx.Client(headers=headers,base_url="https://www.google.com") as client:
            res = client.get(self.url,headers=headers)
            print(res.text)
