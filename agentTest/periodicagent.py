import wmi
from send import *

class PeriodicAgent(Agent):
	w = wmi.WMI()
	seconds_to_sleep = 30

	def __init__(self, table_structure, seconds_to_sleep = 30):

		Agent.__init__(self)

		self.seconds_to_sleep = seconds_to_sleep
		self.table = table_structure
		self.table_name = self.table[0]
		
		self.__register__()

	def set_interval(self, seconds):
		self.seconds_to_sleep = seconds

