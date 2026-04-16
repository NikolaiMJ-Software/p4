from src.visitors.base_visitor import Visitor

class TypeCheckerVisitor(Visitor):
    def __init__(self):
        self.v_table = {}
        self.f_table = {}
        
    def is_numeric(self, t):
        return t in ["int", "float"]

    def numeric_result_type(self, node, left_type, right_type):
        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(f"Expected numeric types, got {left_type} and {right_type}")

        if "float" in (left_type, right_type):
            return "float"
        return "int"

    def comparable_ordered(self, left_type, right_type):
        # for <, >, <=, >=
        return self.is_numeric(left_type) and self.is_numeric(right_type)

    def comparable_equality(self, left_type, right_type):
        # fpr ==, !=
        if left_type == right_type:
            return True
        if self.is_numeric(left_type) and self.is_numeric(right_type):
            return True
        
        return False

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
    
    def visit_create_variable(self, node):
        if node.name in self.v_table:
            raise TypeError(f"The variable: '{node.name}' already exist")
        
        if node.value is None:
            self.v_table[node.name] = None
            return None

        value_type = self.visit(node.value)
        self.v_table[node.name] = value_type
        return value_type
    
    def visit_assign(self, node):
        if node.base:
            if node.base not in self.v_table:
                raise TypeError(f"The struct: '{node.base}' don't exist")
            
            base_type = self.v_table[node.base]
            if node.name not in base_type:
                raise TypeError(f"The variable: '{node.name}' don't exist in the struct: '{node.base}'")
            
            value_type = self.visit(node.value)
            base_type[node.name] = value_type
            return value_type
        
        if node.name not in self.v_table:   
            raise TypeError(f"The variable: '{node.name}' don't exist")
        
        value_type = self.visit(node.value)
        self.v_table[node.name] = value_type
        return value_type
    
    def visit_return(self, node):
        if node.value in self.v_table:
            return self.visit(node.value)
        raise TypeError(f"The variable: '{node.value}' don't exist")
    
    def visit_define(self, node):
        # Check if fthe function are already defined
        if node.name in self.f_table:
            raise TypeError(f"Function: '{node.name}' already exist")

        # Save data as 'params' and 'body' in functions
        self.f_table[node.name] = {
            "params": node.params,
            "body": node.body
        }

        return None
    
    def visit_call(self, node):
        # Check if the function are already definend, then get its data
        if node.name not in self.f_table:
            raise TypeError(f"The function: '{node.name}' don't exist")
        func = self.f_table[node.name]
        
        # Update the local variable types
        local_vars = {}
        for p, arg in zip(func["params"], node.args):
            local_vars[p] = self.visit(arg)
        
        # Temperary switch scope
        old = self.v_table
        self.v_table = local_vars

        # Typecheck the function
        return_type = None
        from src.ast.nodes import Return
        for stmt in func["body"]:
            t = self.visit(stmt)
            if isinstance(stmt, Return):
                return_type = t

        # Restore old scope
        self.v_table = old

        return return_type
    
    def visit_add(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type == "str" and right_type == "str":
            return "str"

        return self.numeric_result_type(node, left_type, right_type)
    
    def visit_sub(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        return self.numeric_result_type(node, left_type, right_type)
    
    def visit_mul(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        return self.numeric_result_type(node, left_type, right_type)
    
    def visit_div(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(f"Expected numeric types, got {left_type} and {right_type}")

        return "float"
    
    def visit_pow(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        return self.numeric_result_type(node, left_type, right_type)

    # comparison operators
    def visit_equal_expr(self, node):
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if not self.comparable_equality(left_type, right_type):
            raise TypeError(f"Cannot compare {left_type} == {right_type}")

        return "bool"
    
    def visit_not_equal_expr(self, node):
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if not self.comparable_equality(left_type, right_type):
            raise TypeError(f"Cannot compare {left_type} != {right_type}")

        return "bool"

    def visit_greater_expr(self, node):
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if not self.comparable_ordered(left_type, right_type):
            raise TypeError(f"Cannot compare {left_type} > {right_type}")

        return "bool"

    def visit_less_expr(self, node):
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if not self.comparable_ordered(left_type, right_type):
            raise TypeError(f"Cannot compare {left_type} < {right_type}")

        return "bool"

    def visit_greater_equal_expr(self, node):
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if not self.comparable_ordered(left_type, right_type):
            raise TypeError(f"Cannot compare {left_type} >= {right_type}")

        return "bool"

    def visit_less_equal_expr(self, node):
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if not self.comparable_ordered(left_type, right_type):
            raise TypeError(f"Cannot compare {left_type} <= {right_type}")

        return "bool"
    
    #boolean operators

    def visit_and_expr(self,node):
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if left_type != "bool" or right_type != "bool":
            raise TypeError(f"AND requires bool, got {left_type} and {right_type}")

        return "bool"

    def visit_or_expr(self, node):
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if left_type != "bool" or right_type != "bool":
            raise TypeError(f"OR requires bool, got {left_type} and {right_type}")

        return "bool"

    def visit_not_expr(self, node):
        value_type = self.visit(node.cond)

        if value_type != "bool":
            raise TypeError(f"NOT requires bool, got {value_type}")

        return "bool"

    def visit_xor_expr(self, node):
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if left_type != "bool" or right_type != "bool":
            raise TypeError(f"XOR requires bool, got {left_type} and {right_type}")

        return "bool"

    def visit_between(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(f"between requires numeric types, got {left_type} and {right_type}")

        return "bool"

    def visit_chance(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(f"chance requires numeric types, got {left_type} and {right_type}")
        return "bool"

    def visit_if(self, node):
        cond_type = self.visit(node.cond)

        if cond_type is None:
            return None
        if cond_type != "bool":
            raise TypeError(f"if condition must be bool, got {cond_type}")

        for stmt in node.body:
            self.visit(stmt)

        if node.else_body is not None:
            for stmt in node.else_body:
                self.visit(stmt)
        return None
    
    def visit_input(self, node):
        # Make sure the value are define before writing to it
        if node.name in self.v_table:
            return self.visit(node.name)
        raise TypeError(f"The variable: '{node.name}' don't exist")
    
    def visit_output(self, node):
        # Make sure the value are define before writing to it
        if node.name in self.v_table:
            return self.visit(node.name)
        raise TypeError(f"The variable: '{node.name}' don't exist")
    
    def visit_var(self, node):
        # Error, if the parrent (base) are not defined
        if node.base not in self.v_table:
            raise TypeError(f"The struct: '{node.base}' are not defined")
        
        # Error, if the variable 'name' are not inside of the parrent (base)
        if node.name not in self.v_table[node.base]:
            raise TypeError(f"The variable: '{node.name}' are not defined in the struct: '{node.base}'")
        
        # Find and return the type of the 'name'
        return self.v_table[node.base][node.name]
    
    def visit_create_struct(self, node):
        # Error, if the 'name' already exist
        if node.name in self.v_table:
            raise TypeError(f"The struct: '{node.name}' already exist")
        
        elif node.base in self.v_table:
            # Merge with the parrent (base)
            merged = {}
            
            # Base first
            for name, typeof in self.v_table[node.base].items():
                merged[name] = typeof

            # Afterwards fields (overwrite)
            for f in node.fields:
                if type(f.value).__name__ != "NoneType": # Check if it's not a 'None' type
                    merged[f.name] = self.visit(f.value)
                else:
                    merged[f.name] = None

            # Update v_table
            self.v_table[node.name] = merged
            
        elif node.base is None:
            # Create new struct, if no parrent (base) are defined 
            res = {}
            for f in node.fields:
                if type(f.value).__name__ != "NoneType": # Check if it's not a 'None' type
                    res[f.name] = self.visit(f.value)
                else:
                    res[f.name] = None
            
            # Update v_table
            self.v_table[node.name] = res
            
        else:
            # Error, for no parrent
            raise TypeError(f"The parrent struct: '{node.base}' don't exist")