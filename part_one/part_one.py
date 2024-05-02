#        ______________
#       /   ,,____,,   \
#       |__| [][][] |__|
#         /  [][][]  \
#        /   [][][]   \
#       /    [][][]    \
# =====|________________|
#
# Did you miss me?
#
#
# Best,
# Professor M.
from messages import send_messages, receive_messages
from moriarty import send_clue_to_moriarty, receive_moriarty_answers
from tools.rabbit_mq_tools import setup_connection_and_channel


def main() -> None:
    mq_connection, mq_channel = setup_connection_and_channel()

    moriarty_queue = "i_hear_you"  # Keep this value unchanged, to enable communication with Professor Moriarty
    mq_exchange_name = "exchange_part_one"  # Keep this value unchanged, to enable communication between both teams

    team_name = "team1"  # Change this value accordingly to your team: team1 or team2
    other_team_name = "team1"  # Change this value accordingly to the other team: team1 or team2

    answer_queue = "answer_queue"  # Decide in which queue you want Moriarty to answer in
    answer_routing_key = "answers"  # Decide which routing key you want Moriarty to use for the answers

    try:
        while True:
            user_input = input(
                "1 - Send Message to the other team\n2 - Receive Message from the other team\n"
                "3 - Send Clue\n4 - Listen for Moriarty\nEnter your choice:")

            if user_input == "1":
                while send_messages(channel=mq_channel,
                                    exchange_name=mq_exchange_name,
                                    sender=team_name,
                                    receiver=other_team_name):
                    pass

            elif user_input == "2":
                receive_messages(channel=mq_channel,
                                 exchange_name=mq_exchange_name,
                                 receiver=team_name)

            elif user_input == "3":
                send_clue_to_moriarty(channel=mq_channel,
                                      moriarty_queue=moriarty_queue,
                                      answer_queue=answer_queue,
                                      anwer_routing_key=answer_routing_key)

            elif user_input == "4":
                receive_moriarty_answers(channel=mq_channel,
                                         answer_queue=answer_queue,
                                         anwer_routing_key=answer_routing_key)
            else:
                break
    finally:
        mq_connection.close()


if __name__ == "__main__":
    main()
