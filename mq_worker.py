import json

import pika
import redis
import requests

import computation


def computation_callback(ch, method, properties, body):
    id = properties.correlation_id
    input_data = int(body)
    print(f"Received request for data {input_data} with id {id}.")

    fib = computation.fibonacci(input_data)

    print(f"The {int(body)}-th fibonacci number is: {fib}")

    cache.set(id, fib)

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    conn_param = pika.ConnectionParameters("localhost")
    cache = redis.Redis(host="localhost", port=6379, decode_responses=True)

    with pika.BlockingConnection(conn_param) as connection:
        channel = connection.channel()

        channel.queue_declare("computation-request-queue")

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue="computation-request-queue", on_message_callback=computation_callback
        )
        print("[x] MQ-Worker Started...")
        channel.start_consuming()
