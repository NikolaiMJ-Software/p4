from src.visitors.base_visitor import Visitor
from src.ast.nodes import *
from ..runtime.game_state import GameStateManager
import random

class ReturnException(Exception): # exception raised by return() to stop function call
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class InterpreterVisitor(Visitor):
    def __init__(self, slot=1):
        self.v_tables = [{}] # list of variables split into scope levels
        self.f_table = {} # list of defined functions
        self.game_state_manager = GameStateManager(slot) # safe state manager, where slot equals save file
    
    
    
    # SCOPE HANDLING
    def lookup(self, name): # goes through scopes to find variable
        for v_table in reversed(self.v_tables):
            if name in v_table:
                return v_table[name]
        return None
    
    def find_scope(self, name): # goes through scopes to find scope level of variable
        for scope in reversed(self.v_tables):
            if name in scope:
                return scope
        return None
    
    # Game state handling
    def load_game_state(self):
        loaded_game = self.game_state_manager.load()
        if loaded_game is not None and "Game" in self.v_tables[0]:
            self.v_tables[0]["Game"] = loaded_game
    
    def save_game_state(self):
        game = self.v_tables[0].get("Game")
        if game is not None:
            self.game_state_manager.save(game)
    
    def run(self, ast, args=None):
        try:
            for stmt in ast:
                self.visit(stmt)

            self.load_game_state()

            if "Play" in self.f_table:
                self.visit(Call("Play", args or []))

        except KeyboardInterrupt:
            print("\nProgram interrupted. Saving game state...")

        finally:
            self.save_game_state()
    
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
    def visit_create_variable(self, node):
        value = self.visit(node.value) if node.value else "UNINITIALIZED"
        self.v_tables[-1][node.name] = value
        
    def visit_create_struct(self, node):
        parent = self.lookup(node.base)
        fields = {field.name: self.visit(field.value) if field.value else "UNINITIALIZED" for field in node.fields}
        if parent == None:
            self.v_tables[-1][node.name] = fields
        else:
            self.v_tables[-1][node.name] = {**parent, **fields}
        
    def visit_create_list(self, node):
        listing = [self.visit(item) for item in node.listing] if node.listing else []
        self.v_tables[-1][node.name] = listing
        
    def visit_assign(self, node):
        value = self.visit(node.value)
        if node.base: # handles inheritance
            struct = self.lookup(node.base)
            struct[node.name] = value
            return
        scope = self.find_scope(node.name)
        scope[node.name] = value
        
    def visit_if(self, node):
        if self.visit(node.cond): # original if-statement
            self.v_tables.append({}) # start scope
            for stmt in node.body:
                self.visit(stmt)
            self.v_tables.pop() # end scope
            return
        for elifs in node.elifs: # loop all else-ifs
            if self.visit(elifs[0]): # else-if condition
                self.v_tables.append({}) # start scope
                for stmt in elifs[1]:
                    self.visit(stmt)
                self.v_tables.pop() # end scope
                return
        if node.elses: # else
            self.v_tables.append({}) # start scope
            for stmt in node.elses:
                self.visit(stmt)
            self.v_tables.pop() # end scope
                
    def visit_while(self, node):
        while self.visit(node.cond):
            try:
                for stmt in node.body:
                    self.visit(stmt)
            except BreakException:
                break
                
    def visit_dowhile(self, node):
        while True:
            try:
                for stmt in node.body:
                    self.visit(stmt)
            except BreakException:
                break
            
            if not self.visit(node.cond):
                break
            
    def visit_forrange(self, node):
        for i in range(self.visit(node.start), self.visit(node.end) + 1):
            self.v_tables.append({}) # start scope
            self.v_tables[-1][node.name] = i
            try:
                for stmt in node.body:
                    self.visit(stmt)
            except BreakException:
                break
            finally:
                self.v_tables.pop() # end scope
    
    def visit_foreach(self, node):
        collection = self.lookup(node.collection)
        for item in collection:
            self.v_tables.append({}) # start scope
            self.v_tables[-1][node.name] = item
            try:
                for stmt in node.body:
                    self.visit(stmt)
            except BreakException:
                break
            finally:
                self.v_tables.pop() # end scope
    
    
    def visit_define(self, node):
        self.f_table[node.name] = {
            "params" : node.params,
            "body" : node.body
        }
        
    def visit_return(self, node):
        value = self.visit(node.value)
        raise ReturnException(value)

    def visit_break(self, node):
        raise BreakException()
    
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
        self.v_tables.append({}) # start scope
        for param, arg in zip(params, args):
            self.v_tables[-1][param] = self.visit(arg) # tie defined function values to those described on call
        try:
            for stmt in body:
                self.visit(stmt)
        except ReturnException as r: # end function if return statement met
            self.v_tables.pop() # end scope
            return r.value
        self.v_tables.pop() # end scope