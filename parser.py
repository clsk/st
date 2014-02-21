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

    def parse(self):
        if (len(self.line) < 3 or self.line[1] != " "):
            return Error(self.lineno, "At least one argument is expected per statement")

        token, self.line = Parser._eat_token(self.line)

        if (token == '<'):
            return self._parse_output(token);
        elif (token == '>'):
            return self._parse_input(token);
        elif (re.match(re_identifier, token)):
            return self._parse_assignment(token)
        elif (token in reserved_words):
            return self._parse_reserved(token, None)
            # No code needs to be generated for this as the result will get thrown away anyways
            return None
        else:
            return Error(self.lineno, "Unexpected Token '%s'" % self.line[0])

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

    def _parse_output(self, token):
        self.line = self.line.strip()
        if (self.line[0] == '"'): # Output string
            if (self.line[-1] != '"'):
                return Error(self.lineno, "Unmatched quotes")
            is_vector = False
        else: # Output Vector
            tokens = Parser._tokenize(self.line)
            if (len(tokens) != 1):
                return Error(self.lineno, "Exactly one argument expected for output operation")
            if (not Parser._is_identifier(self.line)):
                return Error(self.lineno, "%s is not a valid identifier" % self.line)
            if (self.line not in Symbol.table):
                return Error(self.lineno, "Undeclared identifier {0}.")

            is_vector = True

        return OutputNode(self.line, is_vector)

    def _parse_input(self, token):
        tokens = Parser._tokenize(self.line)
        if (len(tokens) != 1):
            return Error(self.lineno, "Exactly one argument expected for input operation")
        if (not Parser._is_identifier(self.line)):
            return Error(self.lineno, "%s is not a valid identifier" % self.line)
        # Handle this as an assignment
        n = AssignmentNode(self.line, self.line in Symbol.table)
        if (self.line not in Symbol.table):
            Symbol.table[self.line] = Symbol(self.line)
        n.child_node = InputNode(n)
        return n

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

        if (node.name not in Symbol.table):
            Symbol.table[node.name] = Symbol(node.name)

        return node

    _args_for_op = {
            'S': 1,
            'C': 1,
            'E': 2,
            'P': 2,
            'I': 1
            }

    def _parse_reserved(self, token, parent):
        tokens = Parser._tokenize(self.line)
        if (Parser._args_for_op[token] != len(tokens)):
            return Error(self.lineno, "Exactly %d argument(s) expected for %s operation" % (args_for_op[token], token))
        for arg in tokens:
            if (not Parser._is_identifier(arg)):
                return Error(self.lineno, "%s is not a valid identifier" % arg)
            if (arg not in Symbol.table):
                return Error(self.lineno, "Undeclared identifier {0}.")

        if (parent == None):
            # If this operationg won't get assigned to anything
            # Then just return None
            return None
        else:
            return OperationNode(token, parent, tokens)

        return None

