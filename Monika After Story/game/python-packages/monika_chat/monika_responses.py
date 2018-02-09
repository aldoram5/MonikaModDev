import os
import glob
import inspect
import utils
from conversation import Action, Conversation, Node

NO_ANSWER = "no-answer"

STATEMENTS = "statements"

WH_QUESTIONS = "wh-questions"

YN_QUESTIONS = "yn-questions"

OPINIONS_RELATIVE_PATH = "opinions"

# Monika's predefined answers when you tell nonsense to her
answers_for_gibberish =\
    [[("Why would you say that to me?", "1c",),("That didn't make any sense.", "1q")],
                        [("What was that?", "1m"),("Stop teasing me like that.", "1n")],
                        [("Sorry I couldn't understand that.", "1o")],
                        [("bhcsjnjdnjshn", "1a"), ("nuybyubefy ujjdujqwer", "1r"),
                         ("asdadsf ", "1q"),("I can say nonsense too, you know?", "1a"),
                         ("Ahaha~", "1k")
                         ]]

answers_for_greetings =\
    [[("Hello again, sweetheart!", "1k",),
      ("It's kind of embarrassing to say out loud, isn't it?","1l"),
      ("Still, I think it's okay to be embarrassed every now and then.","3b")],
                        [("Hi! Welcome back.", "1b"), ("I'm so glad that you're able to spend some time with me.", "1k")],
                        [("Oh, hello there!", "1j")],
                        [("Hi honey!", "1j")]]

answers_for_current_state_query =\
    [[("I'm perfectly fine now that you're here", "1b",),
      ("It's kind of embarrassing to say out loud, isn't it?","1l"),
      ("Still, I think it's okay to be embarrassed every now and then.","3b")],
                        [("Hi! Welcome back.", "1b"), ("I'm so glad that you're able to spend some time with me.", "1k")],
                        [("Oh, hello there!", "1j")],
                        [("Hi honey!", "1j")]]

monika_predef_answers = {"nonsense": answers_for_gibberish, "greeting": answers_for_greetings}


def get_answer_for_current_state_query():
    conversation = Conversation()
    node1 = Node()
    node1.reaction = "1b"
    node1.display_text = "I'm perfectly fine now that you're here."
    node1.id = "n1"
    node2 = Node()
    node2.reaction = "1a"
    node2.display_text = "What about you?"
    node2.id = "n2"
    node3 = Node()
    node3.id = "n3"
    node3.add_option("I'm fine thanks", "n4")
    node3.add_option("Not so well", "n5")
    node3.set_input_multi()
    node3.display_text = ""
    node4 = Node()
    node4.id = "n4"
    node4.display_text = "I'm happy to hear that."
    node4.reaction = "1a"
    node5 = Node()
    node5.id = "n5"
    node5.display_text = "I'm sorry to hear that."
    node5.reaction = "1f"
    node6 = Node()
    node6.id = "n6"
    node6.reaction = "4e"
    node6.display_text = "But don't worry."
    node7 = Node()
    node7.id = "n7"
    node7.reaction = "1j"
    node7.display_text = "I'm here for you now~"
    node1.next_node = node2.id
    node2.next_node = node3.id
    node5.next_node = node6.id
    node6.next_node = node7.id
    conversation.add_node(node1)
    conversation.add_node(node2)
    conversation.add_node(node3)
    conversation.add_node(node4)
    conversation.add_node(node5)
    conversation.add_node(node6)
    conversation.add_node(node7)
    conversation.next_node = node1.id
    return conversation


def get_opinion_monika_conversations(base_dir=None):
    return get_conversations_in_folder(base_dir, OPINIONS_RELATIVE_PATH)


def get_yes_no_query_conversations(base_dir=None):
    return get_conversations_in_folder(base_dir, YN_QUESTIONS)


def get_wh_query_conversations(base_dir=None):
    return get_conversations_in_folder(base_dir, WH_QUESTIONS)


def get_statements_conversations(base_dir=None):
    return get_conversations_in_folder(base_dir, STATEMENTS)


def get_conversations_in_folder(base_dir=None,folder=None):
    if base_dir is None:
        base_dir = os.path.dirname(inspect.getfile(utils))
    folder = os.path.join(base_dir, folder)
    conversations = []
    for file_name in glob.glob(os.path.join(folder, '*.json')):
        with open(file_name, 'r') as json_data:
            conversation = Conversation()
            conversation.load_from_json(json_data)
            conversations.append(conversation)
    return conversations

def get_default_chat(base_dir=None):
    return get_conversations_in_folder(base_dir, NO_ANSWER)