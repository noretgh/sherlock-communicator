from typing import Tuple

import os
import pika
import ssl

from pika.adapters.blocking_connection import BlockingConnection, BlockingChannel


def setup_connection_and_channel() -> Tuple[BlockingConnection, BlockingChannel]:
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')

    rabbitmq_user = os.getenv("RABBITMQ_USER")
    rabbitmq_password = os.getenv("RABBITMQ_PWD")
    rabbitmq_broker_id = os.getenv("BROKER_ID")

    region = "eu-west-1"

    url = f"amqps://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_broker_id}.mq.{region}.amazonaws.com:5671"

    parameters = pika.URLParameters(url)
    parameters.ssl_options = pika.SSLOptions(context=ssl_context)

    connection = pika.BlockingConnection(parameters)

    return connection, connection.channel()
