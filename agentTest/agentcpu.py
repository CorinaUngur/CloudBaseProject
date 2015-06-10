from periodicagent import *
import datetime
import time

class AgentCpu(PeriodicAgent):
	def __init__(self, seconds_to_sleep = 30):

		PeriodicAgent.__init__(self, seconds_to_sleep = seconds_to_sleep,
								 table_structure = ["AgentCPU", {"load":"Integer", "date":"String"}])

	def start_process(self):
		while(True):
			l = self.w.Win32_Processor()[0].LoadPercentage
			d = datetime.datetime.now()
			self.send_values({"load":l, "date":str(d)})

			time.sleep(self.seconds_to_sleep)



