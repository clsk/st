def get_generator(node):
    if (node.type == "Assignment"):
        return AssignmentGenerator(node)
    elif (node.type == "Operation"):
        return OperationGenerator(node)
    elif (node.type == "Output"):
        return OutputGenerator(node)
    else:
        return None

class Generator(object):
    def __init__(self, node = None):
        self.node = node
    def generate(self):
        return ""

class MainGenerator(Generator):
    def generate(self):
        return '#include <stdlib.h>\n#include <stdio.h>\n#include "vector.h"\nint main() { Vector tmp;\n'

class EndGenerator(Generator):
    def __init__(self, retstatus = "0"):
        self.retstatus = retstatus

    def generate(self):
        return "return %s;\n}" % self.retstatus

class VectorLiteralGenerator(Generator):
    def __init__(self, node):
        Generator.__init__(self, node)

    def generate(self):
        name = self.node.parent.name
        out = "vector_realloc(&%s, %d);\n" % (name, len(self.node.elements))
        i = 0
        for e in self.node.elements:
            out += name + ".data[" + str(i) + "] = " + e + ";\n"
            i = i+1

        return out

class AssignmentGenerator(Generator):
    def __init__(self, decl_node):
        Generator.__init__(self, decl_node)

    def generate(self):
        name = self.node.name
        out = ""
        if (not self.node.redeclaration):
            out += "Vector %s; vector_init(&%s);\n" % (self.node.name, self.node.name)

        if (self.node.child_node.type == "VectorLiteral"):
            generator = VectorLiteralGenerator(self.node.child_node)
            out += generator.generate()
        elif (self.node.child_node.type == "Operation"):
            generator = OperationGenerator(self.node.child_node)
            out += generator.generate()

        return out

class OperationGenerator(Generator):
    def __init__(self, node):
        Generator.__init__(self, node)

    def generate(self):
        out = "tmp = %s;  %s = vector_%c(" % (self.node.parent.name, self.node.parent.name, self.node.operation)
        for arg in self.node.args:
            out += "&%c," % arg

        out = out[:-1]
        out += "); vector_free(&tmp);\n"

        return out

class OutputGenerator(Generator):
    def __init__(self, node):
        Generator.__init__(self, node)

    def generate(self):
        if (self.node.is_vector):
            return "vector_output(&%s);\n" % self.node.output
        else:
            return "printf(%s);\n" % self.node.output
