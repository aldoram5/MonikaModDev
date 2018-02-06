
import inspect
import math
import monika_responses as mr
import monika_words_lists as mwl
import os
import pickle
import re
import random
import string
import utils
from conversation import Conversation, Node, Action
from monika_memory import MonikaMemory
from pos_tagger import PerceptronTagger
from morphy import Morphy


class MonikaAi:

    def __init__(self, base_dir=None):
        if base_dir is None:
            folder = os.path.dirname(inspect.getfile(mr))
            self.gib_detector = pickle.load(open(os.path.join(folder, 'gibberish_model.pki'), 'rb'))
        else:
            self.gib_detector = pickle.load(open(os.path.join(base_dir, 'gibberish_model.pki') , 'rb'))
        self.current_chat_index = 0
        self.current_chat = None
        self.next_chat_node = None
        self.current_chat_node = None
        self.pos_tagger = PerceptronTagger(base_dir=base_dir)
        self.memory = MonikaMemory()
        self.morphy = Morphy(base_dir=base_dir)
        # self.greeting_conversations =
        # self.thanking_conversations =
        # self.apology_conversations = mr.
        self.opinion_monika_conversations = mr.get_opinion_monika_conversations(base_dir)
        print(self.opinion_monika_conversations)
        self.yes_no_query_conversations = mr.get_yes_no_query_conversations(base_dir)
        self.wh_query_conversations = mr.get_wh_query_conversations(base_dir)
        # self.current_state_query =
        self.statements_conversations = mr.get_statements_conversations(base_dir)

    def classify_sentence(self, sentence):
        if self.detect_gibberish(sentence):
            return "nonsense"
        else:
            # check for current_state_query first
            clean_sentence = utils.strip_punc(sentence, True)
            expanded_sentence = utils.expand_contractions(clean_sentence)
            clean_sentence_lower = expanded_sentence.lower()
            if clean_sentence_lower in mwl.how_are_you_variants:
                return "current_state_question"
            # classify normally
            tagged = self.pos_tagger.tag(sentence)
            self.memory.store_current_sentence_data(tagged)
            return "greeting"

    def detect_gibberish(self, text):
        clean = utils.strip_punc(text,True)
        #clean = text.translate(None, string.punctuation)
        if len(clean) < 4:
            if clean.lower() in mwl.short_valid_messages:
                return False
            else:
                return True
        else:
            model_mat = self.gib_detector['mat']
            threshold = self.gib_detector['thresh']
            return utils.avg_transition_prob(clean.lower(), model_mat) <= threshold

    # chat function
    # this is where the "magic" happens, monika keeps track of current conversation
    # so if she needs to say something else she remembers and keeps talking
    # if not she will process player input so she 'understands' what the player 'said'
    # and respond accordingly
    # this function return a multiple values in this order:
    # response -  a string with the contents of what Monika thinks she should answer
    # emotion - a simple string with format '1a', this is based on the already working system
    # continue_chat - a boolean flag to let renpy know if the chat is still going on or if it can go back
    #                 to looper_30 or whatever state it was before chatting
    # expecting_input - another boolean flag to let renpy know if we expect a response
    #                   from the player or not

    def start_chat(self, sentence):

        sentence_type = self.classify_sentence(sentence)
        if sentence_type in mr.monika_predef_answers:
            answers = mr.monika_predef_answers[sentence_type]
            self.current_chat = random.choice(answers)
            self.current_chat_index = 0

        else:
            if sentence_type == "current_state_question":
                self.current_chat = mr.get_answer_for_current_state_query()
                self.next_chat_node = self.current_chat.next_node

        # we must process the input as a non defined sentence type
        #return "Thanks, this is the first step to me talking to you for real", 'k', bool(random.getrandbits(1))
        #emotions = ['1a', '1b', '1c', '1d', '1e', '1f', '1g', '1h', '1i', '1j' '1k', '1l', '1m', '1n', '1o', '1p', '1q', '1r', '1']

        #return "I don't really know what to say about it", random.choice(emotions), False, bool(random.getrandbits(1))
        #return "I don't really know what to say about it", '1p', False, False, None

    def execute_action(self, action, entered_input=None):
        if not isinstance(action, Action):
            return
        if action.type == "check":
            pass
        elif action.type == "store":
            pass

    def reset_conversation(self):
        self.current_chat_index = 0
        self.current_chat = None
        self.next_chat_node = None
        self.current_chat_node = None

    def chat(self, entered_input=None):
        # define default return values
        response = ""
        emotion = "1a"
        continue_chat = False
        need_player_input = False
        menu = None

        # check conversation active type

        if self.current_chat is not None:
            if isinstance(self.current_chat,list):
                # since it's predefined we only need the text and reaction
                if len(self.current_chat) > self.current_chat_index:
                    # we set the values we'll return
                    response, emotion = self.current_chat[self.current_chat_index]
                    continue_chat = len(self.current_chat) > (self.current_chat_index + 1)
                    # we keep track of which value we are in
                    self.current_chat_index += 1
                    if not continue_chat:
                        self.reset_conversation()
            elif isinstance(self.current_chat, Conversation):
                # if we have a node active we check for it's final action
                if self.current_chat_node is not None and self.current_chat_node.final_action is not None:
                    # to execute that action
                    self.execute_action(self.current_chat_node.final_action, entered_input)

                # retrieve current conversation next node
                self.current_chat_node = self.current_chat.nodes.get(self.next_chat_node, None)
                # check that we have a valid node
                if self.current_chat_node is not None and isinstance(self.current_chat_node, Node):
                    # check for initial action
                    if self.current_chat_node is not None and self.current_chat_node.initial_action is not None:
                        # to execute that action
                        self.execute_action(self.current_chat_node.initial_action, entered_input)
                    # check node values and set the values we'll return
                    response = self.current_chat_node.display_text
                    emotion = self.current_chat_node.reaction
                    need_player_input = True if self.current_chat_node.input_type == "text" else False
                    menu = self.current_chat_node.options
                    # determine next node
                    self.next_chat_node = self.current_chat_node.next_node
                    # if we don't have a next node
                    if self.next_chat_node is None and not menu:
                        # set to none active conversations
                        self.reset_conversation()
                        # we return continue chat as false
                        continue_chat = False
                        #continue_chat = True if menu else False
                    else:
                        # or true since next node exist
                        continue_chat = True

        return response, emotion, continue_chat, need_player_input, menu


def command_interface():
    print('Monika Ai\n---------')
    print('Welcome to the Monika (AKA. Best girl) person to person chat')
    print('this is for testing and debugging Monika responses to chat inquiries')
    print('='*20)
    print("Hi honey,  What's up?")
    debug = True
    s = 'hello'
    continue_chat = True
    monika = MonikaAi()
    try:
        s = raw_input('> ')
    except EOFError:
        continue_chat = False
    monika.start_chat(s)
    while continue_chat:
        if debug:
            print(s)
        response, emotion, continue_chat, ask_input, menu = monika.chat(s)
        print(response)
        if debug:
            print(emotion)
            print(continue_chat)
            print(ask_input)
            print(menu)
        if ask_input:
            try:
                s = raw_input('> ')
            except EOFError:
                s = 'quit'
            if s == 'quit':
                return


if __name__ == "__main__":
    command_interface()

#command_interface()