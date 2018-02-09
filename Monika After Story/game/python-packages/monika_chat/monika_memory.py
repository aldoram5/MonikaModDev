import pickle
from datetime import date

# https://simple.wikipedia.org/wiki/List_of_emotions


class TemporalMemory:
    def __init__(self):
        self.fear = 0
        self.anger = 0
        self.sadness = 0
        self.joy = 10
        self.disgust = 0
        self.surprise = 0
        self.trust = 10
        self.anticipation = 0
        self.today_important_date = False
        self.subject = ""
        self.verb = ""
        self.adjective = ""
        self.noun = ""


class PermanentMemory:
    def __init__(self):
        self.important_dates = {"birthday": date(2017, 9, 22)}
        self.player_data = {"name": "", "birthday": None}
        self.player_interests = {}
        self.player_likes = {}
        self.player_dislikes = {}
        self.monika_preferences = {}
        self.monika_interests = {}
        self.monika_likes = {}
        self.monika_dislikes = {}
        self.monika_stored_info = {}


class MonikaMemory:
    def __init__(self, base_dir=None, load=True):
        self.temporal_memory = TemporalMemory()
        self.permanent_memory = PermanentMemory()

    def store_current_sentence_data(self,tagged_sentence):
        self.temporal_memory.adjective = ""
        self.temporal_memory.noun = ""
        self.temporal_memory.subject = ""
        self.temporal_memory.verb = ""
        pos = 0
        for (word, tag) in tagged_sentence:
            print(word)
            print(tag)
            if "VB" in tag and not self.temporal_memory.verb:
                self.temporal_memory.verb = word
            if "W" in tag and pos == 0:
                self.temporal_memory.subject
            if "PR" in tag and pos == 0:
                self.temporal_memory.subject
            if "NN" in tag and pos == 0:
                self.temporal_memory.subject
            if "NN" in tag and pos > 0 and not self.temporal_memory.noun:
                self.temporal_memory.noun = word
            if "FW" in tag and pos > 0 and not self.temporal_memory.noun:
                self.temporal_memory.noun = word
            if "JJ" in tag and not self.temporal_memory.adjective:
                self.temporal_memory.adjective = word
            pos+=1


    def store_unclassified_data(self, key, value):
        self.permanent_memory.monika_stored_info[key] = value



