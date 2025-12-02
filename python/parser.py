from lexer import Token
class ASTNode:
    pass

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.op.type} {self.right})"

class Num(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"Num({self.value})"

class Var(ASTNode):
    def __init__(self, token):
        self.token = token
        self.name = token.value

    def __repr__(self):
        return f"Var({self.name})"

class Assign(ASTNode):
    def __init__(self, left, op, right):
        self.left = left  
        self.op = op     
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.op.type} {self.right})"

class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return "Block([" + ", ".join(map(str, self.statements)) + "])"

class Return(ASTNode):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"Return({self.expr})"
class FuncDef(ASTNode):
    def __init__(self, return_type, name, body):
        self.return_type = return_type  
        self.name = name                
        self.body = body                

    def __repr__(self):
        return f"FuncDef({self.return_type.value} {self.name.value}, {self.body})"
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Unexpected token {self.current_token}, expected {token_type}")

    def parse(self):
        nodes = []
        while self.current_token.type != 'EOF':
            nodes.append(self.function())
        return nodes  
    
    def statement(self):
        token = self.current_token
        if token.type == 'INT':
            self.eat('INT')
            var_token = self.current_token
            if var_token.type != 'ID':
                raise Exception(f"Expected variable name after int, got {var_token}")
            self.eat('ID')
            var_node = Var(var_token)
            if self.current_token.type == 'ASSIGN':
                assign_token = self.current_token
                self.eat('ASSIGN')
                expr_node = self.expression()
                self.eat('SEMICOLON')
                return Assign(var_node, assign_token, expr_node)
            else:
                self.eat('SEMICOLON')
                return var_node
        elif token.type == 'RETURN':
            self.eat('RETURN')
            expr = self.expression()
            self.eat('SEMICOLON')
            return Return(expr)      
        elif token.type == 'LBRACE':
            self.eat('LBRACE')
            stmts = []
            while self.current_token.type != 'RBRACE':
                stmts.append(self.statement())
            self.eat('RBRACE')
            return Block(stmts)       
        elif token.type == 'ID':
            left = Var(token)
            self.eat('ID')
            if self.current_token.type != 'ASSIGN':
                raise Exception(f"Expected '=', got {self.current_token}")
            op = self.current_token
            self.eat('ASSIGN')
            right = self.expression()
            self.eat('SEMICOLON')
            return Assign(left, op, right)
        else:
            raise Exception(f"Unknown statement starting with {token}")

    def function(self):
        ret_type = self.current_token
        self.eat('INT')        
        name = self.current_token
        self.eat('ID')        
        self.eat('LPAREN')
        self.eat('RPAREN')        
        body = self.statement() 
        return FuncDef(ret_type, name, body)

    def expression(self):
        node = self.term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(left=node, op=op, right=self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in ('MUL', 'DIV'):
            op = self.current_token
            self.eat(op.type)
            node = BinOp(left=node, op=op, right=self.factor())
        return node

    def factor(self):
        token = self.current_token
        if token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expression()
            self.eat('RPAREN')
            return node
        elif token.type == 'ID':
            self.eat('ID')
            return Var(token)
        elif token.type == 'INT_LITERAL':
            self.eat('INT_LITERAL')
            return Num(token)
        else:
            raise Exception(f"Invalid syntax in factor: {token}")

