from src.visitors.base_visitor import Visitor
from src.type_check import TypeCheckError

class TypeCheckerVisitor(Visitor):
    def __init__(self):
        self.code = code
        self.v_table = {}
        self.f_table = {}
        
    def is_numeric(self, t):
        return t in ["int", "float"]

    def numeric_result_type(self, node, left_type, right_type):
        # Makes sure both sides are numeric
        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            # raise TypeError(f"Expected numeric types, got {left_type} and {right_type}")
            raise TypeCheckError(
                # message,
                f"Expected numeric types, got {left_type} and {right_type}", # this is the value of message
                line=node.line,
                column=node.column,
                context=make_context(self.code, node.line, node.column)
            )
        if "float" in (left_type, right_type):
            return "float"
        return "int"

    def visit_var(self, node):
        if node.base is None:
            if node.name not in self.v_table:
                raise TypeError(f"The variable: '{node.name}' don't exist")
            return self.v_table[node.name]

        # Error, if the parrent (base) are not defined
        if node.base not in self.v_table:
            raise TypeError(f"The struct: '{node.base}' are not defined")
        
        # Check its parrent, if the variable 'name' are not inside of the struct (base)
        if node.name not in self.v_table[node.base]:
            parrent = self.v_table[node.base]["_parrent"]
                       
            while True:
                if node.name in self.v_table[parrent]: # Name found
                    return self.v_table[parrent][node.name]
                else:
                    # Error, If no parrent found
                    if "_parrent" not in self.v_table[parrent]:
                        raise TypeError(f"The variable: '{node.name}' are not defined in the struct: '{node.base}' or its parrent")
                    
                    # Save new parrent
                    parrent = self.v_table[parrent]["_parrent"]
        
        # Find and return the type of the 'name'
        return self.v_table[node.base][node.name]
        
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
        # Make sure no duplicate of variabels
        if node.name in self.v_table:
            # raise TypeError(f"The variable: '{node.name}' already exist")
            raise TypeCheckError(
                #message,
                f"The variable: '{node.name}' already exist",
                line=node.line,
                column=node.column,
                context=make_context(self.code, node.line, node.column)
            )
        
        # Set type to 'None' if it doesn't exist
        if node.value is None:
            self.v_table[node.name] = None
            return None

        # Save variable in v_table, with name and type
        value_type = self.visit(node.value)
        self.v_table[node.name] = value_type
        return value_type

    def visit_assign(self, node):
        # Check if assigning to a list index
        if type(node.name).__name__ == "IndexAccess":
            # Find the type of the index
            index_type = self.visit(node.name.index)
            if index_type != "int":
                raise TypeError(f"List index must be int, got {index_type}")

            # Find the type of the collection
            collection_type = self.visit(node.name.target)

            # Make sure the target is a list
            if not isinstance(collection_type, str) or not collection_type.startswith("list"):
                raise TypeError(f"Cannot index non-list type '{collection_type}'")

            # Find the element type inside the list
            if collection_type == "list":
                elem_type = None
            else:
                elem_type = collection_type[5:-1]  # list[int] -> int

            # Find the type of the assigned value
            value_type = self.visit(node.value)

            # If the list has a known element type, enforce it
            if elem_type is not None and value_type != elem_type:
                raise TypeError(
                    f"Cannot assign value of type '{value_type}' to list element of type '{elem_type}'"
                )
            return value_type

        # Check if it got inheritance
        if node.base:
            # Check if the parrent exist
            if node.base not in self.v_table:
                raise TypeError(f"The struct: '{node.base}' don't exist")
            
            # Check if the name exist
            base_type = self.v_table[node.base]
            if node.name not in base_type:
                parrent = self.v_table[node.base]["_parrent"]

                # Check its parrent's
                while True:
                    base_type = self.v_table[parrent]
                    if node.name in base_type:
                        break
                    else:
                        # Error, If no parrent found
                        if "_parrent" not in self.v_table[parrent]:
                            raise TypeError(f"The variable: '{node.name}' don't exist in the struct: '{node.base}', or its parrent")
                        
                        # Save new parrent
                        parrent = self.v_table[parrent]["_parrent"]
            
            # Save in the parrent's v_table and return the type 
            value_type = self.visit(node.value)
            base_type[node.name] = value_type
            return value_type
        
        # Check if the name exist
        if node.name not in self.v_table:   
            raise TypeError(f"The variable: '{node.name}' don't exist")
        
        # Save in v_table and return the type
        value_type = self.visit(node.value)
        self.v_table[node.name] = value_type
        return value_type

    def visit_return(self, node):
        return self.visit(node.value)
    
    def visit_define(self, node):
        # Check if fthe function are already defined
        if node.name in self.f_table:
            # raise TypeError(f"Function: '{node.name}' already exist")
            raise TypeCheckError(
                #message,
                f"Function: '{node.name}' already exist",
                line=node.line,
                column=node.column,
                context=make_context(self.code, node.line, node.column)
            )

        # Save data as 'params' and 'body' in functions
        self.f_table[node.name] = {
            "params": node.params,
            "body": node.body
        }

        return None
    
    def visit_call(self, node):
        # Check if the function are already definend, then get its data
        if node.name not in self.f_table:
            # raise TypeError(f"The function: '{node.name}' don't exist")
            raise TypeCheckError(
                #message,
                f"The function: '{node.name}' don't exist",
                line=node.line,
                column=node.column,
                context=make_context(self.code, node.line, node.column)
            )
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
        # Allow string concatenation
        if left_type == "str" and right_type == "str":
            return "str"

        # Otherwise, both sides must be numeric
        return self.numeric_result_type(node, left_type, right_type)
    
    def visit_sub(self, node):
        #both sides must be numeric
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        return self.numeric_result_type(node, left_type, right_type)
    
    def visit_mul(self, node):
        #both sides must be numeric
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        return self.numeric_result_type(node, left_type, right_type)
    
    def visit_div(self, node):
        #both sides must be numeric
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            # raise TypeError(f"Expected numeric types, got {left_type} and {right_type}")
            raise TypeCheckError(
                #message,
                f"Expected numeric types, got {left_type} and {right_type}",
                line=node.line,
                column=node.column,
                context=make_context(self.code, node.line, node.column)
            )

        #division always returns float
        return "float"
    
    def visit_pow(self, node):
        #both sides must be numeric
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        return self.numeric_result_type(node, left_type, right_type)

    # comparison operators
    def visit_equal_expr(self, node):
        #checks both sides of equality
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if not self.comparable_equality(left_type, right_type):
            # raise TypeError(f"Cannot compare {left_type} == {right_type}")
            raise TypeCheckError(
                #message,
                f"Cannot compare {left_type} == {right_type}",
                line=node.line,
                column=node.column,
                context=make_context(self.code, node.line, node.column)
            )

        return "bool"
    
    def visit_not_equal_expr(self, node):
        # Checks both sides of inequality
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if not self.comparable_equality(left_type, right_type):
            # raise TypeError(f"Cannot compare {left_type} != {right_type}")
            raise TypeCheckError(
                #message,
                f"Cannot compare {left_type} != {right_type}",
                line=node.line,
                column=node.column,
                context=make_context(self.code, node.line, node.column)
            )

        return "bool"

    def visit_greater_expr(self, node):
        # Checks both sides of greater than ">"
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if not self.comparable_ordered(left_type, right_type):
            # raise TypeError(f"Cannot compare {left_type} > {right_type}")
            raise TypeCheckError(
                #message,
                f"Cannot compare {left_type} > {right_type}",
                line=node.line,
                column=node.column,
                context=make_context(self.code, node.line, node.column)
            )

        return "bool"

    def visit_less_expr(self, node):
        #checks both sides of less than "<"
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if not self.comparable_ordered(left_type, right_type):
            # raise TypeError(f"Cannot compare {left_type} < {right_type}")
            raise TypeCheckError(
                #message,
                f"Cannot compare {left_type} > {right_type}",
                line=node.line,
                column=node.column,
                context=make_context(self.code, node.line, node.column)
            )

        return "bool"

    def visit_greater_equal_expr(self, node):
        # Checks both sides of greater than or equal ">="
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if not self.comparable_ordered(left_type, right_type):
            # raise TypeError(f"Cannot compare {left_type} >= {right_type}")
            raise TypeCheckError(
                #message,
                f"Cannot compare {left_type} >= {right_type}",
                line=node.line,
                column=node.column,
                context=make_context(self.code, node.line, node.column)
            )

        return "bool"

    def visit_less_equal_expr(self, node):
        # Checks both sides of less than or equal "<="
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if not self.comparable_ordered(left_type, right_type):
            # raise TypeError(f"Cannot compare {left_type} <= {right_type}")
            raise TypeCheckError(
                #message,
                f"Cannot compare {left_type} <= {right_type}",
                line=node.line,
                column=node.column,
                context=make_context(self.code, node.line, node.column)
            )

        return "bool"
    
    #boolean operators

    def visit_and_expr(self,node):
        # AND requires both sides to be bool
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if left_type != "bool" or right_type != "bool":
            # raise TypeError(f"AND requires bool, got {left_type} and {right_type}")
            raise TypeCheckError(
                #message,
                f"AND requires bool, got {left_type} and {right_type}",
                line=node.line,
                column=node.column,
                context=make_context(self.code, node.line, node.column)
            )

        return "bool"

    def visit_or_expr(self, node):
        # OR requires both sides to be bool
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if left_type != "bool" or right_type != "bool":
            # raise TypeError(f"OR requires bool, got {left_type} and {right_type}")
            raise TypeCheckError(
                #message,
                f"OR requires bool, got {left_type} and {right_type}",
                line=node.line,
                column=node.column,
                context=make_context(self.code, node.line, node.column)
            )

        return "bool"

    def visit_not_expr(self, node):
        # NOT requires a single bool operand
        value_type = self.visit(node.cond)

        if value_type != "bool":
            # raise TypeError(f"NOT requires bool, got {value_type}")
            raise TypeCheckError(
                #message,
                f"NOT requires bool, got {value_type}",
                line=node.line,
                column=node.column,
                context=make_context(self.code, node.line, node.column)
            )

        return "bool"

    def visit_xor_expr(self, node):
        # XOR requires both sides to be bool
        left_type = self.visit(node.cond)
        right_type = self.visit(node.cond2)

        if left_type != "bool" or right_type != "bool":
            # raise TypeError(f"XOR requires bool, got {left_type} and {right_type}")
            raise TypeCheckError(
                #message,
                f"XOR requires bool, got {left_type} and {right_type}",
                line=node.line,
                column=node.column,
                context=make_context(self.code, node.line, node.column)
            )

        return "bool"

    def visit_between(self, node):
        # Between requires numeric values
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            # raise TypeError(f"between requires numeric types, got {left_type} and {right_type}")
            raise TypeCheckError(
                #message,
                f"between requires numeric types, got {left_type} and {right_type}",
                line=node.line,
                column=node.column,
                context=make_context(self.code, node.line, node.column)
            )

        return "bool"

    def visit_chance(self, node):
        # Chance requires numeric values
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(f"chance requires numeric types, got {left_type} and {right_type}")
        return "bool"

    def visit_if(self, node):
        # condition must be a bool
        cond_type = self.visit(node.cond)

        if cond_type is None:
            return None
        if cond_type != "bool":
            raise TypeError(f"if condition must be bool, got {cond_type}")

        # Checks statements inside if body
        for stmt in node.body:
            self.visit(stmt)

        # Checks statements inside else body
        if node.elses:
            for stmt in node.elses:
                self.visit(stmt)

        # Checks all elif branches
        if node.elifs:
            for cond, body in node.elifs:
                cond_type = self.visit(cond)
                if cond_type != "bool":
                    raise TypeError(f"elif condition must be bool, got {cond_type}")
                for stmt in body:
                    self.visit(stmt)
        return None

    def visit_while(self, node):
        cond_type = self.visit(node.cond)

        if cond_type != "bool":
            raise TypeError(f"while condition must be bool, got {cond_type}")
        # saves current scope
        old = self.v_table.copy()

        # Checks all statements inside loop body
        for stmt in node.body:
            self.visit(stmt)

        #restore previous scope
        self.v_table = old

        return None

    def visit_dowhile(self, node):
        # Saves current scope
        old = self.v_table.copy()
        # Checks body
        for stmt in node.body:
            self.visit(stmt)
        # Restore previous scope
        self.v_table = old

        # check condition
        cond_type = self.visit(node.cond)
        if cond_type != "bool":
            raise TypeError(f"dowhile condition must be bool, got {cond_type}")

        return None

    def visit_create_list(self, node):
        # List name must be unique
        if node.name in self.v_table:
            raise TypeError(f"The variable: '{node.name}' already exist")

        # Empty list gets generic list type
        if node.listing is None:
            self.v_table[node.name] = "list"
            return "list"

        element_types = []

        # Finds type of each list element
        for item in node.listing:
            t = self.visit(item)
            element_types.append(t)

        # enforce same type
        if len(set(element_types)) > 1:
            raise TypeError(f"List '{node.name}' has mixed types: {element_types}")

        # Creates typed list, for example list[int]
        list_type = f"list[{element_types[0]}]" if element_types else "list"

        self.v_table[node.name] = list_type
        return list_type

    def visit_index_access(self, node):
        index_type = self.visit(node.index)
        if index_type != "int":
            raise TypeError(f"List index must be int, got {index_type}")

        target_type = self.visit(node.target)

        if not isinstance(target_type, str) or not target_type.startswith("list"):
            raise TypeError(f"Cannot index non-list type '{target_type}'")

        if target_type == "list":
            return None

        return target_type[5:-1]   # list[int] -> int

    def visit_forrange(self, node):
        # Range start and end must be numeric
        start_type = self.visit(node.start)
        end_type = self.visit(node.end)

        if not self.is_numeric(start_type) or not self.is_numeric(end_type):
            raise TypeError(f"for-range bounds must be numeric, got {start_type} and {end_type}")

        # Saves old scope and creates loop variable
        old = self.v_table.copy()
        self.v_table[node.name] = "int"

        # Checks all statements inside loop body once
        for stmt in node.body:
            self.visit(stmt)

        # Restore previous scope
        self.v_table = old
        return None

    def visit_foreach(self, node):
        # List to iterate over must exist
        if node.collection not in self.v_table:
            raise TypeError(f"The variable: '{node.collection}' don't exist")

        collection_type = self.v_table[node.collection]

        # Only lists can be used in foreach
        if not isinstance(collection_type, str) or not collection_type.startswith("list"):
            raise TypeError(f"Cannot iterate over non-list type '{collection_type}'")
        # Finds the type of one element inside the list
        if collection_type == "list":
            elem_type = None
        else:
            elem_type = collection_type[5:-1]  # list[int] → int

        # Saves old scope and creates loop variable
        old = self.v_table.copy()
        self.v_table[node.name] = elem_type

        # Checks all statements inside loop body once
        for stmt in node.body:
            self.visit(stmt)

        # Restores previous scope
        self.v_table = old
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
    
    def visit_create_struct(self, node):
        # Error, if the 'name' already exist
        if node.name in self.v_table:
            raise TypeError(f"The struct: '{node.name}' already exist")
        
        elif node.base in self.v_table:
            # Merge with the parrent (base)
            merged = {"_parrent": node.base}

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