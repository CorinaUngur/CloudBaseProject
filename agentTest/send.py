import pika
import uuid
import json


class Agent():

	table='[{"name":"String", "val":"Integer"}]'

	def __init__(self, host="localhost"):
		self.host = host
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
		self.channel = self.connection.channel()

		self.result = self.channel.queue_declare(exclusive=True)
 		self.callback_queue = self.result.method.queue
		
		self.channel.queue_declare(queue='values')
		self.channel.queue_declare(queue='keys')

		self.channel.basic_consume(self.on_register_response, no_ack=True, queue=self.callback_queue)

		self.__register__()


	def on_register_response(self, ch, method, props, body):
		if body=='True':
			print "Agent registered successfullyy"
		else:
			print "There's been a problem with the table configuration"

		self.response = "received"


	def __register__(self):

		self.response = None

		self.corr_id = str(uuid.uuid4())
		self.channel.basic_publish(exchange='',
									routing_key='keys',
									properties=pika.BasicProperties(
									reply_to = self.callback_queue,
									correlation_id = self.corr_id,
									content_type="application/json"
									),
									body=self.table)
		print "keys sent"
		while self.response is None:
			self.connection.process_data_events()

		print "end of registration"

	def send_values(self, values):
		self.channel.basic_publish(exchange='',
					 routing_key='values', 
					 properties=pika.BasicProperties(content_type="application/json"), 
					 body=json.dumps(values))

	def close_connection(self):
		self.connection.close()

