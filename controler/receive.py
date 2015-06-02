import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="hello")

print 'Waiting...'

def callback(ch, method, properties, body):
	print 'received: ' + body

channel.basic_consume(callback, queue='hello', no_ack=True)

channel.start_consuming()