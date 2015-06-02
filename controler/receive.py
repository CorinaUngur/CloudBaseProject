import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="hello")

print 'Waiting...'

def callback(ch, method, properties, body):
	print 'received: ' + body

channel.basic_qos(prefetch_count=1)

channel.basic_consume(callback, queue='hello', no_ack=True)



channel.queue_declare(queue="listener1")

print 'listener 1 channel declared queue'

def callback2(ch, method, properties, body):
	print 'listener1 received: ' + body

channel.basic_consume(callback2, queue='listener1', no_ack=True)



print 'listener 2 channel declared queue'

def callback3(ch, method, properties, body):
	print 'listener2 received: ' + body

channel.basic_consume(callback3, queue='listener2', no_ack=True)



channel.start_consuming()