import dbmanager
from sqlalchemy import *


class Test_DBManager():
	def test_all(self):
		man = dbmanager.DBManager()

		columns = {"name":"String", "note":"Integer", "number":"String"}
		man.create_table("Table1", columns)
		values = {"name":"Dorel", "note":10, "number":"12345"}
		values2 = {"name":"Cipri", "note":12, "number":"23545"}
		values3 = {"name":"Corina", "note":12, "number":"23545"}
		values4 = {"name":"Adelina", "note":12, "number":"23545"}
		values5 = {"name":"Adi", "note":12, "number":"23545"}
		values6 = {"name":"Nasu", "note":12, "number":"23545"}
		values7 = {"name":"Alexandru", "note":12, "number":"23545"}

		man.insert_into_table("Table1", values)
		man.insert_into_table("Table1", values2)
		man.insert_into_table("Table1", values3)
		man.insert_into_table("Table1", values4)
		man.insert_into_table("Table1", values5)
		man.insert_into_table("Table1", values6)
		man.insert_into_table("Table1", values7)

		result = man.select_from_table("Table1")
		result2 = man.select_from_table_lasts("Table1", 5)
		
		print "\n\n\n\n"

		for r in result:
			print r
			
		s=''
		for row in result2:
			s += str(row) + '\n'

		print s

def execute_all():
	test = Test_DBManager()
	test.test_all()