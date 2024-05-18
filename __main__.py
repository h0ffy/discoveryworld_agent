# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 03:00:49 2024

@author: kitty
"""


from discoveryagent import *
from discoveryserv import *
if __name__ == "__main__":
	DiscoveryAgent.banner()
	"""
	#with daemon.DaemonContext():
	with Daemonizer() as (is_setup,daemonizer):
		if is_setup:
			nop=0x90

		is_parent, arg1, arg2 = daemonizer(200)

		if is_parent:
			print("BYE BYE!!!")
	"""
	DiscoveryAgent.main()
	#DiscoveryServ.main()