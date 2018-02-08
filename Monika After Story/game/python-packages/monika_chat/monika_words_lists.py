# Word and phrases lists that help Monika process the info the player writes
#

# Greeting oriented specific words, used to influence a greeting dialogue of act classification
common_greeting_specific = ["hi", "hello", "howdy", "hiya"]


# Couldn't really find a way to check for the how are you doing variants
# might need to train a model to classify them, but it seems like overkill
how_are_you_variants = ["what is up", "how is it going", "how are you doing",
                        "how are you", "what is new", "how is everything",
                        "how are things", "how is life", "how is your day going",
                        "how have you been"]


# Helpers for reading time of the day
time_related = ["day", "evening", "night", "afternoon", "morning"]

# Valid terms gibberish detector should let pass
short_valid_messages = ["hi", "hey", "mmm", "sup", "hiya", "yo", "love"]

# POS Tags for Wh questions
wh_question_tags = ['WP', 'WD', 'WR']

# Verbs for YN questions
yn_verbs = ["be", "do", "have"]