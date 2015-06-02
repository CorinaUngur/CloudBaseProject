import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="hello")

channel.basic_publish(exchange='', routing_key='hello', body='Hey there')
print '[x] Sent "hey there"'

channel.queue_declare(queue="listener1")

channel.basic_publish(exchange='', routing_key='listener1', body='Hey listener1, nice to meet you')
print '[x] Sent message for listener1'


channel.queue_declare(queue="listener2")

channel.basic_publish(exchange='', routing_key='listener2', body='Hey listener2, are you ready?')
print '[x] Sent message for listener2'




connection.close()