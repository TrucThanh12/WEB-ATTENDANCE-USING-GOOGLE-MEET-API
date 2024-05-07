import pika

def public(str: str):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()

    channel.queue_declare(queue='service')

    channel.basic_publish(exchange='', routing_key='service', body=str)
    print(" [x] Sent message successful")
    connection.close()