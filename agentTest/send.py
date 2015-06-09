import pika
import uuid
import json


class Agent():

	table='["Agent2", {"name":"String", "val":"Integer"}]'
	table_name = "Agent2"

	def __init__(self, host="localhost"):
		self.host = host
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
		self.channel = self.connection.channel()

 		self.callback_queue_reg = self.channel.queue_declare(exclusive=True).method.queue
 		self.callback_queue_sts = self.channel.queue_declare('statistics_response').method.queue
		
		self.channel.queue_declare(queue='values')
		self.channel.queue_declare(queue='keys')
		self.channel.queue_declare(queue='statistics')

		self.channel.basic_consume(self.on_register_response, no_ack=True, queue=self.callback_queue_reg)
		self.channel.basic_consume(self.on_statistics_response, no_ack=True, queue=self.callback_queue_sts)

		self.__register__()


	def on_register_response(self, ch, method, props, body):
		if body=='True':
			print "Agent registered successfullyy"
		else:
			print "There's been a problem with the table configuration"

		self.response = "received"


	def __register__(self):

		self.response = None

		corr_id = str(uuid.uuid4())
		self.channel.basic_publish(exchange='',
									routing_key='keys',
									properties=pika.BasicProperties(
									reply_to = self.callback_queue_reg,
									correlation_id = corr_id,
									content_type="application/json"
									),
									body=self.table)
		print "keys sent"
		while self.response is None:
			self.connection.process_data_events()

		print "end of registration"

	def send_values(self, values):
		s = '["' + self.table_name + '", ' + str(values) + ']'
		self.channel.basic_publish(exchange='',
					 routing_key='values', 
					 properties=pika.BasicProperties(content_type="application/json"), 
					 body=s)

	def get_last_entries(self, no):
		s = '["' + table_name + '", ' + str(no) + ']'
		self.response = None

		corr_id = str(uuid.uuid4())
		self.channel.basic_publish(exchange='',
									routing_key='statistics',
									properties=pika.BasicProperties(
									reply_to = self.callback_queue_sts,
									correlation_id = corr_id,
									content_type="application/json"
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

