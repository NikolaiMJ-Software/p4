from src.errors import TypeError

class TypeChecker:
    def __init__(self, code=""):
        self.code = code



    # NUMERIC CHECKS FOR EXPRESSIONS
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



    # VALIDATION FOR RESERVED GAME STRUCT
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



    # STATEMENTS
    def check_create_variable(self, node, already_exists):
        self.validate_game_name(node, "variable")

        # Make sure no duplicate of variabels
        if already_exists:
            raise TypeError(
                self.code,
                node,
                f"The variable: '{node.name}' already exists"
            )
    
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
    
    def check_create_list(self, node, already_exists):
        self.validate_game_name(node, "list")

        if already_exists:
            raise TypeError(
                self.code,
                node,
                f"The list: '{node.name}' already exists"
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
            name = node.target if hasattr(node, "target") else node.name
            if not isinstance(target, dict) or name not in target:
                raise TypeError(
                    self.code,
                    node,
                    f"The variable: '{name}' does not exist in the struct: '{node.base}'"
                )

            return

        # Check if the name exist
        if target is False:
            if hasattr(node, "target"):
                msg = f"The list: '{node.target}' does not exist"
            else:
                msg = f"The variable: '{node.name}' does not exist"
            
            raise TypeError(
                self.code,
                node,
                msg
            )
    
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
    
    def check_define(self, node, already_exists):
        self.validate_game_name(node, "function")

        # Check if the function are already defined
        if already_exists:
            raise TypeError(
                self.code,
                node,
                f"Function: '{node.name}' already exists"
            )
    
    
    
    # EXPRESSIONS
    def check_bool_ops_expr(self, node, ops, left_type, right_type = "bool"):
        include_right = f" and '{right_type}'"
        if ops == "NOT":
            include_right = ""
        if left_type != "bool" or right_type != "bool":
            raise TypeError(
                self.code,
                node,
                f"{ops} requires bool, got '{left_type}'{include_right}"
            )
        return "bool"
    
    def check_comp_ops_expr(self, node, symbol, left_type, right_type):
        if not (left_type == right_type or self.is_numeric(left_type) and self.is_numeric(right_type)):
            raise TypeError(
                self.code,
                node,
                f"Can't compare: '{left_type}' {symbol} '{right_type}'"
            )

        return "bool"
    
    def check_add(self, node, left_type, right_type):
        # Allow string concatenation
        if left_type == "str" and right_type == "str":
            return "str"

        # Otherwise, both sides must be numeric
        return self.numeric_result_type(node, "+", left_type, right_type)
    
    def check_mul(self, node, left_type, right_type):
        return self.numeric_result_type(node, "*", left_type, right_type)

    def check_div(self, node, left_type, right_type):
        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(
                self.code,
                node,
                f"Expected numeric types on operation: /, got '{left_type}' and '{right_type}'"
            )
        return "float" # division always returns float
    
    def check_pow(self, node, left_type, right_type):
        return self.numeric_result_type(node, "^", left_type, right_type)
    
    def check_neg(self, node, value_type):
        if not self.is_numeric(value_type):
            raise TypeError(
                self.code,
                node,
                f"NEG requires numeric type, got '{value_type}'"
            )
        return value_type
    
    def check_between(self, node, left_type, right_type):
        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(
                self.code,
                node,
                f"between requires numeric types, got '{left_type}' and '{right_type}'"
            )

        if "float" in (left_type, right_type):
            return "float"

        return "int"
    
    def check_chance(self, node, left_type, right_type):
        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(
                self.code,
                node,
                f"chance requires numeric types, got '{left_type}' and '{right_type}'"
            )

        return "bool"
    
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

    def check_call(self, node, function):
        # Check if the function are already defined
        if function is False:
            raise TypeError(
                self.code,
                node,
                f"The function: '{node.name}' does not exist"
            )

    def check_index_access(self, node, index_type):        
        # Make sure the index is a 'int'
        if index_type != "int":
            raise TypeError(
                self.code,
                node,
                f"List index must be 'int', got a '{index_type}'"
            )