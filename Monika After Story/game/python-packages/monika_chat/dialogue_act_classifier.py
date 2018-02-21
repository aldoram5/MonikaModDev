import csv
import os
import inspect
import utils
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

    def train(self, corpus):
        """
        train method to get the word weight per class, requires a corpus tsv file with the columns class and sentence
        :param corpus: name of the tsv file containing the classes and senteces to train on
        :return: nothing but once the training is done the classes and corpus_words are defined the model stores itself
        """
        training_data = []
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
            print(sentence)
            # tokenize and tag each sentence into words
            for word, tag in self.pos_tagger.tag(sentence):
                # ignore a some things
                # use morphy to get base form and lowercase each word
                base_word = self.morphy.morphy(word.lower(),tag)
                # have we not seen this word already?
                if base_word not in self.corpus_words:
                    self.corpus_words[base_word] = 1
                else:
                    self.corpus_words[base_word] += 1

                    # add the word to our words in class list
                self.class_words[data['class']].extend([base_word])

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
        print(self.corpus_words)
        print(self.class_words)
        # loop through our classes
        for c in self.class_words.keys():
            # calculate score of sentence for each class
            score = self.calculate_class_score(sentence, c, show_details=True)
            # keep track of highest score
            if score > high_score:
                high_class = c
                high_score = score

        return high_class, high_score

    # calculate a score for a given class taking into account word commonality
    def calculate_class_score(self,sentence, class_name, show_details=True):
        score = 0
        # pre processing our sentence
        sentence = self.pre_process_sentence(sentence)
        # tokenize and tag each sentence into words
        for word, tag in self.pos_tagger.tag(sentence):
            # use morphy to get base form and lowercase each word
            base_word = self.morphy.morphy(word.lower(), tag)
            # check to see if the stem of the word is in any of our classes
            if base_word in self.class_words[class_name]:
                # treat each word with relative weight
                score += (1.0 / self.corpus_words[base_word])

                if show_details:
                    print ("   match: %s (%s)" % (
                        base_word, 1.0 / self.corpus_words[base_word]))
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
    monika = DialogueActClassifier()
    monika.train("dialogue-act-corpus.tsv")
    try:
        s = raw_input('> ')
    except EOFError:
        continue_chat = False
    while continue_chat:
        print(s)
        c, s = monika.classify(s)
        print(c)
        print(s)
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