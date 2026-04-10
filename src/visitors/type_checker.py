from src.visitors.base_visitor import Visitor

class TypeCheckerVisitor(Visitor):
    def __init__(self):
        self.symbols = {}
        
    def visit_int_literal(self, node):
        return "int"
    
    def visit_string_literal(self, node):
        return "str"

    def visit_add(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type != "int" or right_type != "int":
            raise TypeError("Cannot add non-integers")

        return "int"
    
        
    def visit_expression(self, node):
        return self.visit(node.value)
    
    def visit_create_v(self, node):
        if node.value is None:
            self.symbols[node.name] = None
            return None

        value_type = self.visit(node.value)
        self.symbols[node.name] = value_type
        return value_type