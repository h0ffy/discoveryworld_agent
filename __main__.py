# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 03:00:49 2024

@author: kitty
"""
from discoveryagent import *
from discoveryserv import *
from monitor_syslog import *
from monitor_system import *

if __name__ == "__main__":
#	DiscoveryAgent.banner()
#	DiscoveryServ.main()
	#MonitorLog.read_file(sys.argv[1])
	#sys.exit(0)

	if len(sys.argv) <= 1:
		DiscoveryAgent.main()
	else:
		arg1 = sys.argv[1]

		if  arg1 == "agent":
			DiscoveryAgent.main()
		elif arg1 == "server":
			DiscoveryServ.main()
		elif arg1 == "insert":
			BeanStackQueue.beanstalk_cli(cmd=sys.argv[2],data=sys.argv[3])
		elif arg1 == "monitor":
			MonitorLog.read_file(sys.argv[2])
		elif arg1 == "monitor-system":
			MonitorSystem.run()
		else:
			DiscoveryAgent.main()

