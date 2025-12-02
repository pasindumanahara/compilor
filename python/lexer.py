# for testing arg 
#import sys

class Token:
    def __init__(self,type,value,line):
        self.type = type
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"Token({self.type},{self.value},{self.line})"
        
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
    
    def string_literal(self):
        result = ''
        self.advance() 
        
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\\':
                self.advance()
                if self.current_char == 'n': result += '\n'
                elif self.current_char == 't': result += '\t'
                elif self.current_char == '"': result += '"'
                elif self.current_char == '\\': result += '\\'
                else: result += self.current_char
            else:
                result += self.current_char
            self.advance()

        if self.current_char != '"':
            raise Exception(f"Unterminated string literal at line {self.line}")
            
        self.advance() 
        return Token("STRING_LITERAL", result, self.line)
    
    def get_next_token(self):
        while self.current_char is not None:   
            
            # 1. Skip Whitespace
            if self.current_char.isspace():
                self.skip_whitspaces()
                continue
            
            # 2. Handle Comments and Division
            if self.current_char == '/':
                peek = self.peek()
                if peek == '/':
                    self.skip_line_comments()
                    continue
                elif peek == '*':
                    self.skip_block_comments()
                    continue
                
            # 3. Identifiers and Keywords
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()
            
            # 4. Numbers
            if self.current_char.isdigit():
                return self.number()

            # 5. String Literals 
            if self.current_char == '"':
                return self.string_literal()

            # 6. Operators 
            token = self.match_operator()
            if token:
                return token

            # 7. Structural Symbols 
            if self.current_char == '{':
                self.advance(); return Token("LBRACE", '{', self.line)
            if self.current_char == '}':
                self.advance(); return Token("RBRACE", '}', self.line)
            if self.current_char == '(':
                self.advance(); return Token("LPAREN", '(', self.line)
            if self.current_char == ')':
                self.advance(); return Token("RPAREN", ')', self.line)
            if self.current_char == ';':
                self.advance(); return Token("SEMICOLON", ';', self.line)
            if self.current_char == ',':
                self.advance(); return Token("COMMA", ',', self.line)

            # 8. Preprocessor 
            if self.current_char == '#':
                self.advance()
                return Token("HASH", "#", self.line)

            # Error
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

        # Compound assignments
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
                

'''
# testing 
# Test the Lexer
if __name__ == "__main__":
    code = """
    int main() {
        int a = 10;
        if (a >= 10) {
            return "Success"; /* Block Comment */
        }
        return 0; // Line Comment
    }
    """
    # change given code to argument for demo
    if len(sys.argv) < 2:
        sys.exit(1)
    source_file = sys.argv[1]

    with open(source_file, "r") as f:
        content = f.read()
    
    lexer = Lexer(content)
    token = lexer.get_next_token()
    while token.type != "EOF":
        print(token)
        token = lexer.get_next_token()

'''