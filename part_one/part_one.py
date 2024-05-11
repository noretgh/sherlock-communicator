#        ______________
#       /   ,,____,,   \
#       |__| [][][] |__|
#         /  [][][]  \
#        /   [][][]   \
#       /    [][][]    \
# =====|________________|
# Subject: Did you miss me?
#
# Hello Watsons,
#
# you must have been separated while searching for Sherlock Holmes. But I don't want to be like that and I´m giving
# you an opportunity to communicate. Use it wisely!
#
# Find the correct connections between the clues in your box and the other team´s box and send them to me.
# If they are correct you will get further.
#
# You'll have to find out for yourself how to communicate with me,
# but I think the communication between your teams should help you figure it out.
#
# Best,
# Professor M.
import sys
import os

# Add the root directory to the Python path
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir)

from messages import send_messages, receive_messages, create_queue_and_binding
from moriarty import send_clue_to_moriarty, receive_moriarty_answers
from tools.rabbit_mq_tools import setup_connection_and_channel


def main() -> None:
    mq_connection, mq_channel = setup_connection_and_channel()

    moriarty_queue = "i_hear_you"  # DO NOT CHANGE: This key enables the communication with Professor Moriarty
    mq_exchange_name = "exchange_part_one"  # DO NOT CHANGE: enables the communication between both teams

    team_name = "team1"  # Change this value accordingly to your team: team1 or team2
    other_team_name = "team2"  # Change this value accordingly to the other team: team1 or team2

    answer_exchange = "answer_exchange"  # Decide in which exchange you want Moriarty to answer in
    answer_routing_key = "answers"  # Decide which routing key you want Moriarty to use for the answers

    try:
        while True:
            print_menu(team_name)
            user_input = input("Enter your choice:")

            if user_input == "1":
                # This function is already prepared and ready to use
                while send_messages(channel=mq_channel,
                                    exchange_name=mq_exchange_name,
                                    sender=team_name,
                                    receiver=other_team_name):
                    print("Message sent to: ", other_team_name)

            elif user_input == "2":
                # This function is already prepared and ready to use
                receive_messages(channel=mq_channel,
                                 exchange_name=mq_exchange_name,
                                 receiver=team_name)

            elif user_input == "3":
                # This function needs to be implemented by you
                send_clue_to_moriarty(channel=mq_channel,
                                      moriarty_queue=moriarty_queue,
                                      answer_exchange=answer_exchange,
                                      anwer_routing_key=answer_routing_key)

            elif user_input == "4":
                # This function needs to be implemented by you
                receive_moriarty_answers(channel=mq_channel,
                                         answer_exchange=answer_exchange,
                                         anwer_routing_key=answer_routing_key)
            elif user_input.lower() == "exit":
                break
            else:
                print("Invalid choice. Please try again")
    finally:
        mq_connection.close()

def print_menu(team_name):
    print(
        f"WELCOME {team_name}\n"
        "1 - Send Message to the other team\n"
        "2 - Receive Message from the other team\n"
        "3 - Send Clues to Moriarty\n"
        "4 - Listen for Moriarty´s answer\n"
        "Type 'exit' to quit"
    )


if __name__ == "__main__":
    main()
