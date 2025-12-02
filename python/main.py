import sys
from lexer import Lexer
from parser import Parser

# Optionally read from file:

if len(sys.argv) < 2:
    print("Usage: python main.py <source_file>")
    sys.exit(1)

source_file = sys.argv[1]

with open(source_file, 'r') as f:
    content = f.read()


# Initialize lexer and parser
lexer = Lexer(content)
parser = Parser(lexer)

# Parse and get AST
ast = parser.parse()

# Print AST
print(ast)
