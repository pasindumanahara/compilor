import sys
from lexer import Lexer
from parser import Parser
from ast import Interpreter

# Optionally read from file:

if len(sys.argv) < 2:
    sys.exit(1)

source_file = sys.argv[1]

with open(source_file, 'r') as f:
    content = f.read()


# lexer phase
lexer = Lexer(content)

#parser phase
parser = Parser(lexer)

# paser ast output
ast = parser.parse()
print(ast)
'''
# interpreter calling 
interpreter = Interpreter(parser)

result = interpreter.interpret()
print("Program returned:", result)
'''