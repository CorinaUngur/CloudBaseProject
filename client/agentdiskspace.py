from periodicagent import *
import datetime
import time

class AgentDiskSpace(PeriodicAgent):
	def __init__(self, seconds_to_sleep):
		PeriodicAgent.__init__(self, seconds_to_sleep = seconds_to_sleep, 
								table_structure = ["AgentDiskSpace", {"free":"String", "date":"String"}])

	def start_process(self):
			l = str(self.w.Win32_LogicalDisk()[0].FreeSpace)
			d = datetime.datetime.now()
			self.__start_process__({"free":l, "date":str(d)})
