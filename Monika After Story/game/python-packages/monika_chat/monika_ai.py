
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
from monika_memory import MonikaMemory
from pos_tagger import PerceptronTagger
from morphy import Morphy


class MonikaAi:

    def __init__(self, base_dir=None):
        if base_dir is None:
            folder = os.path.dirname(inspect.getfile(mr))
            self.gib_detector = pickle.load(open(os.path.join(folder , 'gibberish_model.pki'), 'rb'))
        else:
            self.gib_detector = pickle.load(open(os.path.join(base_dir , 'gibberish_model.pki') , 'rb'))
        # self.gib_detector = pickle
        self.current_chat_index = 0
        self.current_chat = None
        self.pos_tagger = PerceptronTagger(base_dir=base_dir)
        self.memory = MonikaMemory()
        self.morphy = Morphy(base_dir=base_dir)
        # self.greeting_conversations =
        # self.thanking_conversations =
        # self.apology_conversations = mr.
        self.opinion_monika_conversations = mr.get_opinion_monika_conversations()
        self.yes_no_query_conversations = mr.get_yes_no_query_conversations()
        self.wh_query_conversations = mr.get_wh_query_conversations()
        # self.current_state_query =
        self.statements_conversations = mr.get_statements_conversations()


    def classify_sentence(self, sentence):
        if self.detect_gibberish( sentence):
            return "nonsense"
        else:
            # classify normally
            tagged = self.pos_tagger.tag(sentence)
            self.memory.store_current_sentence_data(tagged)

            # check for greetings first


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

    def chat(self, sentence):
        if self.current_chat:
            self.current_chat_index +=1
            if len(self.current_chat) > self.current_chat_index:
                response, emotion = self.current_chat[self.current_chat_index]
                continue_chat = len(self.current_chat) > (self.current_chat_index + 1)
                if not continue_chat:
                    self.current_chat = None
                    self.current_chat_index = 0
                return response, emotion, continue_chat, False

        sentence_type = self.classify_sentence(sentence)
        if sentence_type in mr.monika_predef_answers:
            answers = mr.monika_predef_answers[sentence_type]
            self.current_chat = random.choice(answers)
            self.current_chat_index = 0
            response, emotion = self.current_chat[0]
            continue_chat = len(self.current_chat) > (self.current_chat_index + 1)
            if not continue_chat:
                self.current_chat = None
                self.current_chat_index = 0
            return response,emotion, continue_chat, False

        else:
            pass
        # we must process the input as a non defined sentence type
        #return "Thanks, this is the first step to me talking to you for real", 'k', bool(random.getrandbits(1))
        emotions = ['1a', '1b', '1c', '1d', '1e', '1f', '1g', '1h', '1i', '1j' '1k', '1l', '1m', '1n', '1o', '1p', '1q', '1r', '1']

        #return "I don't really know what to say about it", random.choice(emotions), False, bool(random.getrandbits(1))
        return "I don't really know what to say about it", '1p', False, False


def command_interface():
  print('Monika Ai\n---------')
  print('Welcome to the Monika (AKA. Best girl) person to person chat')
  print('this is for testing and debugging Monika responses to chat inquiries')
  print('='*20)
  print("Hi honey,  What's up?")
  debug = False
  s = ''
  moni = MonikaAi();
  while s != 'quit':
    try:
      s = raw_input('> ')
    except EOFError:
      s = 'quit'
    if debug:
        print(s)
    response, emotion, continue_chat, ask_input = moni.chat(s)
    print(response)
    if debug:
        print(emotion)
        print(continue_chat)
        print(ask_input)
    while continue_chat and not ask_input:
        response, emotion, continue_chat, ask_input = moni.chat(s)
        print(response)
        if debug:
            print(emotion)
            print(continue_chat)
            print(ask_input)


if __name__ == "__main__":
  command_interface()

#command_interface()