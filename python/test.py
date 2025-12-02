import sys
from lexer import Lexer
from parser import Parser

source_file = sys.argv[1]

with open(source_file,'r') as f:
    content = f.read()

lexer = Lexer(content)
token = lexer.get_next_token()
while token.type != "EOF":
    #print(token)
    tmp = Parser(token)
    re_tmp = tmp.parse()
    print(re_tmp)
    #token = lexer.get_next_token()