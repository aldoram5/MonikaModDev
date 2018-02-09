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
from operator import itemgetter
from pos_tagger import PerceptronTagger
from morphy import Morphy

GREETING = "greeting"

STATEMENT = "statement"

OPINION = "opinion"

WH_QUESTION = "wh-question"

YN_QUESTION = "yn-question"

NONSENSE = "nonsense"

CURRENT_STATE_QUESTION = "current_state_question"


class MonikaAi:

    def __init__(self, base_dir=None):
        if base_dir is None:
            folder = os.path.dirname(inspect.getfile(mr))
            self.gib_detector = pickle.load(open(os.path.join(folder, 'gibberish_model.pki'), 'rb'))
        else:
            self.gib_detector = pickle.load(open(os.path.join(base_dir, 'gibberish_model.pki'), 'rb'))
        self.current_chat_index = 0
        self.current_chat = None
        self.next_chat_node = None
        self.current_chat_node = None
        self.pos_tagger = PerceptronTagger(base_dir=base_dir)
        self.memory = MonikaMemory()
        self.morphy = Morphy(base_dir=base_dir)
        self.conversations = {OPINION: mr.get_opinion_monika_conversations(base_dir),
                              YN_QUESTION: mr.get_yes_no_query_conversations(base_dir),
                              WH_QUESTION: mr.get_wh_query_conversations(base_dir),
                              STATEMENT: mr.get_statements_conversations(base_dir)}
        self.default_chat = mr.get_default_chat(base_dir)[0]

    def classify_sentence(self, sentence):
        """
        The classify_sentence method, it determines which dialogue of act class makes more
        sense for the given sentence. The possible constants this can return are STATEMENT,
        OPINION, WH_QUESTION, YN_QUESTION, NONSENSE, CURRENT_STATE_QUESTION, GREETING and
        STATEMENT
        :param sentence: the sentence to classify
        :return: one of the mentioned constants
        """
        if self.detect_gibberish(sentence.lower()):
            return NONSENSE
        # check for current_state_query first
        expanded_sentence = utils.expand_contractions(sentence)
        clean_sentence = utils.strip_punc(expanded_sentence, True)
        clean_sentence_lower = clean_sentence.lower()
        if clean_sentence_lower in mwl.how_are_you_variants:
            return CURRENT_STATE_QUESTION
        # check for greetings
        if re.search(r"\b(hi|hello|howdy|hiya)\b", clean_sentence_lower) or \
                re.search(r"\s{0,1}\bgood\b\s{0,1}(morning|afternoon|day|evening)", clean_sentence_lower):
            return GREETING
        tagged = self.pos_tagger.tag(expanded_sentence)
        base_forms = []
        for word, tag in tagged:
            base_word = self.morphy.morphy(word, tag)
            base_tag = tag
            if 'VB' in base_tag: base_tag = 'VB'
            base_forms.append((word if base_word is None else base_word, base_tag))
        self.memory.store_current_sentence_data(base_forms)
        if '?' in sentence:
            if [(word, tag) for (word, tag) in base_forms if tag in mwl.wh_question_tags]:
                return WH_QUESTION
            elif [(word, tag) for (word, tag) in base_forms if 'MD' in tag]:
                return YN_QUESTION
            elif [(word, tag) for (word, tag) in base_forms if word.lower() in mwl.yn_verbs]:
                return YN_QUESTION
        else:
            if "monika" in clean_sentence_lower:
                return OPINION
            else:
                state_about_her = False
                player_verb = False
                player_verb_her = False
                for base_word, tag in base_forms:
                    word = base_word.lower()
                    if player_verb:
                        if "VB" == tag:
                            player_verb_her = True
                        else:
                            player_verb = False
                    if state_about_her:
                        if "be" == word:
                            return OPINION
                    if "i" == word or "me" == word:
                        player_verb = True
                    if "you" == word:
                        state_about_her = True
                        if player_verb_her:
                            return OPINION
                    else:
                        state_about_her = False
        return STATEMENT

    def detect_gibberish(self, text):
        """
        The detect_gibberish method determines whether the text makes sense or not
        :param text: text to verify
        :return: a bool indicating True if the text doesn't make sense
        """
        clean = utils.strip_punc(text, True)
        if len(clean) < 4:
            if clean.lower() in mwl.short_valid_messages:
                return False
            else:
                return True
        else:
            model_mat = self.gib_detector['mat']
            threshold = self.gib_detector['thresh']
            return utils.avg_transition_prob(clean.lower(), model_mat) <= threshold


    def start_chat(self, sentence):
        """
        The start_chat method classifies the given sentence in one of the known
        Dialogue of Act types defined for Monika and then chooses the best chat
        match for that given sentence
        :param sentence: The sentence which is getting classified and used to determine
            which chat she should start
        :return: Nothing
        """
        sentence_type = self.classify_sentence(sentence)
        print(sentence_type)
        if sentence_type in mr.monika_predef_answers:
            answers = mr.monika_predef_answers[sentence_type]
            self.current_chat = random.choice(answers)
            self.current_chat_index = 0

        else:
            if sentence_type == CURRENT_STATE_QUESTION:
                self.current_chat = mr.get_answer_for_current_state_query()
                self.next_chat_node = self.current_chat.next_node
            else:
                conversations = self.conversations[sentence_type]
                possible_chats = []
                for chat in conversations:
                    matches, percentage = utils.check_conversation_matching(chat, self.memory.temporal_memory.verb,
                                                                            self.memory.temporal_memory.adjective,
                                                                            self.memory.temporal_memory.subject,
                                                                            self.memory.temporal_memory.noun)
                    if matches:
                        possible_chats.append((chat, percentage))
                if possible_chats:
                    possible_chats.sort(key=itemgetter(1), reverse=True)
                    self.current_chat, percentage = possible_chats[0]
                    self.next_chat_node = self.current_chat.next_node
                else:
                    self.current_chat = self.default_chat
                    self.next_chat_node = self.current_chat.next_node

    def execute_action(self, action, entered_input=None):
        if not isinstance(action, Action):
            return
        elif action.type == "store":
            self.memory.store_unclassified_data(action.key, action.value)

    def reset_conversation(self):
        """
        The reset_conversation method it resets Monika's current chat variables,
        so she can start a new conversation
        :return: nothing
        """
        self.current_chat_index = 0
        self.current_chat = None
        self.next_chat_node = None
        self.current_chat_node = None

    def chat(self, entered_input=None):
        """
        The chat method, this method is the one that return to renpy the tuple of values
        that it requires for Monika to speak and ask for player input, either as a
        text input or a menu of options
        :param entered_input: The text, if any, entered by the text input interface on
            renpy side
        :return: this function return a multiple values in this order:
            response -  a string with the contents of what Monika thinks she should answer
            emotion - a simple string with format '1a', this is based on the already working system
            continue_chat - a boolean flag to let renpy know if the chat is still going on or if it can
                go back to looper_30 or whatever state it was before chatting
            need_player_input - a boolean flag to indicate that she needs the player text input
                for something
            menu - a list of tuples containing the text for that menu element and the id of the node that
                will be the next if the player choose that menu option
        """
        # define default return values
        response = ""
        emotion = "1a"
        continue_chat = False
        need_player_input = False
        menu = None

        # check conversation active type

        if self.current_chat is not None:
            if isinstance(self.current_chat, list):
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
                        # continue_chat = True if menu else False
                    else:
                        # or true since next node exist
                        continue_chat = True

        return response, emotion, continue_chat, need_player_input, menu


def command_interface():
    print('Monika Ai\n---------')
    print('Welcome to the Monika (AKA. Best girl) person to person chat')
    print('this is for testing and debugging Monika responses to chat inquiries')
    print('=' * 20)
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

# command_interface()
