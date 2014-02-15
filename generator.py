class Generator(object):
    def generate(self):
        pass

class MainGenerator(Generator):
    def generate(self):
        return '#include <stdlib.h>\n#include <stdio.h>\n#include "vector.h"\nint main() {\n'

class EndGenerator(Generator):
    def __init__(self, retstatus = "0"):
        self.retstatus = retstatus

    def generate(self):
        return "return %s;\n}" % self.retstatus

class DeclarationGenerator(Generator):
    def __init__(self, decl_node):
        self.decl_node = decl_node

    def generate(self):
        name = self.decl_node.name
        out = ""
        realloc = False;
        if (not self.decl_node.redeclaration):
            out += "Vector %s; %s.vect = NULL; " % (name, name)

        out += "%s.len = %d; %s.vect = realloc(%s.vect, sizeof(double)*%s.len);\nif(%s.vect == NULL) {printf(\"Runtime Error: Cannot Allocate System Memory!\");}\n" % (name, len(self.decl_node), name, name, name, name)
        i = 0
        for e in self.decl_node.elements:
            out += name + ".vect[" + str(i) + "] = " + e + ";\n"
            i = i+1

        return out
