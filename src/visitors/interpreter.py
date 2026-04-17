from src.visitors.base_visitor import Visitor
from src.ast.nodes import *
import random

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class InterpreterVisitor(Visitor):
    def __init__(self):
        self.v_tables = [{}]
        self.f_table = {}
    
    # SCOPE HANDLING
    def lookup(self, name):
        for v_table in reversed(self.v_tables):
            if name in v_table:
                return v_table[name]
        return None
    def find_scope(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope
        return None
    
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
        self.v_tables[-1][node.name] = value
    def visit_create_s(self, node): # IS SUPPOSED TO CHANGE DEPENDING ON TYPECHECKER
        parent = self.lookup(node.base)
        fields = {field.name: self.visit(field.value) if field.value else "UNINITIALIZED" for field in node.fields}
        self.v_tables[-1][node.name] = {**parent, **fields}
    def visit_create_l(self, node):
        listing = [self.visit(item) for item in node.listing] if node.listing else []
        self.v_tables[-1][node.name] = listing
    def visit_assign(self, node):
        value = self.visit(node.value)
        if node.base:
            struct = self.lookup(node.base)
            struct[node.name] = value
            return
        scope = self.find_scope(node.name)
        scope[node.name] = value
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
            self.v_tables.append({})
            self.v_tables[-1][node.name] = i
            for stmt in node.body:
                self.visit(stmt)
            self.v_tables.pop()
    def visit_foreach(self, node):
        collection = self.lookup(node.collection)
        for item in collection:
            self.v_tables.append({})
            self.v_tables[-1][node.name] = item
            for stmt in node.body:
                self.visit(stmt)
            self.v_tables.pop()
    def visit_define(self, node):
        self.f_table[node.name] = {
            "params" : node.params,
            "body" : node.body
        }
    def visit_return(self, node):
        value = self.visit(node.value)
        raise ReturnException(value)
    def visit_expression(self, node):
        self.visit(node.value)
    def visit_input(self, node):
        scope = self.find_scope(node.name)
        scope[node.name] = input()
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
            struct = self.lookup(node.base)
            return struct.get(node.name, None)
        return self.lookup(node.name)
    def visit_call(self, node):
        function = self.f_table[node.name]
        params = function["params"]
        body = function["body"]
        args = node.args or []
        self.v_tables.append({})
        for param, arg in zip(params, args):
            self.v_tables[-1][param] = self.visit(arg)
        try:
            for stmt in body:
                self.visit(stmt)
        except ReturnException as r:
            self.v_tables.pop()
            return r.value
        self.v_tables.pop()