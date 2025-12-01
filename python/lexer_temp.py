class Token:
    def __init__(self,type,value,line):
        self.type = type
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"Token({self.type},{self.value},{self.value})"
        
KEYWORDS = {
    "int", "return", "if", "else", "while", "for"
}

TOKEN_TYPES = {
    "ID",
    "INT_LITERAL",
    "STRING_LITERAL",

    "PLUS", "MINUS", "MUL", "DIV",
    "ASSIGN",
    "EQ", "NEQ", "LT", "GT", "LE", "GE", 

    "LPAREN", "RPAREN",
    "LBRACE", "RBRACE",
    "SEMICOLON", "COMMA",

    "LINE_COMMENT",
    "BLOCK_COMMENT",

    "EOF"
}
# key value pairs 
SINGLE_CHAR_TOKENS = {
    '+': "PLUS",
    '-': "MINUS",
    '*': "MUL",
    '/': "DIV",
    '=': "ASSIGN",
    '<': "LT",
    '>': "GT",
    '(': "LPAREN",
    ')': "RPAREN",
    '{': "LBRACE",
    '}': "RBRACE",
    ';': "SEMICOLON",
    ',': "COMMA"
}
MULTI_CHAR_TOKENS = {
    '==': "EQ",
    '!=': "NEQ",
    '<=': "LE",
    '>=': "GE"
}

