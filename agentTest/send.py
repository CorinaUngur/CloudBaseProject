import pika
import uuid
import json


class Agent(object):
	table = []
	table_name = ''

	def __init__(self):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
		self.channel = self.connection.channel()

 		self.callback_queue_reg = self.channel.queue_declare(exclusive=True).method.queue
 		self.callback_queue_sts = self.channel.queue_declare('statistics_response').method.queue

		self.channel.queue_declare(queue='keys', durable=False)
		self.channel.queue_declare(queue='values', durable=False)
		self.channel.queue_declare(queue='statistics', durable=False)

		self.channel.basic_consume(self.on_register_response, no_ack=True, queue=self.callback_queue_reg)
		self.channel.basic_consume(self.on_statistics_response, no_ack=True, queue=self.callback_queue_sts)




	def on_register_response(self, ch, method, props, body):
		if body=='True':
			print "Agent registered successfullyy"
		else:
			print "There's been a problem with the table configuration"

		self.response = "received"


	def __register__(self):
		"""sends to the server a json with the table name and the columns names and types, 
		the server tries to create the specific table and sends back a acknowledgement "True" if the table was created successfully"""
		self.response = None

		corr_id = str(uuid.uuid4())
		self.channel.basic_publish(exchange='',
									routing_key='keys',
									properties=pika.BasicProperties(
									reply_to = self.callback_queue_reg,
									correlation_id = corr_id,
									content_type="application/json",
									delivery_mode = 1
									),
									body=json.dumps(self.table))
		print "keys sent"
		while self.response is None:
			self.connection.process_data_events()

		print "end of registration"

	def send_values(self, values):
		"""sends a json with the values and the table name to the server"""
		s = [self.table_name, values ]
		self.channel.basic_publish(exchange='',
					 routing_key='values', 
					 properties=pika.BasicProperties(content_type="application/json", delivery_mode = 1), 
					 body=json.dumps(s))

	def get_last_entries(self, no):
		"""sends a request for last no number of rows in its table"""
		s = [self.table_name , no]
		self.response = None

		corr_id = str(uuid.uuid4())
		self.channel.basic_publish(exchange='',
									routing_key='statistics',
									properties=pika.BasicProperties(
									reply_to = self.callback_queue_sts,
									correlation_id = corr_id,
									content_type="application/json",
									delivery_mode = 1
									),
									body=json.dumps(s))

		while self.response is None:
			self.connection.process_data_events()

		print "end of registration"

	def close_connection(self):
		self.connection.close()

	def on_statistics_response(self, ch, method, props, body):
		print body
		self.response = 'received'

	def __set_table__(self, t):
		self.table = t

