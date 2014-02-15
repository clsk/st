class Node(object):
    def __init__(self, type):
        self.type = type or "Node"

    def children(self):
        pass

class DeclarationNode(Node):
    def __init__(self, name, elements, redeclaration):
        Node.__init__(self, "Declaration")
        self.name = name
        self.elements = elements
        self.redeclaration = redeclaration

    def __len__(self):
        return len(self.elements)
