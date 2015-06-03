import pika
import uuid


class Agent:
	def __init__(self, host="localhost"):
		self.host = host
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
		self.channel = self.connection.channel()

		self.result = self.channel.queue_declare(exclusive=True)
 		self.callback_queue = self.result.method.queue
		
		self.channel.queue_declare(queue='values')
		self.channel.queue_declare(queue='keys')

		self.channel.basic_consume(self.on_key_response, no_ack=True, queue=self.callback_queue)

	def set_info(self, dictt={}):
		self.keys = ''
		self.values = ''
		for k, v in dictt.iteritems():
			self.keys += str(k) + ' '
			self.values += str(v) + ' '


	def on_key_response(self, ch, method, props, body):
		self.response = 'received'
		print 'response received'
		self.channel.basic_publish(exchange='', routing_key='values', body=self.values)


	def send_keys(self):
		self.response = None

		self.corr_id = str(uuid.uuid4())
		self.channel.basic_publish(exchange='',
									routing_key='keys',
									properties=pika.BasicProperties(
									reply_to = self.callback_queue,
									correlation_id = self.corr_id,
									),
									body=self.keys)
		print '# Sent keys: ' + self.keys
		while self.response is None:
			self.connection.process_data_events()

	def close_connection(self):
		self.connection.close()

