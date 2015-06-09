import pika
import json
import dbmanager

class Controller():
	def __init__(self, host='localhost'):
		connection = pika.BlockingConnection(pika.ConnectionParameters(
		host='localhost'))

		self.channel = connection.channel()

		self.channel.queue_declare(queue='keys')
		self.channel.queue_declare(queue='values')

		self.manager=dbmanager.DBManager()

	def on_receive_keys(self, ch, method, props, body):
		print "keys received: " + body
		ch.basic_ack(delivery_tag = method.delivery_tag)
		keys = json.loads(body)[0]
		print "decoded keys: " + str(keys)
		self.manager.create_table("Name1", keys)

		ch.basic_publish(exchange='',
							routing_key=props.reply_to,
							properties=pika.BasicProperties(correlation_id = \
													props.correlation_id),
							body='True')

		print "Acknowledgement sent to ctrl"


	def on_receive_values(self, ch, method, props, body):
		self.manager.insert_into_table("Name1", json.loads(body))
		self.manager.select_from_table("Name1")

	def start(self):
		self.channel.basic_consume(self.on_receive_keys, queue='keys')
		self.channel.basic_consume(self.on_receive_values, queue='values')

		print " [x] Awaiting for keys and values"

		self.channel.start_consuming()
