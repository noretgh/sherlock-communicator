from pika.adapters.blocking_connection import BlockingChannel


def send_clue_to_moriarty(channel: BlockingChannel,
                          moriarty_queue: str,
                          answer_queue: str,
                          anwer_routing_key: str) -> None:
    pass


def receive_moriarty_answers(channel: BlockingChannel,
                             answer_queue: str,
                             anwer_routing_key: str) -> None:
    pass
