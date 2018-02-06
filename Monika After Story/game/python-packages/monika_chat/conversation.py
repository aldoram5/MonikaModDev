import json


class Conversation:

    def __init__(self):
        self.trigger_verb = ""
        self.trigger_adj = ""
        self.trigger_noun = ""
        self.trigger_subject = ""
        self.next_node = ""
        self.nodes = {}

    def load_from_json(self, json_data):
        data = json.load(json_data)
        self.load_from_array_json(data)

    def load_from_array_json(self, data):
        self.trigger_verb = data["verb"]
        self.trigger_adj = data["adjective"]
        self.trigger_subject = data["subject"]
        self.trigger_noun = data["referringNoun"]
        self.next_node = data["nextNode"]
        for node in data["nodes"]:
            temp = Node()
            temp.load_from_array_json(node)
            self.add_node(temp)

    def add_node(self, node):
        if not node.id or node.id is None:
            node.id = 'node'+str(len(self.nodes))
        self.nodes[node.id] = node

    def get_next_node(self):
        if not self.next_node:
            return None
        next_node = self.nodes.get(self.next_node)
        self.next_node = next_node.next_node
        return next_node


class Node:

    def __init__(self):
        self.id = None
        self.initial_action = None
        self.display_text = ""
        self.reaction = ""
        self.next_node = None
        self.input_type = None
        self.final_action = None
        self.options = []

    def load_from_json(self, json_data):
        data = json.load(json_data)
        self.load_from_array_json(data)

    def load_from_array_json(self, data):
        self.id = data["id"]
        self.input_type = data["inputType"]
        self.next_node = data["nextNode"]
        self.reaction = data["reaction"]
        for option in data["options"]:
            self.add_option(option["text"], option["nextNode"])
        if data["initialAction"] is not None:
            self.initial_action = Action()
            self.initial_action.load_from_array_json(data["initialAction"])
        if data["finalAction"] is not None:
            self.final_action = Action()
            self.final_action.load_from_array_json(data["finalAction"])

    def add_option(self,text_option, next_node_id):
        self.options.append((text_option,next_node_id))

    def determine_next_node(self, selected_option):
        if selected_option < len(self.possible_nodes):
            return self.possible_nodes[selected_option]
        else:
            return None

    def set_input_multi(self):
        self.input_type = "multi"

    def set_input_text(self):
        self.input_type = "text"


class Action:

    def __init__(self):
        self.type = ""
        self.key = None
        self.value = None

    def load_from_json(self, json_data):
        data = json.load(json_data)
        self.load_from_array_json(data)

    def load_from_array_json(self, data):
        self.type = data['type']
        self.key = data['key']
        self.value = data['value']

    def set_check_value_type(self):
        self.type = "check"

    def set_store_value_type(self):
        self.type = "store"


