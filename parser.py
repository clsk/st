import re
from Error import Error
from ast import *
re_reserved_words = r"[S|C|E|P|I|<|>]"
re_identifier = r"[a-z]"
re_float = "^(\d+(.\d+)?([E|e][+-]?\d+)?)$"

class Identifier:
    def __init__(self, name, elements):
        self.name = name
        self.elements = elements

    def __len__(self):
        return len(self, elements)

class Parser:


    def __init__(self, lineno, line, sym_table):
        self.lineno = lineno
        self.line = line
        self.parser = self._get_parser(line[0])
        self.generate = None
        self.sym_table = sym_table

    def parse(self):
        return self.parser(self)

    # private
    def _parse_assignment(self):
        if (self.line[1] != " "):
            return Error(lineno, "Expecting space between identifier and definition.")
        elements = self.line[2:].strip().split(" ")
        for f in elements:
            if (not re.match(re_float, f)):
                return Error(self.lineno, "'{0}' is not a valid float".format(f))

        self.sym_table[self.line[0]] = DeclarationNode(self.line[0], elements, self.line[0] in self.sym_table)
        return self.sym_table.get(self.line[0])

    def _parse_reserved(self, line):
        return None

    def _get_parser(self, c):
        for regex, func in Parser._func_table.iteritems():
            if (re.match(regex, c)):
                return func

    _func_table = {
            re_reserved_words: _parse_reserved,
            re_identifier: _parse_assignment
    }

