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
        self.current_conversation = None


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


class MonikaMemory:
    def __init__(self, load=True):
        self.temporal_memory = TemporalMemory()
        self.permanent_memory = PermanentMemory()

    def store_current_sentence_data(self,tagged_sentence):
        print (tagged_sentence)



