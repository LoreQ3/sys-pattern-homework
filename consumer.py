#!/usr/bin/env python3
import pika
import time

def callback(ch, method, properties, body):
    print(f" [x] Received: {body.decode()}")
    # Имитируем обработку сообщения
    time.sleep(2)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    # Подключаемся ко второму узлу (покажем работу с разными нодами)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5673,
                                 credentials=pika.PlainCredentials('admin', 'password'))
    )
    channel = connection.channel()
    
    channel.queue_declare(queue='hello', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='hello', on_message_callback=callback)
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
