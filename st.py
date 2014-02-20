#!/usr/bin/python
import sys
import re
from parser import Parser
from Error import Error
from generator import *
from symbol import *

if len(sys.argv) < 2:
    print "Missing file argument"
    exit(0)

print "Scanning:", sys.argv[1] + "..."

errors = []
output = ""
current_lineno = 1
parse_tree = [] # more like parse list

def error_count():
    return len(errors)


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
            parser = Parser(current_lineno, line)
            node = parser.parse()
            if (isinstance(node,Error)):
                errors.append(node)
            elif (node is not None):
                parse_tree.append(node)

        current_lineno = current_lineno+1

for error in errors:
    print "line " + repr(error.lineno) + ": Error: " + error.str

# Lets generate some code
# TODO: Put MainGenerator and EndGenerator in ast
if (len(errors) == 0):
    generator = MainGenerator()
    output += generator.generate()
    print len(parse_tree)
    for node in parse_tree:
        generator = get_generator(node)
        output += generator.generate()

    generator = EndGenerator("0")
    output += generator.generate()
    with open("out/out.c", "w") as out:
        out.write(output)

