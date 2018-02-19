#
# This python script uses parts of Gibberish Detector https://github.com/rrenaud/Gibberish-Detector
# below you'll find their license
#
### Gibberish Detector
#
# Base code from https://github.com/rrenaud/Gibberish-Detector
#
# Licensed under MIT License https://github.com/rrenaud/Gibberish-Detector/blob/master/LICENSE
#
# Copyright (c) 2015 Rob Renaud
#
# Modified/extracted for easy usage with renpy
#


import math
import string
import re
import datetime
from difflib import SequenceMatcher


contractions_dict = {
  "ain't": "am not",
  "aren't": "are not",
  "can't": "cannot",
  "can't've": "cannot have",
  "'cause": "because",
  "could've": "could have",
  "couldn't": "could not",
  "didn't": "did not",
  "doesn't": "does not",
  "don't": "do not",
  "hadn't": "had not",
  "hasn't": "has not",
  "haven't": "have not",
  "he'd": "he would",
  "he'll": "he will",
  "he's": "he is",
  "how'd": "how did",
  "how'll": "how will",
  "how's": "how is",
  "I'd": "I would",
  "I'd've": "I would have",
  "I'll": "I will",
  "I'm": "I am",
  "I've": "I have",
  "isn't": "is not",
  "it'd": "it had",
  "it'll": "it will",
  "it's": "it is",
  "let's": "let us",
  "ma'am": "madam",
  "mayn't": "may not",
  "might've": "might have",
  "must've": "must have",
  "mustn't": "must not",
  "mustn't've": "must not have",
  "needn't": "need not",
  "needn't've": "need not have",
  "oughtn't": "ought not",
  "oughtn't've": "ought not have",
  "she'd": "she would",
  "she'd've": "she would have",
  "she'll": "she will",
  "she'll've": "she will have",
  "she's": "she is",
  "shouldn't": "should not",
  "so've": "so have",
  "so's": "so is",
  "that'd": "that would",
  "that's": "that is",
  "there'd": "there had",
  "there's": "there is",
  "they'd": "they would",
  "they'll": "they will",
  "they're": "they are",
  "they've": "they have",
  "to've": "to have",
  "wasn't": "was not",
  "we'd": "we had",
  "we'll": "we will",
  "we're": "we are",
  "we've": "we have",
  "weren't": "were not",
  "what'll": "what will",
  "what're": "what are",
  "what's": "what is",
  "what've": "what have",
  "when's": "when is",
  "when've": "when have",
  "where'd": "where did",
  "where's": "where is",
  "where've": "where have",
  "who'll": "who will",
  "who's": "who is",
  "who've": "who have",
  "why's": "why is",
  "why've": "why have",
  "will've": "will have",
  "won't": "will not",
  "would've": "would have",
  "wouldn't": "would not",
  "you'll": "you will",
  "you're": "you are",
  "you've": "you have"
}

contractions_regex = re.compile(r'('+'|'.join(contractions_dict.keys())+')')

PUNCTUATION_REGEX = re.compile('[{0}]'.format(re.escape(string.punctuation)))

accepted_chars = 'abcdefghijklmnopqrstuvwxyz '

pos = dict([(char, idx) for idx, char in enumerate(accepted_chars)])


def unique_elements(array):
    unique_ordered = []
    unique = set()
    for element in array:
        if element in unique:
            continue
        unique.add(element)
        unique_ordered.append(element)
    return unique_ordered


def contractions_replace(match):
    return contractions_dict[match.group(0)]


def expand_contractions(text, regex=contractions_regex):
    return regex.sub(contractions_replace, text.lower())


def strip_punc(s, all=False):
    """Removes punctuation from a string.
    :param s: The string.
    :param all: Remove all punctuation. If False, only removes punctuation from
        the ends of the string.
    """
    if all:
        return PUNCTUATION_REGEX.sub('', s.strip())
    else:
        return s.strip().strip(string.punctuation)


def calculate_string_distance(first, final):
    return SequenceMatcher(None, first.lower(), final.lower()).ratio()


def check_conversation_matching(conversation, verb, adjective, subject, noun):
    matches = False
    averaged_score = 0
    scores = []
    if conversation.trigger_verb and verb:
        score = calculate_string_distance(conversation.trigger_verb, verb)
        averaged_score += score
        scores.append(score)
        if score > 0.7:
            matches = True

    if conversation.trigger_adj and adjective:
        score = calculate_string_distance(conversation.trigger_adj, adjective)
        averaged_score += score
        scores.append(score)
        if score > 0.7:
            matches = True

    if conversation.trigger_subject and subject:
        score = calculate_string_distance(conversation.trigger_subject, subject)
        averaged_score += score
        scores.append(score)
        if score > 0.7:
            matches = True

    if conversation.trigger_noun and noun:
        score = calculate_string_distance(conversation.trigger_noun, noun)
        averaged_score += score
        scores.append(score)
        if score > 0.7:
            matches = True
    if scores:
        averaged_score = averaged_score/len(scores)
    return matches, averaged_score


#
# gibberish detector functions
#


def avg_transition_prob(l, log_prob_mat):
    """ Return the average transition prob from l through log_prob_mat. """
    log_prob = 0.0
    transition_ct = 0
    for a, b in ngram(2, l):
        log_prob += log_prob_mat[pos[a]][pos[b]]
        transition_ct += 1
    # The exponentiation translates from log probs to probs.
    return math.exp(log_prob / (transition_ct or 1))


def normalize(line):
    """ Return only the subset of chars from accepted_chars.
    This helps keep the  model relatively small by ignoring punctuation, 
    infrequenty symbols, etc. """
    return [c.lower() for c in line if c.lower() in accepted_chars]


def ngram(n, l):
    """ Return all n grams from l after normalizing """
    filtered = normalize(l)
    for start in range(0, len(filtered) - n + 1):
        yield ''.join(filtered[start:start + n])


def parse_any_date(sentence, use_mdy=False):
    """
    Parses any sent date let it be written in natural language
    or a specific pattern (like dd-MM-YYYY). By default it looks
    for days first then month and then year, since most countries 
    do it that way(see http://calendars.wikia.com/wiki/Date_format_by_country),
    however it can be changed to search for month first. 
    Please note that this function only parses dates and not time
    :param sentence: 
    :param use_mdy: 
    :return: 
    """
    formatted_date_regex = re.compile("\d{1,2}([-/.])\d{1,2}([-/.])\d{4}")
    found = formatted_date_regex.search(sentence)
    if found is not None:
        return datetime.datetime.strptime(strip_punc(found.group(0),True), "%m%d%Y" if use_mdy else "%d%m%Y").date()
    formatted_date_yf_regex = re.compile("\d{4}([-/.])\d{1,2}([-/.])\d{1,2}")
    found = formatted_date_yf_regex.search(sentence)
    if found is not None:
        return datetime.datetime.strptime(strip_punc(found.group(0),True), "%Y%m%d").date()
    written_month_regex = re.compile("\s{0,1}(january|february|march|april|may|june|july|august|september|october|november|december)(\s{1})(\d{1,2})+")
    found = written_month_regex.search(sentence.lower())
    # now = datetime.datetime.now().date()
    # for future reference https://stackoverflow.com/questions/3418050/month-name-to-month-number-and-vice-versa-in-python
    # https://en.wikipedia.org/wiki/Calendar_date
    if found is not None:
        return datetime.datetime.strptime(strip_punc(found.group(0),True), "%Y%m%d").date()
    else:
        return None





