import csv
import os
import inspect
import utils
import time
from monika_ai import MonikaAi
from pos_tagger import PerceptronTagger
from morphy import Morphy


class DialogueActClassifier:

    def __init__(self, base_dir=None):
        self.base_dir = base_dir
        if self.base_dir is None:
            self.base_dir = os.path.dirname(inspect.getfile(self.__class__))
        self.corpus_words = {}
        self.class_words = {}
        self.ngrams = 2
        self.pos_tagger = PerceptronTagger(base_dir=base_dir)
        self.morphy = Morphy(base_dir=base_dir)

    def pre_process_sentence(self, sentence):
        """
        pre_process_sentence expands contractions on a sentence and changes the symbol ? so it can be specially processed
        :param sentence: the sentence to pre-process
        :return: the sentence with the modifications
        """
        # expand the contractions
        expanded_sentence = utils.expand_contractions(sentence.lower())
        # remove punctuation
        return utils.strip_punc(expanded_sentence)

    def change_to_base(self, words):
        """
        change_to_base An auxiliary method that changes the input list of tuples words to base form if possible
        :param words: list of tuples containing word and tag
        :return: a list of words in their base form
        """
        base_words = []
        for word, tag in words:
            # use morphy to get base form and lowercase each word
            base_word = self.morphy.morphy(word, tag)
            base_words.append(base_word)
        return base_words

    def transform_ngrams(self, words):
        """
        transform_ngrams method performs a n-gram tokenization based on the self.ngrams defined, if self.ngrams is 
        equal to 1 it return the word list as is since there's nothing to do to it.
        Example of what this function does: for the word list : "hello", "there", "my", "love", it transforms it into a
        list: "hello there", "there my", "my love" for ngrams = 2
        :param words: a list of the words to tokenize
        :return: the tokenized words
        """
        return words if self.ngrams == 1 else [" ".join(words[i:i+self.ngrams]) for i in range(len(words)-self.ngrams+1)]

    def train(self, corpus):
        """
        train method to get the word weight per class, requires a corpus tsv file with the columns class and sentence
        :param corpus: name of the tsv file containing the classes and senteces to train on
        :return: nothing but once the training is done the classes and corpus_words are defined the model stores itself
        """
        with open(os.path.join(self.base_dir, corpus)) as tsvfile:
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            training_data = list(reader)

        classes = list(set([e['class'] for e in training_data]))
        for c in classes:
            # prepare a list of words within each class
            self.class_words[c] = []

        # loop through each sentence in our training data
        for data in training_data:
            # pre processing our sentence
            sentence = self.pre_process_sentence(data['sentence'])
            # tokenize and tag each sentence into words
            words = self.pos_tagger.tag(sentence)
            # use morphy to get base form and lowercase each word
            base_words = self.change_to_base(words)
            ngrams = self.transform_ngrams(base_words)
            for element in ngrams:
                # have we not seen this word combination already?
                if element not in self.corpus_words:
                    self.corpus_words[element] = 1
                else:
                    self.corpus_words[element] += 1

                    # add the word to our words in class list
                self.class_words[data['class']].extend([element])

    # return the class with highest score for sentence
    def classify(self, sentence):
        """
        classify here we actually calculate the probability of the sentence being part of some class, that's done by a
        simple naive analysis
        :param sentence: sentence to classify
        :return: the highest scoring class and the score it got, defaults to 'statement'
        """
        high_class = "statement"
        high_score = 0
        trustable = True
        # loop through our classes
        for c in self.class_words.keys():
            # calculate score of sentence for each class
            score = self.calculate_class_score(sentence, c, show_details=True)
            # keep track of highest score
            if score > high_score:
                high_class = c
                high_score = score

        return high_class, high_score, trustable

    # calculate a score for a given class taking into account word commonality
    def calculate_class_score(self,sentence, class_name, show_details=True):
        score = 0
        # pre processing our sentence
        sentence = self.pre_process_sentence(sentence)
        # tokenize and tag each sentence into words
        words = self.pos_tagger.tag(sentence)
        # use morphy to get base form and lowercase each word
        base_words = self.change_to_base(words)
        ngrams = self.transform_ngrams(base_words)
        for element in ngrams:
            # have we not seen this word combination already?
            if element in self.class_words[class_name]:
                # treat each word with relative weight
                score += (1.0 / self.corpus_words[element])
                if show_details:
                    print ("   match: %s (%s)" % (element, 1.0 / self.corpus_words[element]))
        return score


def command_interface():
    print('Dialogue act classifier interactive tester\n---------')
    print('Welcome to the Monika DACT classifier tester. ')
    print('this is for testing and debugging the classifier performance')
    print('=' * 20)
    print("Hi honey,  What's up?")
    train = True
    s = 'hello'
    continue_chat = True

    start = time.time()
    monika = DialogueActClassifier()
    end = time.time()
    print("training finished in:")
    print(end - start)
    monika.train("dialogue-act-corpus.tsv")
    #monika.train("dialogue-act-corpus-mini.tsv")
    try:
        s = raw_input('> ')
    except EOFError:
        continue_chat = False
    while continue_chat:
        print(s)
        c, s, t = monika.classify(s)
        print(c)
        print(s)
        print(t)
        if True:
            try:
                s = raw_input('> ')
            except EOFError:
                s = 'quit'
            if s == 'quit':
                return


if __name__ == "__main__":
    command_interface()

# command_interface()