import re
from Error import Error
from ast import *
from symbol import *
reserved_words = "SCEPI"
re_reserved_words = r"^S|C|E|P|I$"
re_io = r"<|>"
re_identifier = r"[a-z]"
re_float = "^(\d+(.\d+)?([E|e][+-]?\d+)?)$"

class Parser:


    def __init__(self, lineno, line):
        self.lineno = lineno
        self.line = line

    # private
    @staticmethod
    def _is_float(f):
        return bool(re.match(re_float,f))
    @staticmethod
    def _is_identifier(i):
        return bool(re.match(re_identifier, i))
    @staticmethod
    def _tokenize(s):
        return s.strip().split(" ")
    @staticmethod
    def _eat_token(s):
        # Since all tokens consist of single words, we can optimize by removing 2 chars from left
        i = s.find(" ")
        if (i != -1):
            return s[0:i], s[i+1:]
        else:
            return s, ""

    def _parse_io(self, token):
        if (token == "<"): # output
            pass
        else:
            pass

        return None

    def _parse_vector_literal(self, token, parent_node):
        tokens = Parser._tokenize(self.line)
        for f in tokens:
            if (not Parser._is_float(f)):
                return Error(self.lineno, "'{0}' is not a valid float.".format(f))

        tokens.insert(0, token)
        return VectorLiteralNode(parent_node, tokens)


    def _parse_assignment(self, token):
        node = AssignmentNode(token, token in Symbol.table)
        token, self.line = Parser._eat_token(self.line)

        if (re.match(re_float, token)):
            node.child_node = self._parse_vector_literal(token, node)
        elif (token in reserved_words):
            node.child_node = self._parse_reserved(token, node)
        else:
            return Error(self.lineno, "Unidentified argument for assignment")

        # If there is an error, return that
        if (isinstance(node.child_node, Error)):
            return node.child_node

        Symbol.table[node.name] = Symbol(node.name)
        return node

    def _parse_reserved(self, token, parent):
        tokens = Parser._tokenize(self.line)
        if (token == 'S'):
            if (len(tokens) != 1):
                return Error(self.lineno, "Exactly one argument expected for S operation")
            if (not Parser._is_identifier(tokens[0])):
                return Error(self.lineno, "{0} is not a valid identifier".format(tokens[0]))
            if (tokens[0] not in Symbol.table):
                return Error(self.lineno, "Undeclared identifier {0}.")

            if (parent == None):
                return None
            else:
                return SNode(parent, tokens[0])

        return None

    def parse(self):
        if (len(self.line) < 3 or self.line[1] != " "):
            return Error(self.lineno, "At least one argument is expected per statement")

        token, self.line = Parser._eat_token(self.line)

        if (token in '><'):
            return _parse_io(token);
        elif (re.match(re_identifier, token)):
            return self._parse_assignment(token)
        elif (token in reserved_words):
            return self._parse_reserved(token, None)
            # No code needs to be generated for this as the result will get thrown away anyways
            return None
        else:
            return Error(self.lineno, "Unexpected Token '%s'" % self.line[0])
