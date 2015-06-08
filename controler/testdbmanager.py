import dbmanager
from sqlalchemy import *


class Test_DBManager():
	def test_all(self):
		man = dbmanager.DBManager()

		columns = {"name":"String", "note":"Integer", "number":"String"}
		man.create_table("Table1", columns)
		values = {"name":"Dorel", "note":10, "number":"12345"}
		man.insert_into_table("Table1", values)

		result = man.select_from_table("Table1")
		
		print "\n\n\n\n"

		for r in result:
			print r

def execute_all():
	test = Test_DBManager()
	test.test_all()