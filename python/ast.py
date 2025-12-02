from parser import Parser, ASTNode, BinOp, Num, Var, Assign, Block, Return
from lexer import Lexer

class Interpreter:
    def __init__(self, tree):
        self.tree = tree
        self.global_scope = {}  # Symbol table for variables

    def visit(self, node):
        if isinstance(node, Num):
            return node.value
        elif isinstance(node, Var):
            if node.name in self.global_scope:
                return self.global_scope[node.name]
            else:
                raise Exception(f"Variable '{node.name}' not defined")
        elif isinstance(node, BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            if node.op.type == 'PLUS':
                return left + right
            elif node.op.type == 'MINUS':
                return left - right
            elif node.op.type == 'MUL':
                return left * right
            elif node.op.type == 'DIV':
                return left // right  # integer division
            else:
                raise Exception(f"Unknown operator {node.op.type}")
        elif isinstance(node, Assign):
            value = self.visit(node.right)
            self.global_scope[node.left.name] = value
            return value
        elif isinstance(node, Return):
            return self.visit(node.expr)
        elif isinstance(node, Block):
            result = None
            for stmt in node.statements:
                result = self.visit(stmt)
                if isinstance(stmt, Return):
                    break  # stop at return
            return result
        else:
            raise Exception(f"Unknown node type: {type(node)}")

    def interpret(self):
        # Look for main function block
        for stmt in self.tree.statements:
            if isinstance(stmt, FuncDef) and stmt.name == "main":
                return self.visit(stmt.block)
        raise Exception("No main function found")
