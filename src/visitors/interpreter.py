from src.visitors.base_visitor import Visitor
from src.ast.nodes import *
import random

class InterpreterVisitor(Visitor):
    
    # LITERALS
    def visit_int_literal(self, node):
        return node.value
    
    # STATEMENTS
    def visit_output(self, node):
        values = [self.visit(v) for v in node.value]
        print(*values)

    # EXPRESSIONS
    def visit_or_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if left or right:
            return True
        return False
    def visit_and_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if left and right:
            return True
        return False
    def visit_xor_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if (left and not right) or (not left and right):
            return True
        return False
    def visit_not_expr(self, node):
        value = self.visit(node.cond)
        return not value
    def visit_equal_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return left == right
    def visit_not_equal_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return left != right
    def visit_greater_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return left > right
    def visit_less_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return left < right
    def visit_greater_equal_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return left >= right
    def visit_less_equal_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return left <= right
    def visit_add(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return left + right
    def visit_mul(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return left * right
    def visit_div(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return left / right
    def visit_pow(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return left ** right
    def visit_neg(self, node):
        value = self.visit(node.value)
        return -value
    def visit_between(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return random.randrange(left, right + 1)
    def visit_chance(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if random.randrange(0, right) < left:
            return True
        return False