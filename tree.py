class Node:
    def __init__(self):
        self.children = []
        self.parent = None
        self.data = None

    def add_child(self, child):
        self.children.append(child)
        child.parent = self
