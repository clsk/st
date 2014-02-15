#!/usr/bin/python
import sys
import re
from parser import Parser
from Error import Error
from generator import *

if len(sys.argv) < 2:
    print "Missing file argument"
    exit(0)

print "Scanning:", sys.argv[1] + "..."

sym_table = {}
errors = []
output = ""
current_lineno = 1
parse_tree = [] # more like parse list

def error_count():
    return len(errors)

def get_symbol(id):
    return sym_table.get(id, None)


# TODO:
# 1. Command line arguments
# open file
with open(sys.argv[1]) as file:
    line_num = 0
    for line in file:
        line = line.strip()
        pos = line.find("#")
        if (pos != -1):
            if (pos == 0):
                current_lineno = current_lineno+1
                continue
            elif (line[pos-1] != "\\"):
                line = line[:pos]
        if (len(line) > 0):
            parser = Parser(current_lineno, line, sym_table)
            node = parser.parse()
            if (isinstance(node,Error)):
                errors.append(node)
            else:
                parse_tree.append(node)

        current_lineno = current_lineno+1

for error in errors:
    print "line " + repr(error.lineno) + ": Error: " + error.str

# Lets generate some code
if (len(errors) == 0):
    generator = MainGenerator()
    output += generator.generate()
    print len(parse_tree)
    for node in parse_tree:
        if (node.type == "Declaration"):
            generator = DeclarationGenerator(node)

        output += generator.generate()
    generator = EndGenerator("0")
    output += generator.generate()
    with open("out/out.c", "w") as out:
        out.write(output)

class Token:
    def __init__(self, token, op1, op2):
        self.token = token
        self.op1 = op1
        self.op2 = op2


# Regular Expressions

