from pika.adapters.blocking_connection import BlockingChannel


def send_clue_to_moriarty(channel: BlockingChannel,
                          moriarty_queue: str,
                          answer_exchange: str,
                          anwer_routing_key: str) -> None:
    """
    Send two clues that are associated with each other to Moriarty.
    He will send his answer back to the exchange in the answer_exchange (type: direct) with the anwer_routing_key.

    But take care, Moriarty will neither create an Exchange nor a Queue for you!

    Moriarty expects the following format (order of the clues does not matter):
    {
        "clue1": "string"
        "clue2": "string"
        "sender_team": "string"
        "datetime_sent": "string" (dd.mm.YYYY HH:MM:SS)
        "response_exchange": "string"
        "response_receiver": "string"
    }

    Take care, if the formatting is not correct, you will not get any response from Moriarty!
    """
    raise NotImplementedError


def receive_moriarty_answers(channel: BlockingChannel,
                             answer_exchange: str,
                             anwer_routing_key: str) -> None:
    """
    Subscribe the exchange to your queue to access the answers from Moriarty.

    Moriarty sends the response in the following format:
    {
        "success": boolean,
        "message": "string"
        "next_task": "string"
    }
    """
    raise NotImplementedError
