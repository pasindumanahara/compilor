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

# example lexer class helper
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None
        
    def peek(self):        
        next_pos = self.pos + 1
        if next_pos < len(self.text):
            return self.text[next_pos]
        return None

    def identifier(self):        
        result = ""
        if not (self.current_char.isalpha() or self.current_char == '_'):
            raise Exception(f"Invalid identifier start '{self.current_char}' at line {self.line}")
        
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        if result in KEYWORDS:
            return Token(result.upper(), result, self.line)

        return Token("ID", result, self.line)

    def _id(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        if result in KEYWORDS:
            return Token(result.upper(), result, self.line)  
        else:
            return Token("ID", result, self.line)

    def number(self):        
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token("INT_LITERAL", int(result), self.line)
    
    def skip_whitspaces(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_line_comments(self):
        self.advance()
        self.advance()
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

    def skip_block_comments(self):
        self.advance()
        self.advance()
        while self.current_char is not None:
            if self.current_char == '*' and self.peek() == '/':
                self.advance()
                self.advance()
                return
            else:
                self.advance()
        raise Exception(f"Unterminated block comment at line {self.line}")
    
    def get_next_token(self):
        while self.current_char is not None:   
            # white spaces         
            if self.current_char.isspace():
                self.skip_whitspaces()
                continue
            
            # handle comments
            if self.current_char == '/':
                next_char = self.peek()
                if next_char == '/':
                    self.skip_line_comments()
                    continue
                if next_char == '*':
                    self.skip_block_comments()
                    continue 
                self.advance()
                return Token("DIV",'/',self.line)
            
            # identifers and key words
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier() # TODO
            
            if self.current_char.isdigit():
                return self.number()
            
            # operators
            if self.current_char == '+':
                self.advance()
                return Token("PLUS", '+', self.line)
            if self.current_char == '-':
                self.advance()
                return Token("MINUS", '-', self.line)
            if self.current_char == '*':
                self.advance()
                return Token("MUL", '*', self.line)
            if self.current_char == '=':
                self.advance()
                return Token("ASSIGN", '=', self.line)
            if self.current_char == ';':
                self.advance()
                return Token("SEMI", ';', self.line)
            if self.current_char == '(':
                self.advance()
                return Token("LPAREN", '(', self.line)
            if self.current_char == ')':
                self.advance()
                return Token("RPAREN", ')', self.line)
            
            # unknown character
            raise Exception(f"Illegal character '{self.current_char}' at line {self.line}")
        return Token("EOF", None, self.line)
    
    def match_operator(self):
        ch = self.current_char
        nxt = self.peek()

        if ch == '=' and nxt == '=':
            self.advance()
            self.advance()
            return Token("EQ", "==", self.line)
        if ch == '!' and nxt == '=':
            self.advance(); self.advance()
            return Token("NEQ", "!=", self.line)
        if ch == '>' and nxt == '=':
            self.advance(); self.advance()
            return Token("GE", ">=", self.line)
        if ch == '<' and nxt == '=':
            self.advance(); self.advance()
            return Token("LE", "<=", self.line)
        if ch == '+' and nxt == '+':
            self.advance(); self.advance()
            return Token("INC", "++", self.line)
        if ch == '-' and nxt == '-':
            self.advance(); self.advance()
            return Token("DEC", "--", self.line)

        # Compound assignment: += -= *= /=
        if ch == '+' and nxt == '=':
            self.advance(); self.advance()
            return Token("PLUS_ASSIGN", "+=", self.line)
        if ch == '-' and nxt == '=':
            self.advance(); self.advance()
            return Token("MINUS_ASSIGN", "-=", self.line)
        if ch == '*' and nxt == '=':
            self.advance(); self.advance()
            return Token("MUL_ASSIGN", "*=", self.line)
        if ch == '/' and nxt == '=':
            self.advance(); self.advance()
            return Token("DIV_ASSIGN", "/=", self.line)

        # Single-character operators
        if ch == '+':
            self.advance()
            return Token("PLUS", "+", self.line)
        if ch == '-':
            self.advance()
            return Token("MINUS", "-", self.line)
        if ch == '*':
            self.advance()
            return Token("MUL", "*", self.line)
        if ch == '/':
            self.advance()
            return Token("DIV", "/", self.line)
        if ch == '=':
            self.advance()
            return Token("ASSIGN", "=", self.line)
        if ch == '>':
            self.advance()
            return Token("GT", ">", self.line)
        if ch == '<':
            self.advance()
            return Token("LT", "<", self.line)
        if ch == '&':
            self.advance()
            return Token("AND", "&", self.line)
        if ch == '|':
            self.advance()
            return Token("OR", "|", self.line)

        return None
                
                

            

    

# example for using this functions and the class to check each token 
'''
def get_next_token(self):
    while self.current_char is not None:

        if self.current_char.isspace():
            self.skip_whitespace()
            continue

        if self.current_char.isalpha() or self.current_char == '_':
            return self._id()

        if self.current_char.isdigit():
            return self.number()

        # handle comments
        if self.current_char == '/':
            if self.peek() == '/':
                self.skip_line_comment()
                continue
            if self.peek() == '*':
                self.skip_block_comment()
                continue
            return Token("DIV", '/', self.line)

        # handle operators (==, !=, <=, etc.)
        token = self.match_operator()
        if token:
            return token

        # symbols ((), {}, etc.)
        if self.current_char in SINGLE_CHAR_TOKENS:
            ch = self.current_char
            self.advance()
            return Token(SINGLE_CHAR_TOKENS[ch], ch, self.line)

        # unknown character → error
        raise Exception(f"Unexpected char {self.current_char!r} at line {self.line}")

    return Token("EOF", None, self.line)

'''