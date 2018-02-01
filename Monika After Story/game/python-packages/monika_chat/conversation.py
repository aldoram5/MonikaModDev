
class Conversation:

    def __init__(self):
        self.trigger_verb = ""
        self.trigger_adj = ""
        self.trigger_noun = ""
        self.trigger_subject = ""
        self.next_node = ""
        self.nodes = {}

    def add_node(self,node):
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

    def add_option(self,text_option, next_node_id):
        self.options.append((text_option,next_node_id))

    def determine_next_node(self,selected_option):
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

    def set_check_value_type(self):
        self.type = "check"

    def set_store_value_type(self):
        self.type = "store"


