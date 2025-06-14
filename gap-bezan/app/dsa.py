


class Node(data):
    self.data = data
    self.new_node = None

class Linked_list:

    def __init__(self):
        self.head = None

    def insert_at_start(self, data):
        new_node = Node(data)
        if self.head == None:
            self.head = new_node

        self.new_node = self.head 
        self.head = new_node