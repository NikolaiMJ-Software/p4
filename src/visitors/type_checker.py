from src.visitors.base_visitor import Visitor

class TypeCheckerVisitor(Visitor):
    def __init__(self):
        self.symbols = {}
        
    def is_numeric(self, t):
        return t in ["int", "float"]

    def numeric_result_type(self, left_type, right_type):
        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(f"Expected numeric types, got {left_type} and {right_type}")

        if "float" in (left_type, right_type):
            return "float"
        return "int"

    def visit_int_literal(self, node):
        return "int"
    
    def visit_string_literal(self, node):
        return "str"
    
    def visit_float_literal(self, node):
        return "float"
    
    def visit_bool_literal(self, node):
        return "bool"

    def visit_expression(self, node):
        return self.visit(node.value)
    
    def visit_create_v(self, node):
        if node.value is None:
            self.symbols[node.name] = None
            return None

        value_type = self.visit(node.value)
        self.symbols[node.name] = value_type
        return value_type
    
    def visit_add(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        #if left_type != "int" or right_type != "int":
            #raise TypeError("Cannot add non-integers")

        return self.numeric_result_type(left_type, right_type)
    
    def visit_min(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        #if left_type != "int" or right_type != "int":
            #raise TypeError("Cannot add non-integers")

        return self.numeric_result_type(left_type, right_type)
    
    def visit_mul(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        #if left_type != "int" or right_type != "int":
            #raise TypeError("Cannot add non-integers")

        return self.numeric_result_type(left_type, right_type)
    
    def visit_div(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(f"Expected numeric types, got {left_type} and {right_type}")

        return "float"
    
    def visit_pow(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        #if left_type != "int" or right_type != "int":
            #raise TypeError("Cannot add non-integers")

        return self.numeric_result_type(left_type, right_type)    