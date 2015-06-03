import pika

class Controller:
	def __init__(self, host='localhost'):
		connection = pika.BlockingConnection(pika.ConnectionParameters(
		host='localhost'))

		self.channel = connection.channel()

		self.channel.queue_declare(queue='keys')
		self.channel.queue_declare(queue='values')

	def on_receive_keys(self, ch, method, props, body):
		print 'received keys:' + body

		ch.basic_publish(exchange='',
							routing_key=props.reply_to,
							properties=pika.BasicProperties(correlation_id = \
													props.correlation_id),
							body='keys ok')
		ch.basic_ack(delivery_tag = method.delivery_tag)

	def on_receive_values(self, ch, method, props, body):
		print 'received values:' + body

	def start(self):
		self.channel.basic_consume(self.on_receive_keys, queue='keys')
		self.channel.basic_consume(self.on_receive_values, queue='values')

		print " [x] Awaiting for keys and values"

		self.channel.start_consuming()
