import pika


class Agent:
	def __init__(self, hos="localhost"):
		self.host = hos
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
		self.channel = self.connection.channel()

	def send_message(self, que, message):
		self.channel.queue_declare(queue=que)
		self.channel.basic_publish(exchange='', routing_key=que, body=message)
		print '# Sent to '+que+': '+message

	def close_connection(self):
		self.connection.close()

