#!/usr/bin/python
import sys
import re
from parser import Parser
from Error import Error
from generator import *
from symbol import *


errors = []
output = ""
current_lineno = 1
parse_tree = [] # more like parse list
infile = None
outfile = "out/out.c"

def error_count():
    return len(errors)


if (__name__ == "__main__"):
    if len(sys.argv) < 2:
        print "Error: Missing input file argument!"
        exit(0)

    it = iter(sys.argv)
    it.next() # Skip this file
    for arg in it:
        if (arg == "-o"):
            outfile = it.next()
        elif arg == "-h":
            print "Syntax: \npython st.py <infile.st> [-o outfile.c]"
            quit()
        else:
            infile = arg

    if (infile == None):
        print "Error: Missing input file argument!"
        quit()

    print "Scanning:", infile + "..."

    # open file
    with open(infile) as file:
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
    if (len(errors) == 0):
        print "Generating code..."
        generator = MainGenerator()
        output += generator.generate()
        for node in parse_tree:
            generator = get_generator(node)
            output += generator.generate()

        generator = EndGenerator("0")
        output += generator.generate()
        print "Writing C file to " + outfile
        with open(outfile, "w") as out:
            out.write(output)
