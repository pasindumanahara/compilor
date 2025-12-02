import lexer
"""
can able to handle compound statements too
"""
'''
used naming (for documentation) 
BinaryOp(left, op, right) --> binOp
UnaryOp(op, expr) --> unOp
Number(value) --> Num
Identifier(name) --> Var

'''

class ASTNode:
    def __init__(self, left, op, right):
        self.left = left     # variable
        self.op = op         # Token
        self.right = right   # expression

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op      # Token
        self.right = right

class Num(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Var(ASTNode):
    def __init__(self, token):
        self.token = token
        self.name = token.value

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def parse(self):
        node = self.expression()
        if self.current_token.type != 'EOF':
            raise Exception("Unexpected input after expression")
        return node

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Unexpected token {self.current_token} expected {token_type}")
        
    def expression(self):
        node = self.term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token
            if op.type == 'PLUS':
                self.eat('PLUS')
            else:
                self.eat('MINUS')
            node = BinOp(op.value, node, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in ("MUL", "DIV"):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.factor())
        return node
    
    def factor(self):
        token = self.current_token
        if token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expression()
            self.eat('RPAREN')
            return node
        if token.type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            return ('id', token.value)
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return ('num', token.value)
        raise Exception("Invalid syntax in factor")

    def expr(self):
        node = self.term()
        while self.current_token.type in ("PLUS", "MINUS"):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.term())
        return node

