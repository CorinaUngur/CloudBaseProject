from sqlalchemy import *


class DBManager:
	indexes = {}

	def __init__(self):
		self.engine = create_engine('sqlite:///:memory:', echo=True)
		self.metadata = MetaData()
		self.conn = self.engine.connect()


	def create_table(self, name, table):
		"""creates a table with the name sepcified by name parameter and the column specified in the dict table_name
			table will have the column names as keys and the column types as values"""

		code = "t = Table('" + name + "', self.metadata, Column('id', Integer, primary_key=True)"
		columns = ''
		for k,v in table.items():
			col = "Column('" + k + "'," + v + ")"
			columns += "," + col 

		code += columns + ")"
	
		exec code

		self.indexes[name] = 0

		t.create(self.engine, checkfirst=True)


	def insert_into_table(self, table_name, table_values):
		"""inserts into table table_name values received in the dict table_values
			there is no need for the id value to be in table_values 'cause it is added automatically"""

		table = Table(table_name, self.metadata)
		table_values['id']= self.__get_next_index__(table_name)
		ins = table.insert().values(table_values)
		self.conn.execute(ins)

	def __get_next_index__(self, table_name):
		""" returns the next id for a new item to be added in the table table_name"""

		index = self.indexes.get(table_name)
		index+=1
		self.indexes[table_name] = index

		return index

	def select_from_table(self, table_name):
		"""returns the result of the select * from table_name"""
		table = Table(table_name, self.metadata)
		sel = select([table])
		result = self.conn.execute(sel)

		return result
