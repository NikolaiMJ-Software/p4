from src.visitors.base_visitor import Visitor
from src.errors import Error
from src.ast.nodes import Return, Var 
from src.errors import TypeError

class TypeChecker:
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
    
    def lookup_fun(self, name):
        scope = self.f_table

        while scope:
            if name in scope:
                return scope[name]
            scope = scope.get("__parent__")
        return False

    def is_numeric(self, t):
        return t in ["int", "float"]

    def numeric_result_type(self, node, symbol, left_type, right_type):
        # Makes sure both sides are numeric
        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(
                self.code,
                node,
                f"Expected numeric types on operation: {symbol}, got '{left_type}' and '{right_type}'"
            )
        if "float" in (left_type, right_type):
            return "float"
        return "int"

    def check_var(self, node, value):
        if node.base is None:
            if value is False:
                raise TypeError(
                    self.code,
                    node,
                    f"The variable: '{node.name}' does not exist"
                )
            return

        # Error, if the parent (base) is not defined
        if value is False:
            raise TypeError(
                self.code,
                node,
                f"The struct: '{node.base}' is not defined"
            )

        # Error, if the variable 'name' are not inside of the struct (base)
        if not isinstance(value, dict) or node.name not in value:
            raise TypeError(
                self.code,
                node,
                f"The variable: '{node.name}' is not defined in the struct: '{node.base}'"
            )

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

    def check_neg(self, node, value_type):
        if not self.is_numeric(value_type):
            raise TypeError(
                self.code,
                node,
                f"NEG requires numeric type, got {value_type}"
            )

        return value_type

    def check_create_variable(self, node, already_exists):
        self.validate_game_name(node, "variable")

        # Make sure no duplicate of variabels
        if already_exists:
            raise TypeError(
                self.code,
                node,
                f"The variable: '{node.name}' already exists"
            )

    def check_assign(self, node, target):
        # Check if it got inheritance
        if node.base:
            # Check if the parent exist
            if target is False:
                raise TypeError(
                    self.code,
                    node,
                    f"The struct: '{node.base}' does not exist"
                )

            # Check if the name exist
            if not isinstance(target, dict) or node.name not in target:
                raise TypeError(
                    self.code,
                    node,
                    f"The variable: '{node.name}' does not exist in the struct: '{node.base}'"
                )

            return

        # Check if the name exist
        if target is None:
            raise TypeError(
                self.code,
                node,
                f"The variable: '{node.name}' does not exist"
            )

    def visit_assign_index(self, node):
        # Check if target exists and is indexable
        self.visit(node.target)

        target = node.target
        target_list = self.lookup_var(target.base)[target.target] if target.base else self.lookup_var(target.target)

        # Nested indexes are stored backwards in the AST, so flip them first
        indexes = target.indexing[::-1]

        # Move through nested lists until the final index
        for i in indexes[:-1]:
            index_type = self.visit(i)

            if index_type != "int":
                raise TypeError(
                    self.code,
                    node,
                    f"List index must be int, got {index_type}"
                )

            # Dynamic index, so the exact element cannot be resolved during type checking
            if not hasattr(i, "value"):
                return self.visit(node.value)

            target_list = target_list[i.value]

        var_type = self.visit(node.value)

        final_index = indexes[-1]
        final_index_type = self.visit(final_index)

        if final_index_type != "int":
            raise TypeError(
                self.code,
                node,
                f"List index must be int, got {final_index_type}"
            )

        # Dynamic final index, so we can only verify the assigned value type
        if not hasattr(final_index, "value"):
            return var_type

        target_list[final_index.value] = var_type
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
        if self.lookup_fun(node.name) is False:
            raise TypeError(
                self.code,
                node,
                f"The function: '{node.name}' does not exist"
            )

        func = self.lookup_fun(node.name)
        
        params = func["params"] or []
        args = node.args or []

        # validate argument counts
        if len(params) != len(args):
            raise TypeError(
                self.code,
                node,
                f"Function '{node.name}' expects {len(params)} args, got {len(args)}"
            )
        
        # Update the local variable types
        local_vars = {}
        for p, arg in zip(params, args):
            local_vars[p] = self.visit(arg)
        
        # Temperary switch scope
        new_scope = {
            "__parent__": self.v_table,
            **local_vars
        }
        old = self.v_table.copy()
        self.v_table = new_scope
        old_fun = self.f_table.copy()
        self.f_table = {"__parent__": old_fun}

        # Typecheck the function
        return_type = None
        for stmt in func["body"]:
            t = self.visit(stmt)
            if isinstance(stmt, Return):
                return_type = t

        # Restore old scope
        self.v_table = {**old, **self.v_table["__parent__"]}
        self.f_table = old_fun

        return return_type

    def check_add(self, node, left_type, right_type):
        # Allow string concatenation
        if left_type == "str" and right_type == "str":
            return "str"

        # Otherwise, both sides must be numeric
        return self.numeric_result_type(node, "+", left_type, right_type)

    def visit_sub(self, node):
        #both sides must be numeric
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        return self.numeric_result_type(node, "-", left_type, right_type)

    def check_mul(self, node, left_type, right_type):
        return self.numeric_result_type(node, "*", left_type, right_type)

    def check_div(self, node, left_type, right_type):
        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(
                self.code,
                node,
                f"Expected numeric types on operation: /, got '{left_type}' and '{right_type}'"
            )

        # division always returns float
        return "float"

    def check_pow(self, node, left_type, right_type):
        return self.numeric_result_type(node, "^", left_type, right_type)

    # comparison operators
    def check_comp_ops_expr(self, node, symbol, left_type, right_type):
        if not (left_type == right_type or self.is_numeric(left_type) and self.is_numeric(right_type)):
            raise TypeError(
                self.code,
                node,
                f"Cannot compare {left_type} {symbol} {right_type}"
            )

        return "bool"

    #boolean operators
    def check_bool_ops_expr(self, node, ops, left_type, right_type):
        if left_type != "bool" or right_type != "bool":
            raise TypeError(
                self.code,
                node,
                f"{ops} requires bool, got {left_type} and {right_type}"
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

    def check_between(self, node, left_type, right_type):
        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(
                self.code,
                node,
                f"between requires numeric types, got {left_type} and {right_type}"
            )

        if "float" in (left_type, right_type):
            return "float"

        return "int"

    def check_chance(self, node, left_type, right_type):
        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(
                self.code,
                node,
                f"chance requires numeric types, got {left_type} and {right_type}"
            )

        return "bool"

    def check_if(self, node, cond_type, kind="if"):
        # condition must be a bool
        if cond_type is None:
            return None

        if cond_type != "bool":
            raise TypeError(
                self.code,
                node,
                f"{kind} condition must be bool, got {cond_type}"
            )

        return "bool"

    def check_while(self, node, cond_type):
        # while condition must be bool
        if cond_type != "bool":
            raise TypeError(
                self.code,
                node,
                f"while condition must be bool, got {cond_type}"
            )

        return "bool"

    def check_dowhile(self, node, cond_type):
        # dowhile condition must be bool
        if cond_type != "bool":
            raise TypeError(
                self.code,
                node,
                f"dowhile condition must be bool, got {cond_type}"
            )

        return "bool"

    def visit_create_list(self, node):
        self.validate_game_name(node, "list")

        if node.name in self.v_table:
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
        # Check if the list is in a struct
        table = None
        if node.base:
            table = self.lookup_var(node.base)
            if table is False:
                raise TypeError(
                    self.code,
                    node,
                    f"The struct: '{node.base}' is not defined"
                )
            table = table[node.target] if node.target in table else False
        else:
            table = self.lookup_var(node.target)

        # Check if the list exist in table
        if table is False:
            raise TypeError(
                self.code,
                node,
                f"The list: '{node.target}' does not exist"
            )

        # Find the index
        target_list = table
        for i in node.indexing[::-1]:
            # Make sure it's a list
            if not isinstance(target_list, list):
                raise TypeError(
                    self.code,
                    node,
                    f"The target: '{target_list}' is not a list"
                )
            
            # Make sure the index is a 'int'
            index_type = self.visit(i)
            if index_type != "int":
                raise TypeError(
                    self.code,
                    node,
                    f"List index must be int, got {index_type}"
                )
            
            
            # variable index, bounds are checked at runtime
            if not hasattr(i, "value"):
                return target_list[0] if target_list else None
            index = i.value
            if not isinstance(index, int):
                raise TypeError(
                    self.code,
                    node,
                    f"The index: '{-index.value}' must be positive"
                )
                
            # Check if the index are out of bound
            if 0 <= index and index <= len(target_list) - 1:
                target_list = target_list[index]
            else:
                raise TypeError(
                    self.code,
                    node,
                    f"The index: '{index}' does not exist in '{node.target}'"
                )    
            
        return target_list


    def check_forrange(self, node, start_type, end_type):
        # Range start and end must be numeric
        if not self.is_numeric(start_type) or not self.is_numeric(end_type):
            raise TypeError(
                self.code,
                node,
                f"for-range bounds must be numeric, got {start_type} and {end_type}"
            )

    def check_foreach(self, node, collection):
        # Check if the list exists
        if collection is False:
            raise TypeError(
                self.code,
                node,
                f"The list: '{node.collection}' does not exist"
            )

        # Check if the collection is a list
        if not isinstance(collection, list):
            raise TypeError(
                self.code,
                node,
                f"Cannot iterate over non-list type '{collection}'"
            )

    def visit_input(self, node):
        scope = self.v_table

        # Find the scope whith the variable we want to change
        if node.base:
            while node.base not in scope:
                if "__parent__" not in scope:
                    raise TypeError(
                        self.code,
                        node,
                        f"The struct: '{node.base}' does not exist"
                    )
                scope = scope.get("__parent__")
            scope = scope[node.base]
        else:
            while node.name not in scope:
                if "__parent__" not in scope:
                    raise TypeError(
                            self.code,
                            node,
                            f"The variable: '{node.name}' does not exist"
                        )
                scope = scope.get("__parent__")

        if not node.indexing:
            # normal input, just set variable to string
            scope[node.name] = "str"
            return "str"

        # input into a list element
        target_list = scope[node.name]

        # make sure it's a list
        if not isinstance(target_list, list):
            raise TypeError(
                self.code,
                node,
                f"The variable: '{node.name}' is not a list"
            )
        
        # Nested indexes are stored backwards by the AST, thereby they need to be flipped
        indexes = node.indexing[::-1]
        for index_node in indexes[:-1]:
            index_type = self.visit(index_node)

            # index has to be int
            if index_type != "int":
                raise TypeError(
                    self.code,
                    node,
                    f"List index must be int, got {index_type}"
                )
            # variable index, so no value to check here
            if not hasattr(index_node, "value"):
                return "str"
            index = index_node.value

            # check bounds
            if index < 0 or index >= len(target_list):
                raise TypeError(
                    self.code,
                    node,
                    f"The index: '{index}' does not exist in '{node.name}'"
                )

            # move into the list
            target_list = target_list[index]

            # if we still have more indexes, this better be a list
            if not isinstance(target_list, list):
                raise TypeError(
                    self.code,
                    node,
                    f"Trying to index into something that isn't a list"
                )

        # final index (this is where we store the input)
        final_index_node = indexes[-1]
        final_index_type = self.visit(final_index_node)

        if final_index_type != "int":
            raise TypeError(
                self.code,
                node,
                f"List index must be int, got {final_index_type}"
            )
        if not hasattr(final_index_node, "value"):
            return "str"
        final_index = final_index_node.value

        if final_index < 0 or final_index >= len(target_list):
            raise TypeError(
                self.code,
                node,
                f"The index: '{final_index}' does not exist in '{node.name}'"
            )

        # input is always string, so overwrite the type
        target_list[final_index] = "str"
        return "str"

    def visit_output(self, node):
        # Output has no type, but each printed value must be type checked
        for each in node.value:
            self.visit(each)

        return None

    def check_create_struct(self, node, already_exists, parent_exists):
        self.validate_game_name(node, "struct")

        # Error, if the 'name' already exist
        if already_exists:
            raise TypeError(
                self.code,
                node,
                f"The struct: '{node.name}' already exists"
            )
        
        elif node.base and parent_exists is False:
            # Error, for no parent
            raise TypeError(
                self.code,
                node,
                f"The parent struct: '{node.base}' does not exist"
            )