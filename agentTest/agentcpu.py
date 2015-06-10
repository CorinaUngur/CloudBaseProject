from send import *
import wmi
import datetime
import time

class AgentCpu(Agent):
	w = wmi.WMI()
	seconds_to_sleep = 30

	def __init__(self, seconds_to_sleep = 30):
		print "entered init"
		Agent.__init__(self)

		self.seconds_to_sleep = seconds_to_sleep
		self.table = ["AgentCPU", {"load":"Integer", "date":"String"}]
		self.table_name = "AgentCPU"
		
		self.__register__()
		print str(self.table)
		print self.table_name

	def start(self):
		while(True):
			l = self.w.Win32_Processor()[0].LoadPercentage
			d = datetime.datetime.now()
			self.send_values({"load":l, "date":str(d)})

			time.sleep(self.seconds_to_sleep)


