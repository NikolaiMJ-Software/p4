from src.visitors.base_visitor import Visitor
from src.errors import Error
from src.ast.nodes import Return, Var 
from src.errors import TypeError

class TypeCheckerVisitor(Visitor):
    def __init__(self, code=""):
        self.code = code
        self.v_table = {}
        self.f_table = {}
    
    def lookup_var(self, name):
        scope = self.v_table

        while scope:
            if name in scope:
                return scope[name]
            scope = scope.get("__parent__")
        return False

    def is_numeric(self, t):
        return t in ["int", "float"]

    def numeric_result_type(self, node, left_type, right_type):
        # Makes sure both sides are numeric
        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(
                self.code,
                node,
                f"Expected numeric types, got {left_type} and {right_type}"
            )
        if "float" in (left_type, right_type):
            return "float"
        return "int"

    def visit_var(self, node):
        if node.base is None:
            var_type = self.lookup_var(node.name)
            if var_type is False:
                raise TypeError(
                    self.code,
                    node,
                    f"The variable: '{node.name}' does not exist"
                )
            return var_type

        # Error, if the parent (base) is not defined
        if self.lookup_var(node.base) is False:
            raise TypeError(
                self.code,
                node,
                f"The struct: '{node.base}' is not defined"
            )
        
        # Error, if the variable 'name' are not inside of the struct (base)
        if node.name not in self.v_table[node.base]:
            raise TypeError(
                self.code,
                node,
                f"The variable: '{node.name}' is not defined in the struct: '{node.base}'"
            )
        
        # Find and return the type of the 'name'
        return self.v_table[node.base][node.name]
        
    def comparable_ordered(self, left_type, right_type):
        # for <, >, <=, >=
        return self.is_numeric(left_type) and self.is_numeric(right_type)

    def comparable_equality(self, left_type, right_type):
        # for ==, !=
        if left_type == right_type:
            return True
        if self.is_numeric(left_type) and self.is_numeric(right_type):
            return True
        
        return False
    
    def validate_game_name(self, node, type_type):
        #check if we are dealing with and ID game
        if node.name != "Game":
            return
        #if game is not a struct sent back an error
        if type_type != "struct":
            raise TypeError(
                self.code,
                node,
                "The identifier 'Game' is reserved and can only be used as a struct name."
            )

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
    
    def visit_break(self, node):
        return None
    
    def visit_neg(self, node):
        value_type = self.visit(node.value)

        if not self.is_numeric(value_type):
            raise TypeError(
                self.code,
                node,
                f"NEG requires numeric type, got {value_type}"
            )

        return value_type
    
    def visit_create_variable(self, node):
        
        self.validate_game_name(node, "variable")
        
        # Make sure no duplicate of variabels
        if self.lookup_var(node.name) != False:
            raise TypeError(
                self.code,
                node,
                f"The variable: '{node.name}' already exists"
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
        # Check if it got inheritance
        if node.base:
            # Check if the parent exist
            if self.lookup_var(node.base) is False:
                raise TypeError(
                    self.code,
                    node,
                    f"The struct: '{node.base}' does not exist"
                )
            
            # Check if the name exist
            base_type = self.v_table[node.base]
            if node.name not in base_type:
                raise TypeError(
                    self.code,
                    node,
                    f"The variable: '{node.name}' does not exist in the struct: '{node.base}'"
                )
            
            # Save in the struct's v_table and return the type 
            value_type = self.visit(node.value)
            base_type[node.name] = value_type
            return value_type
        
        # Check if the name exist
        if self.lookup_var(node.name) is False:
            raise TypeError(
                self.code,
                node,
                f"The variable: '{node.name}' does not exist"
            )
        
        # Save in v_table and return the type
        value_type = self.visit(node.value)
        table = self.v_table
        while node.name not in table:
            table = table.get("__parent__")
        table[node.name] = value_type
        return value_type

    def visit_assign_index(self, node):
        # Check if target node exist
        self.visit(node.target)

        # Get the list and index
        target = node.target
        v_table = self.v_table[target.base] if target.base else self.v_table
        
        target_list = v_table[target.target]
        index = target.indexing[0].value
        
        # Save type in the list
        var_type = self.visit(node.value)
        target_list[index] = var_type
        return var_type

    def visit_return(self, node):
        return self.visit(node.value)
    
    def visit_define(self, node):
        self.validate_game_name(node, "function")
        
        # Check if fthe function are already defined
        if node.name in self.f_table:
            raise TypeError(
                self.code,
                node,
                f"Function: '{node.name}' already exists"
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
            raise TypeError(
                self.code,
                node,
                f"The function: '{node.name}' does not exist"
            )

        func = self.f_table[node.name]

        # validate argument counts
        if len(func["params"]) != len(node.args):
            raise TypeError(
                self.code,
                node,
                f"Function '{node.name}' expects {len(func['params'])} args, got {len(node.args)}"
            )
        
        # Update the local variable types
        local_vars = {}
        for p, arg in zip(func["params"], node.args):
            local_vars[p] = self.visit(arg)
        
        # Temperary switch scope
        new_scope = {
            "__parent__": self.v_table,
            **local_vars
        }
        old = self.v_table.copy()
        self.v_table = new_scope

        # Typecheck the function
        return_type = None
        for stmt in func["body"]:
            t = self.visit(stmt)
            if isinstance(stmt, Return):
                return_type = t

        # Restore old scope
        self.v_table = {**old, **self.v_table["__parent__"]}

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
            raise TypeError(
                self.code,
                node,
                f"Expected numeric types, got {left_type} and {right_type}"
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
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if not self.comparable_equality(left_type, right_type):
            raise TypeError(
                self.code,
                node,
                f"Cannot compare {left_type} == {right_type}"
            )

        return "bool"
    
    def visit_not_equal_expr(self, node):
        # Checks both sides of inequality
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if not self.comparable_equality(left_type, right_type):
            raise TypeError(
                self.code,
                node,
                f"Cannot compare {left_type} != {right_type}"
            )

        return "bool"

    def visit_greater_expr(self, node):
        # Checks both sides of greater than ">"
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if not self.comparable_ordered(left_type, right_type):
            raise TypeError(
                self.code,
                node,
                f"Cannot compare {left_type} > {right_type}"
            )

        return "bool"

    def visit_less_expr(self, node):
        #checks both sides of less than "<"
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if not self.comparable_ordered(left_type, right_type):
            raise TypeError(
                self.code,
                node,
                f"Cannot compare {left_type} < {right_type}"
            )

        return "bool"

    def visit_greater_equal_expr(self, node):
        # Checks both sides of greater than or equal ">="
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if not self.comparable_ordered(left_type, right_type):
            raise TypeError(
                self.code,
                node,
                f"Cannot compare {left_type} >= {right_type}"
            )

        return "bool"

    def visit_less_equal_expr(self, node):
        # Checks both sides of less than or equal "<="
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if not self.comparable_ordered(left_type, right_type):
            raise TypeError(
                self.code,
                node,
                f"Cannot compare {left_type} <= {right_type}"
            )

        return "bool"
    
    #boolean operators

    def visit_and_expr(self,node):
        # AND requires both sides to be bool
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type != "bool" or right_type != "bool":
            raise TypeError(
                self.code,
                node,
                f"AND requires bool, got {left_type} and {right_type}"
            )

        return "bool"

    def visit_or_expr(self, node):
        # OR requires both sides to be bool
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type != "bool" or right_type != "bool":
            raise TypeError(
                self.code,
                node,
                f"OR requires bool, got {left_type} and {right_type}"
            )

        return "bool"

    def visit_not_expr(self, node):
        # NOT requires a single bool operand
        value_type = self.visit(node.cond)

        if value_type != "bool":
            raise TypeError(
                self.code,
                node,
                f"NOT requires bool, got {value_type}"
            )

        return "bool"

    def visit_xor_expr(self, node):
        # XOR requires both sides to be bool
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type != "bool" or right_type != "bool":
            raise TypeError(
                self.code,
                node,
                f"XOR requires bool, got {left_type} and {right_type}"
            )

        return "bool"

    def visit_between(self, node):
        # Between requires numeric values
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(
                self.code,
                node,
                f"between requires numeric types, got {left_type} and {right_type}"
            )

        return "bool"

    def visit_chance(self, node):
        # Chance requires numeric values
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(
                self.code,
                node,
                f"chance requires numeric types, got {left_type} and {right_type}"
            )
        return "bool"

    def visit_if(self, node):
        # leftition must be a bool
        left_type = self.visit(node.cond)

        if left_type is None:
            return None
        if left_type != "bool":
            raise TypeError(
                self.code,
                node,
                f"if condition must be bool, got {left_type}"
            )

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
                    raise TypeError(
                        self.code,
                        node,
                        f"elif condition must be bool, got {cond_type}"
                    )
                for stmt in body:
                    self.visit(stmt)
        return None

    def visit_while(self, node):
        cond_type = self.visit(node.cond)

        if cond_type != "bool":
            raise TypeError(
                self.code,
                node,
                f"while condition must be bool, got {cond_type}"
            )
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
            raise TypeError(
                self.code,
                node,
                f"dowhile condition must be bool, got {cond_type}"
            )

        return None

    def visit_create_list(self, node):
        self.validate_game_name(node, "list")

        if self.lookup_var(node.name) != False:
            raise TypeError(
                self.code,
                node,
                f"The list: '{node.name}' already exists"
            )

        # Empty list gets generic list type
        if node.value is None:
            self.v_table[node.name] = []
            return []

        element_types = []

        # Finds type of each list element
        for item in node.value:
            t = self.visit(item)
            element_types.append(t)

        self.v_table[node.name] = element_types
        return element_types


    def visit_index_access(self, node):
        # Make sure the index is a 'int'
        index_type = self.visit(node.indexing[0])
        if index_type != "int":
            raise TypeError(
                self.code,
                node,
                f"List index must be int, got {index_type}"
            )
        
        # Check if the list is in a struct
        v_table = self.v_table
        if node.base:
            if self.lookup_var(node.base) is False:
                raise TypeError(
                    self.code,
                    node,
                    f"The struct: '{node.base}' is not defined"
                )
            else:
                v_table = self.v_table[node.base]

        # Check if the list exist in v_table
        if node.target not in v_table:
            raise TypeError(
                self.code,
                node,
                f"The list: '{node.target}' does not exist"
            )
        
        # Make sure it's a list
        target_list = v_table[node.target]
        if not isinstance(target_list, list):
            raise TypeError(
                self.code,
                node,
                f"The variable: '{node.target}' in not a list"
            )

        # Make sure the index is eather positive or negative
        index = node.indexing[0].value
        if not isinstance(index, int):
            index = -index.value

        # Check if the index are out of bound
        if 0 <= index and index <= len(target_list) - 1:
            return target_list[index]
        else:
            raise TypeError(
                self.code,
                node,
                f"The index: '{index}' does not exist in '{node.target}'"
            )


    def visit_forrange(self, node):
        # Range start and end must be numeric
        start_type = self.visit(node.start)
        end_type = self.visit(node.end)

        if not self.is_numeric(start_type) or not self.is_numeric(end_type):
            raise TypeError(
                self.code,
                node,
                f"for-range bounds must be numeric, got {start_type} and {end_type}"
            )

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
        if self.lookup_var(node.collection) is False:
            raise TypeError(
                self.code,
                node,
                f"The list: '{node.collection}' does not exist"
            )

        collection_type = self.v_table[node.collection]

        # Only lists can be used in foreach
        if not isinstance(collection_type, list):
            raise TypeError(
                self.code,
                node,f"Cannot iterate over non-list type '{collection_type}'"
            )
        
        # Saves old scope
        old = self.v_table.copy()
        
        # Checks all statements inside loop body once
        for item in collection_type:
            old = self.v_table.copy()
            self.v_table[node.name] = item
            for stmt in node.body:
                self.visit(stmt)
            self.v_table = old

        # Restores previous scope
        self.v_table = old
        return None
        
    def visit_input(self, node):
        # Make sure the value are define before writing to it
        var_type = self.lookup_var(node.name)
        if var_type != False:
            return var_type
        raise TypeError(
                self.code,
                node,
                f"The variable: '{node.name}' does not exist"
            )
    
    def visit_output(self, node):
        # Go thru each output value
        for each in node.value:
            if isinstance(each, Var):
                # Find the correct table (from a struct or not)
                table = self.v_table[each.base] if each.base else self.v_table
                if each.name not in table:
                    raise TypeError(
                        self.code,
                        node,
                        f"The variable: '{each.name}' does not exist"
                    )
    
    def visit_create_struct(self, node):
        self.validate_game_name(node, "struct")
        
        # Error, if the 'name' already exist
        if self.lookup_var(node.name) != False:
            raise TypeError(
                self.code,
                node,
                f"The struct: '{node.name}' already exists"
            )
        
        elif self.lookup_var(node.base) != False:
            # Copy the parrent (base)
            merged = self.v_table[node.base].copy()

            # Afterwards fields (overwrite)
            for f in node.fields:
                if f.value is not None: # Check if it's not a 'None' type
                    merged[f.name] = self.visit(f.value)
                else:
                    merged[f.name] = None

            # Update v_table
            self.v_table[node.name] = merged
            
        elif node.base is None:
            # Create new struct, if no parent (base) are defined 
            res = {}
            for f in node.fields:
                if f.value is not None: # Check if it's not a 'None' type
                    res[f.name] = self.visit(f.value)
                else:
                    res[f.name] = None
            
            # Update v_table
            self.v_table[node.name] = res
            
        else:
            # Error, for no parent
            raise TypeError(
                self.code,
                node,
                f"The parent struct: '{node.base}' does not exist"
            )