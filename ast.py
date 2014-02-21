class Node(object):
    def __init__(self, type, parent=None):
        self.type = type or "Node"
        self.parent = parent

class EmptyNode(Node):
    def __init__(self):
        Node.__init__(self, "EmptyNode")

class AssignmentNode(Node):
    def __init__(self, name, redeclaration, child_node = None):
        Node.__init__(self, "Assignment")
        self.name = name
        self.redeclaration = redeclaration
        self.child_node = child_node

class VectorLiteralNode(Node):
    def __init__(self, parent, elements):
        Node.__init__(self, "VectorLiteral", parent)
        self.parent = parent
        self.elements = elements

class OperationNode(Node):
    def __init__(self, operation, parent, args):
        Node.__init__(self, "Operation", parent)
        self.operation = operation
        self.args = args

class OutputNode(Node):
    def __init__(self, output, is_vector):
        Node.__init__(self, "Output")
        self.output = output
        self.is_vector = is_vector

class InputNode(Node):
    def __init__(self, parent):
        Node.__init__(self, "Input", parent)
