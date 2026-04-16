from src.visitors.base_visitor import Visitor
from src.ast.nodes import *
import random

class InterpreterVisitor(Visitor):
    def __init__(self):
        self.v_table = {}
    
    # LITERALS
    def visit_int_literal(self, node):
        return node.value
    def visit_float_literal(self, node):
        return node.value
    def visit_string_literal(self, node):
        return node.value
    def visit_bool_literal(self, node):
        return node.value
    
    # STATEMENTS
    def visit_create_v(self, node):
        value = self.visit(node.value) if node.value else "UNINITIALIZED"
        self.v_table[node.name] = value
    def visit_create_s(self, node): # IS SUPPOSED TO CHANGE DEPENDING ON TYPECHECKER
        parent = self.v_table.get(node.base, {})
        fields = {field.name: self.visit(field.value) if field.value else "UNINITIALIZED" for field in node.fields}
        self.v_table[node.name] = {**parent, **fields}
    def visit_create_l(self, node):
        listing = [self.visit(item) for item in node.listing] if node.listing else []
        self.v_table[node.name] = listing
    def visit_assign(self, node):
        value = self.visit(node.value)
        if node.base:
            struct = self.v_table.get(node.base, {})
            struct[node.name] = value
            self.v_table[node.base] = struct
        else:
            self.v_table[node.name] = value
    def visit_if(self, node):
        if self.visit(node.cond):
            for stmt in node.body:
                self.visit(stmt)
            return
        for elifs in node.elifs:
            if self.visit(elifs[0]):
                for stmt in elifs[1]:
                    self.visit(stmt)
                return
        if node.elses:
            for stmt in node.elses:
                self.visit(stmt)
    def visit_while(self, node):
        while self.visit(node.cond):
            for stmt in node.body:
                self.visit(stmt)
    def visit_dowhile(self, node):
        while True:
            for stmt in node.body:
                self.visit(stmt)
            if not self.visit(node.cond):
                break
    def visit_forrange(self, node):
        for i in range(self.visit(node.start), self.visit(node.end) + 1):
            self.v_table[node.name] = i
            for stmt in node.body:
                self.visit(stmt)
            self.v_table.pop(node.name, None)
    def visit_foreach(self, node):
        collection = self.v_table[node.collection]
        for i in collection:
            self.v_table[node.name] = collection[i-1]
            for stmt in node.body:
                self.visit(stmt)
            self.v_table.pop(node.name, None)
    def visit_input(self, node):
        self.v_table[node.name] = input()
    def visit_output(self, node):
        values = [self.visit(v) for v in node.value]
        print(*values)

    # EXPRESSIONS
    def visit_or_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return left or right
    def visit_and_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return left and right
    def visit_xor_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return (left and not right) or (not left and right)
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
        return -self.visit(node.value)
    def visit_between(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return random.randrange(left, right + 1)
    def visit_chance(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return random.randrange(0, right) < left
    def visit_var(self, node):
        if node.base:
            struct = self.v_table.get(node.base, {})
            return struct.get(node.name, None)
        return self.v_table.get(node.name, None)