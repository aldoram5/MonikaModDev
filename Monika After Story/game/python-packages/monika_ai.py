
import string
import re
import random

class monika_ai:
    def __init__(self):
        self.value = "some random test"
        self.times_before_quit = 2
    
    def reset(self):
        self.times_before_quit = 2
        
    def chat(self, input):
        self.times_before_quit -=1
        #return "Thanks, this is the first step to me talking to you for real", 'k', bool(random.getrandbits(1))
        emotions = ['1a', '1b', '1c', '1d', '1e', '1f', '1g', '1h', '1i', '1j' '1k', '1l', '1m', '1n', '1o', '1p', '1q', '1r', '1']
        
        return "This is the first step to me talking to you for real", random.choice(emotions), bool(self.times_before_quit>0), bool(random.getrandbits(1))
        
        