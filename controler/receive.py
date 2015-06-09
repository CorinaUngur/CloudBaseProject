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
		self.channel.queue_declare(queue='statistics')

		self.manager=dbmanager.DBManager()

	def on_receive_keys(self, ch, method, props, body):
		print "keys received: " + body
		ch.basic_ack(delivery_tag = method.delivery_tag)
		table_name = json.loads(body)[0]
		keys = json.loads(body)[1]
		print "decoded keys: " + str(keys)
		self.manager.create_table(table_name, keys)

		ch.basic_publish(exchange='',
							routing_key=props.reply_to,
							properties=pika.BasicProperties(correlation_id = \
													props.correlation_id),
							body='True')

		print "Acknowledgement sent to ctrl"


	def on_receive_values(self, ch, method, props, body):
		print body
		table_name = json.loads(body)[0]
		values = json.loads(body)[1]

		self.manager.insert_into_table(table_name, values)
		result = self.manager.select_from_table(table_name)

		#for debug puposes uncomment the next section (or comment it if it is uncommented)
		for row in result:
			print row

	def on_statistics_request(self, ch, method, props, body):
		table_name = json.loads(body)[0]
		no = int(json.loads(body)[1])
		result = self.manager.select_from_table_lasts(table_name, no)
		s=''
		for row in result:
			s += str(row) + '\n'

		ch.basic_ack(delivery_tag = method.delivery_tag)

		ch.basic_publish(exchange='',
							routing_key=props.reply_to,
							properties=pika.BasicProperties(correlation_id = \
													props.correlation_id),
							body=s)


	def start(self):
		self.channel.basic_consume(self.on_receive_keys, queue='keys')
		self.channel.basic_consume(self.on_receive_values, queue='values')
		self.channel.basic_consume(self.on_statistics_request, queue='statistics')

		print " [x] Awaiting for keys and values"

		self.channel.start_consuming()
