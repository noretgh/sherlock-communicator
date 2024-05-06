######################################################
############ DO NOT CHANGE THIS FILE! ################
######################################################

from datetime import datetime
import json

from pika import spec
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import BasicProperties


######################################################
################# Send Messages ######################
######################################################
def send_messages(channel: BlockingChannel,
                  exchange_name: str,
                  sender: str,
                  receiver: str) -> bool:
    message = input("Enter your message to the other team (enter 'close' to exit):")

    if message == "close":
        return False

    body = {
        "sender": sender,
        "receiver": receiver,
        "timestamp": get_current_datetime_as_string(),
        "message": message,
    }

    channel.exchange_declare(exchange=exchange_name,
                             exchange_type='direct')

    channel.basic_publish(
        exchange=exchange_name,
        routing_key=receiver,
        body=json.dumps(body))

    return True


######################################################
############### Receive Messages #####################
######################################################

def callback_messages(channel: BlockingChannel,
                      method: spec.Basic.Deliver,
                      properties: BasicProperties,
                      body: bytes) -> None:
    body_obj = json.loads(body)
    sender = body_obj["sender"]
    receiver = body_obj["receiver"]
    timestamp = datetime.strptime(body_obj["timestamp"], "%d.%m.%Y, %H:%M:%S.%f")
    delivery_duration = datetime.now() - timestamp
    message = body_obj["message"]

    print(f"Received message from {sender}, delivered to {receiver} after {delivery_duration}:\n{message}")

    channel.basic_ack(delivery_tag=method.delivery_tag)


def receive_messages(channel: BlockingChannel,
                     exchange_name: str,
                     receiver: str) -> None:
    result = channel.queue_declare(queue='',
                                   exclusive=True)
    queue_name = result.method.queue

    channel.exchange_declare(exchange=exchange_name,
                             exchange_type='direct')

    channel.queue_bind(exchange=exchange_name,
                       queue=queue_name,
                       routing_key=receiver)

    channel.basic_consume(queue=queue_name,
                          on_message_callback=callback_messages)

    print(f"Waiting for new messages at queue {result.method.queue}")

    channel.start_consuming()


def get_current_datetime_as_string() -> str:
    return datetime.now().strftime("%d.%m.%Y, %H:%M:%S.%f")[:-3]
