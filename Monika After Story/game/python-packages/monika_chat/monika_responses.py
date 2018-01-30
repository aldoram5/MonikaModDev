from conversation import Action, Conversation, Node

# Monika's predefined answers when you tell nonsense to her

answers_for_gibberish =\
    [[("Why would you say that to me?", "1c",),("That didn't make any sense.", "1q")],
                        [("What was that?", "1m"),("Stop teasing me like that.", "1n")],
                        [("Sorry I couldn't understand that.", "1o")],
                        [("bhcsjnjdnjshn", "1a"), ("nuybyubefy ujjdujqwer", "1r"),
                         ("asdadsf ", "1q"),("I can say nonsense too, you know?", "1a"),
                         ("Ahaha~", "1k")
                         ]]

answers_for_greetings =\
    [[("Hello again, sweetheart!", "1k",),
      ("It's kind of embarrassing to say out loud, isn't it?","1l"),
      ("Still, I think it's okay to be embarrassed every now and then.","3b")],
                        [("Hi! Welcome back.", "1b"), ("I'm so glad that you're able to spend some time with me.", "1k")],
                        [("Oh, hello there!", "1j")],
                        [("Hi honey!", "1j")]]

answers_for_current_state_query =\
    [[("Hello again, sweetheart!", "1k",),
      ("It's kind of embarrassing to say out loud, isn't it?","1l"),
      ("Still, I think it's okay to be embarrassed every now and then.","3b")],
                        [("Hi! Welcome back.", "1b"), ("I'm so glad that you're able to spend some time with me.", "1k")],
                        [("Oh, hello there!", "1j")],
                        [("Hi honey!", "1j")]]


monika_predef_answers = {"nonsense": answers_for_gibberish, "greeting" : answers_for_greetings}


def get_opinion_monika_conversations():
    conversations = {}
    gibber1 = Conversation()

def get_yes_no_query_conversations():
    conversations = {}
    gibber1 = Conversation()

def get_wh_query_conversations():
    pass

def get_statements_conversations():
    pass
