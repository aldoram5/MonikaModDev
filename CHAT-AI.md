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
  - To use those conversations be sure to move the downloaded ".json" file to the folder for it's category: the folders are in: Monika After Story\game\python-packages\monika_chat\ the folders name indicates it's category, be careful to not rename those folders or Monika won't be able to find those conversations.

The tool itself has a help button that can explain more in detail some of its functions.

## The Node/Step system in a little bit more detail

In the tool these are named steps because I thought that name made more sense since technically speaking the word Node isn't exactly descriptive. These "steps" are the parts in which conform the "conversation" that the player is going to have with Monika. 
So imagine this conversation workflow:

```
player: How are you?
Monika: I'm fine now that you're here with me
Monika: You always brighten my day player~
Monika: But now tell me, how are you?
```
There we have an extract of what would be a conversation with Monika, let's analize it like the Node/Step system would:
First the chat-ai module would analize the player input to determine what conversation flow would be the most appropiate for it.
Then once it has decided which is the best conversation so that conversation will start with it's first step/node: the "I'm fine now that you're here with me" that step defined a text response and a reaction(which can't be seen here since is a text only example), that is what counts as a step/node, once that node finished "playing"(that the user saw the text of finished the interaction) the chat-ai will start with the next node, in this example the next node would be the one that writes "You always brighten my day player~", again it Monika will show an emotion along that text, can't be seen now on this text example though. And now the player is done with that step so it goes to the next step and "plays" it. Now this time it's a question so it will expect some sort of player input, let it be either a selection of predefined options or a text written by the player(these can be defined when creating a conversation in the editing tool).
That mentioned step it's not done until the player enters the asked text or chooses an option from the menu. The choice or the text get procesed differently but we'll get into more detail in the next mini section, there's also a mini tutorial after the next section, just in case you want to see more how the conversations work here.

### The Actions system

Ok we have explained a bit in more detail what's exactly a "step/node" but we haven't talked about what is this interaction they can have with the player input, these major "interactions" are made through the initial and final actions, right now they are some kind of work in progress but the general idea is that they can be used to store, process or check the user input and modify the next node according to parameters defined in each action that a node contains. Again I repeat that these actions are still a work in progress because there's lot of things that could be done with them so it would be better if all voices where heard before setting things in stone.

Now this question might be in your head: Why initial and final action? in what do they differ?

To explain this we'll have to see the order of execution of a step/node.
When executing a node the chat-ai system checks for the last node final action with whatever input it received, then it looks for the next step and loads it, then it inmediatly executes the initial action of this node and continues processing that node data.
So as you can see you can use the node that asked for input final action to process the input and even change the next step if required since it hasn't been loaded, meanwhile initial actions can be used when being a selected option of a menu since you know the selected option by that time. Again as I said nothing about what the actions can do isn't set in stone so feel free to make any sort of suggestions. Below there's the tool's tutorial that can help you to clean any doubts you may still have about this step/node system.

### Creating a conversation mini tutorial
Be sure to head over the [chat editor tool](https://www.crimsonrgames.com/monika/)  and leave it open in another tab if you want to "follow along".

Let's say that the conversation we are creating is a response to something like "I like your hair!", then we would like that Monika would answer: "Thanks, $PLAYER!" with a happy expression, then in the editor we would create a first step which automatically is going to be our initial step( that step is going to be the first executed to answer the player), then we simply fill out the field labeled: "Text Monika will say" with our desired text "Thanks, $PLAYER!", also since we want Monika to look happy we take a look at our [Monika Expression cheat sheet](https://github.com/Backdash/MonikaModDev/blob/master/docs/MonikaCheatsheet.jpg), and decide that we would like an expression of "1j" which would be fitting for the emotion we desire to express, so we fill with that combination our reaction field. 
Up to that point we have a working conversation that only used a single step with no actions, that would defintely would work, however Monika would like to know exactly what makes the player like her hair. To allow her to ask, we'll be needing another step, in this step we would like to ask if it's because of her hair color, because that might be an importat info to let Monika know, so this step might be filled with the "is it because my hair color?" in the "Text Monika will say" and the reaction field might be alright with a "2a" expression. However since we are expecting the player to interact by answering the question we need to specify a "Player Input Type" other than "No player input". The available options right now are "multi" and "text". Multi is a menu of options predefined and Text will pop up an interface to write text. For this case we could be completely fine with a menu of options for the player to choose from, so we change the field "Player Input Type" to multi and then a button labeled "Add menu item" will appear, we press it three times to create 3 menu options, those options will appear below the text ofthe step we're editing, the options contain only two fields: the text to display and the id of the next step to go if the player chooses that menu option. So now this is the first time we mention that next step field, right? well this field was also present at the other step we were editing before, but we ignored it on purpose since there were no other steps, but now we have 2 steps "N1" and "N2" so we can go back to our previous step and mark the next step as "N2" with that we're saying that the next thing to execute once the player read the message is to go to the step N2 and execute it. With that info we can now are going to go back to edit our step N2 menu items we will add to the "Menu options text" fields the following values: "Yes but that's not the only reason", "Yes, it's because it's a lively color!", "That's not exactly the reason", and we'll leave blank the "Next step" fields for now, we'll come back to them later.
Now we'll create 3 more steps, one for each menu option, please note that this might not always be the case, there are times where two or more menu options could go to the same step, just keep that in mind when designing conversations. We'll fill one of those steps with a text saying "Well you like my hair and that's what matters" with a reaction of "1m", that step will be the next step of our "That's not exactly the reason" menu option from before so be sure to go there and and select this node id there. In one of the other empty steps we're going to write the text "I'm happy you like my hair color, that's its natural color just so you know. Ehehe~" with a reaction of "1k", this will be the next step of the menu option "Yes, it's because it's a lively color". Finally as an excersise for the reader, the last empty step will be used for monika to ask more info about what the player likes about her hair. This can be done by using the techniques learned through this tutorial. 

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
