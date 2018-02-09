#
# This python script uses parts of WordNet
# below you'll find their license
#
### WordNet
#
# License: https://wordnet.princeton.edu/wordnet/license/
#
# Required citation
# Princeton University "About WordNet." WordNet. Princeton University. 2010. <http://wordnet.princeton.edu>
#
# Changes done:
# Added some words to the Exceptions Lists since I'm not using the entire WordNet and can't check word
# authenticity, the morphy function is based on
#

import pickle
import re
import os
import inspect


class Morphy:

    def __init__(self,base_dir=None):

        if base_dir is None:
            base_dir = os.path.dirname(inspect.getfile(self.__class__))
        self.nouns = {}
        with open(os.path.join(base_dir, 'nouns.pickle'), 'rb') as handle:
            self.nouns = pickle.load(handle)
        self.adjs = {}
        with open(os.path.join(base_dir, 'adjs.pickle'), 'rb') as handle:
            self.adjs = pickle.load(handle)
        self.advs = {}
        with open(os.path.join(base_dir, 'advs.pickle'), 'rb') as handle:
            self.advs = pickle.load(handle)
        self.verbs = {}
        with open(os.path.join(base_dir, 'verbs.pickle'), 'rb') as handle:
            self.verbs = pickle.load(handle)
        self.modals = {"would": "will", "should":"shall", "ought":"must", "could":"can"}

    #
    # morphy function based on WordNet morphy function
    # https://wordnet.princeton.edu/man/morphy.7WN.html
    #

    def morphy(self,word, pos_tag=None):
        """
        morphy function transforms word into it's base form for easier processing
        :param word: word to transform 
        :param pos_tag: part of speech tag of this word, for morphy functions we 
            only deal with nouns, adjectives and verbs, for other tags we return 
            the word as is. If no tag is specified we'll check in the exceptions
            lists, if it's not in those we return the word as is since there's 
            nothing we can do to the word without more info
        :return: the word base form if possible, the word without modifications 
            otherwise
        """
        if pos_tag is not None:
            if 'JJ' in pos_tag:
                # It must be an adjective
                base = self.adjs.get(word, None)
                if base is not None:
                    return base
                # morphy transforms
                new, changes = re.subn(r'(er)\b', '', word)
                if changes > 0: return new
                new, changes = re.subn(r'(est)\b', '', word)
                if changes > 0: return new
            elif 'RB' in pos_tag:
                # It must be an adverb
                base = self.advs.get(word, None)
                if base is not None:
                    return base
                    # No rules applicable to adverbs
            elif 'NN' in pos_tag:
                # It must be an noun
                base = self.nouns.get(word, None)
                if base is not None:
                    return base
                # morphy transforms for nouns
                new, changes = re.subn(r'(ses)\b', 's', word)
                if changes > 0: return new
                new, changes = re.subn(r'(xes)\b', 'x', word)
                if changes > 0: return new
                new, changes = re.subn(r'(zes)\b', 'z', word)
                if changes > 0: return new
                new, changes = re.subn(r'(ches)\b', 'ch', word)
                if changes > 0: return new
                new, changes = re.subn(r'(shes)\b', 'sh', word)
                if changes > 0: return new
                new, changes = re.subn(r'(men)\b', 'man', word)
                if changes > 0: return new
                new, changes = re.subn(r'(ies)\b', 'y', word)
                if changes > 0: return new
                new, changes = re.subn(r'(s)\b', '', word)
                if changes > 0: return new
            elif 'VB' in pos_tag:
                # It must be an verb
                base = self.verbs.get(word, None)
                if base is not None:
                    return base
                new, changes = re.subn(r'(ies)\b', 'y', word)
                if changes > 0: return new
                new, changes = re.subn(r'(es)\b', '', word)
                if changes > 0: return new
                new, changes = re.subn(r'(s)\b', '', word)
                if changes > 0: return new
                new, changes = re.subn(r'(ing)\b', '', word)
                if changes > 0: return new
                new, changes = re.subn(r'(ed)\b', '', word)
                if changes > 0: return new
            elif 'MD' in pos_tag:
                base =  self.modals.get(word,None)
                if base is not None:
                    return base

