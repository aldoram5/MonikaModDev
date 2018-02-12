# Chat-ai branch features

## Initial motivation
The chat- ai branch was built by having in mind a communication system to a more personal level with our loved Monika. Interaction is key in this system where the player actually starts the conversation about different topics not only by making questions, but also by saying statements about almost whatever is in the player's mind. Also by allowing natural language communication the player gets that "reality" feeling, and feels closer to Monika. 

## High level briefing of what is this thing exactly

The chat ai system is based on the works of current industry standards of how chatbots like [wit.ai](https://wit.ai/) or [converse.ai](https://get.converse.ai/docs/introduction-1) work by using retrieval based responses. This is mostly because Monika is a more complicated character and her responses can't be generated like in a generative based chabot; also because of the inreactive nature that retrieval based chatbots can bring it was the best one to go with. Since this is idea is about having already generated conversation flows defined by the writting team it's top priority to have a tool that can make that job as easy as possible so it was necessary to create the [Conversation editor](https://www.crimsonrgames.com/monika/).

With that tool writters can create conversations more easily than having to edit a renpy or python source file, also they can work on conversations without worrying about somebody else working on the same file and later on having to deal with merging and fixing conflicts. The conversations are stored in a JSON format, which plays nice with almost any technology out there, so in case of migratting the editor or something all the work can be carried over seamessly. Also, since the JSON files are outside the project and they are parsed during initialization writters/testers/anyone can test their conversations on the current "production release", whitout having to clone the repo and setup a dev environment. Also this gives the opportunity to enthusiasts to try things themselves and maybe then they'll want to add their conversation work to others by contributing it to the repo. The tool supports loading a conversation file and then editing it in case of errors or mistakes.
The current tool is web based, meaning that it requires no installation and that it'll work on most desktops without having to worry about the OS, only about the browser.

## Features
  - Natural language processing of player inputs to determine what Monika should answer
  - Node/Step based Conversation system that allows full control over her conversations with the player without having to code an "identation" monster on Renpy or an "if" nightmare on Python
  - An action system that intends to bring a new layer of things that can be achieved while on a conversation(right now only the store data action is the only one working, newer action types will be provided as writters and devs require)
  - Use of a Token system in chats that can help make conversations more personal by allowing any user use an stored variable to replace that token in a conversation (right now the only token working is $PLAYER, newer tokens will be provided as writters and devs require)
  - By having Monika collect player-specific info we can use it in conversations making the experience with Monika different, unique and fully personalized for every player


# How does those things work

## Player input parsing 
The system first filters out inputs that don't make sense like "asdadas" and similar things; if it detects something like that then it returns a predefined answer(this can be changed to selecting randomly from a pool of conversations generated with the tool, I need your opinions on this).
If the input passes that filter then it gets classified in one of these categories: Current state question(how are you?), Greeting(hi! and others), Wh question(what, where, etc. questions), Yes no questions, opinions about Monika and Statements. The greeting and current state questions both have predefined answers because Monika already greets you when opening the mod and also you're given the good morning and good evening options in the talk menu, for current state is mostly because there aren't any sort of rules about how determine those so the system can't really be useful to offer many options for it, the default answer can be changed with the feedback of devs and the writting team. The other types get their answer selected depending on what the user is talking about, this is determined by using an algorithm to match with the conversations created with the tool.

## Conversations created with the tool

The conversations have their own way to be selected as correct answer to a conversation request by allowing to fill up the term to be matched accordingly like the statement subject, the verb, the adjective or the person or object the statement is refering to.
All the conversations are just a collection of steps, to be followed according to the order we determine in the tool. 
The tool let's you decide many things: 
  - The text monika will say, here the option is given to use some special tokens that will get replaced at runtime by values stored like the player name replacing the $PLAYER token
  - The expression she is going to have, these match the already defined cheatsheet
  - Ask for player input which can be either a renpy menu that will let you decide to which step the conversation can go depending on what the player choose, the other input is the text based. 
  - The tool also let's you define an initial or final action to excecute in that step, right now the actions require feedback to add more types and make them more useful for integrations. 

The tool itself has a help button that can explain more in detail some of its functions.

## Features on the works or that require feedback or that are just ideas floating in the air

  - Read any input date and allow the conversation retrieve it as needed to either store it or check it against another date. I already have half of the function written, will get back to it soon 
  - The predefined answers in greetings, nonsense and current state queries must be either specified by the writting team, dropped entirely or changed so they can be loaded as well
  - There's also a predefined answer if she can't find a suitable response this one also must be defined by the writters
  - The token system needs more Tokens to work with $DATE, $TODAY, $TOMORROW tokens are kinda planned but still feedback would be very welcome here.
  - The actions system requires more actions to be really useful, opinions on what types of actions could be helpful would be very appreciated
  - There's a memory module that right now only works to store info about the player input sentence in the temporal memory, however the permanent memory isn't permanent because I want to know if the values gotten from the chat module should be stored in the persistent file or in another file
  - In that memory module there's also some variables that are named after human emotions, the idea was that conversations could change her emotions and also her conversations could vary depending on her emotions as well, however this seemed like an overkill and I never really figured out how to add something with this, if anyone has more imagination for this suggestions are welcome, if not the emotion part can be dropped.
  - Right now for easy use and understanding subjects and refering nouns are limited to one word, however I know there are subjects that contain more than one word, the multi word support can be added if you guys think it'll do more good than bad.
  - I have tested it on Windows 10 and macOS High Sierra, haven't tested on Ubuntu nor any other linux distro, there shouldn't be any problems with it there but if someone can test it I would be really thankful.
  - As a side note the module itself can be run and tested by running the monika-ai file with any python 2.7 interpreter, I developed the python parts of the moule using pycharm, I recommend it if you want to take a look at the source files. The renpy files where modified with Editra.

Thanks for taking time and interest in this system if you have any questions or want a more tech explanation of things I'll be happy to answer.
