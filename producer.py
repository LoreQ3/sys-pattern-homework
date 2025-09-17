#!/usr/bin/env python3
import pika
import time

def main():
    # Подключаемся к первому узлу
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672,
                                 credentials=pika.PlainCredentials('admin', 'password'))
    )
    channel = connection.channel()
    
    # Создаем очередь
    channel.queue_declare(queue='hello', durable=True)
    
    # Отправляем сообщения
    for i in range(10):
        message = f'Сообщение №{i} - {time.strftime("%H:%M:%S")}'
        channel.basic_publish(
            exchange='',
            routing_key='hello',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # persistent message
            ))
        print(f" [x] Sent: {message}")
        time.sleep(1)
    
    connection.close()

if __name__ == '__main__':
    main()
