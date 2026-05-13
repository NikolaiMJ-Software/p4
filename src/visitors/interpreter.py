from src.visitors.base_visitor import Visitor
from src.ast.nodes import *
from ..runtime.game_state import GameStateManager
from src.visitors.type_checker import *
from src.errors import InterpreterError
from src.errors import TypeError as TypeCheckError
import random

class ReturnException(Exception): # exception raised by return() to stop function call
    def __init__(self, value):
        self.value = value

class BreakException(Exception): # exception raised to stop loops
    pass

class RuntimeValue: # class to store value and type for values sent to typechecker
    def __init__(self, type_name, value):
        self.type = type_name
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})"

class InterpreterVisitor(Visitor):
    def __init__(self, code="", slot=1):
        self.code = code
        self.v_table = {} # list of variables split into scope levels
        self.f_table = {} # list of defined functions
        self.game_state_manager = GameStateManager(slot) # save-state manager, where slot equals save-file
        self.type_checker = TypeChecker(self.code)    
    
    
    # SCOPE HANDLING
    def lookup_var(self, name):
        scope = self.v_table

        while scope:
            if name in scope:
                return self.unwrap(scope[name])
            scope = scope.get("__parent__")
        return False
    
    def lookup_fun(self, name):
        scope = self.f_table

        while scope:
            if name in scope:
                return self.unwrap(scope[name])
            scope = scope.get("__parent__")
        return False


    # TYPE CHECK INTEGRATION
    def runtime_to_type(self, value):
        # Convert interpreter values into the type format used by the type checker
        if value == "UNINITIALIZED":
            return None

        if value is None:
            return None

        if isinstance(value, RuntimeValue):
            return value.type

        if isinstance(value, bool):
            return "bool"

        if isinstance(value, int):
            return "int"

        if isinstance(value, float):
            return "float"

        if isinstance(value, str):
            return "str"

        if isinstance(value, list):
            return [self.runtime_to_type(item) for item in value]

        if isinstance(value, dict):
            return {
                name: self.runtime_to_type(field_value)
                for name, field_value in value.items()
            }

        return None

    def sync_type_checker(self):
        type_table = {}
        scope = self.v_table
        
        for name, value in scope.items():
            type_table[name] = self.runtime_to_type(value)

        self.type_checker.v_table = type_table
        self.type_checker.f_table = self.f_table

    def unwrap(self, value): #unwraps runtime value to just value
        if isinstance(value, RuntimeValue):
            return value.value
        return value
    
    def unwrap_list(self, input_list):
        var_list=[]
        for var in input_list:
            if isinstance(var, list):
                var_list.append(self.unwrap_list(var))
            else:
                var_list.append(self.unwrap(var))
        return var_list

    def check_expression_type(self, node):
        self.sync_type_checker()

        return self.type_checker.visit(node)



    # GAME STATE HANDLING
    def load_game_state(self):
        loaded_game = self.game_state_manager.load()
        if loaded_game is not None and "Game" in self.v_table:
            # Convert saved JSON values back into runtime values before loading them into Game
            self.v_table["Game"] = self.from_json_value(loaded_game)
    
    def save_game_state(self):
        game = self.v_table.get("Game")
        if game is not None:
            # Convert runtime values before writing to JSON
            self.game_state_manager.save(self.to_json_value(game))

    def run(self, ast, args=None):
        should_save = True # Used to prevent saving after runtime or type errors

        try:
            for stmt in ast:
                self.visit(stmt)

            self.load_game_state()

            if "Play" in self.f_table:
                self.visit(Call("Play", args or []))

        except KeyboardInterrupt:
            print("\nProgram interrupted. Saving game state...")

        except (InterpreterError, TypeCheckError):
            should_save = False  # Do not save if the program stopped because of an error
            raise

        finally:
            if should_save: # Only save if the program ended safely or was manually interrupted
                self.save_game_state()

    def to_json_value(self, value): # Convert runtime values before saving them as JSON
        if isinstance(value, RuntimeValue):
            # Save only the actual value, not the runtime wrapper
            return self.to_json_value(value.value)

        if isinstance(value, list):
            # Convert all values inside lists
            return [self.to_json_value(item) for item in value]

        if isinstance(value, dict):
            # Convert struct fields and skip parent since they are only used during interpretation and arent a part of the actual saved game state
            return {
                key: self.to_json_value(val)
                for key, val in value.items()
                if key != "__parent__"
            }

        if value == "UNINITIALIZED":
            return None

        return value

    def from_json_value(self, value):
        # Convert saved JSON values back into runtime values

        if value is None:
            return "UNINITIALIZED"

        if isinstance(value, bool):
            return RuntimeValue("bool", value)

        if isinstance(value, int):
            return RuntimeValue("int", value)

        if isinstance(value, float):
            return RuntimeValue("float", value)

        if isinstance(value, str):
            return RuntimeValue("str", value)

        if isinstance(value, list):
            return [self.from_json_value(item) for item in value]

        if isinstance(value, dict):
            return {
                key: self.from_json_value(val)
                for key, val in value.items()
            }

        return value



    # LITERALS
    def visit_int_literal(self, node):
        return RuntimeValue("int", node.value)

    def visit_float_literal(self, node):
        return RuntimeValue("float", node.value)

    def visit_string_literal(self, node):
        return RuntimeValue("str", node.value)

    def visit_bool_literal(self, node):
        return RuntimeValue("bool", node.value)
    
    
    
    
    # STATEMENTS
    def visit_create_variable(self, node):
        # Make sure no duplicate of variabels
        self.type_checker.check_create_variable(
            node,
            node.name in self.v_table
        )

        # Set value to 'UNINITIALIZED' if it doesn't exist
        if node.value is None:
            self.v_table[node.name] = "UNINITIALIZED"
            return

        # Save variable in v_table, with name and value
        value = self.visit(node.value)
        self.v_table[node.name] = value

    def visit_create_struct(self, node):
        # Make sure no duplicate of struct, and check parrent
        self.type_checker.check_create_struct(
            node,
            node.name in self.v_table,
            self.lookup_var(node.base)
        )

        parent = self.lookup_var(node.base)
        fields = {field.name: self.visit(field.value) if field.value else "UNINITIALIZED" for field in node.fields}

        if parent is False:
            self.v_table[node.name] = fields
        else:
            self.v_table[node.name] = {**parent, **fields}
        
    def visit_create_list(self, node):
        # Make sure no duplicate of variabels
        self.type_checker.check_create_list(
            node,
            node.name in self.v_table
        )

        listing = []
        if node.value:
            for val in node.value:
                listing.append(self.visit(val))

        self.v_table[node.name] = listing
        
    def visit_assign(self, node):
        # Save value
        value = self.visit(node.value)

        # Check if it got inheritance
        if node.base:
            # Find parent
            target = self.lookup_var(node.base)
            # Check if parent and name exist
            self.type_checker.check_assign(node, target)
            # Save in the struct's v_table
            target[node.name] = value
            return

        # Find the scope where the variable exists
        table = self.v_table
        while table and node.name not in table:
            table = table.get("__parent__")

        # Check if the name exist
        self.type_checker.check_assign(node, table)

        # Save in v_table
        table[node.name] = value

    def visit_assign_index(self, node):
        value = self.visit(node.value)

        if node.target.base:
            lst = self.lookup_var(node.target.base)[node.target.target]
        else:
            lst = self.lookup_var(node.target.target)

        # Check if list exist
        self.type_checker.check_assign(
            node.target,
            lst
        )

        indexes = node.target.indexing
        lst = self.iterate_through_list(node, lst, indexes[:-1])

        final_index = self.unwrap(self.visit(indexes[-1]))
        if not isinstance(lst, list):
            raise InterpreterError(
                self.code,
                node,
                f"Trying to assign into something that isn't a list"
            )

        if final_index < 0 or final_index >= len(lst):
            raise InterpreterError(
                self.code,
                node,
                f"Index {final_index} outside of list: '{self.unwrap_list(lst)}'"
            )

        lst[final_index] = value

    def visit_if(self, node):
        # condition must be a bool
        cond = self.visit(node.cond)
        self.type_checker.check_if(node, cond.type, "if")

        if self.unwrap(cond):
            # Save outer scope and create if scope
            old = self.v_table
            self.v_table = {"__parent__": old}
            old_fun = self.f_table
            self.f_table = {"__parent__": old_fun}
            try:
                # Run each statement inside if body
                for stmt in node.body:
                    self.visit(stmt)
            finally:
                # Restore outer scope after if body
                self.v_table = old
                self.f_table = old_fun
            return

        # Check all else-if branches
        for cond, body in node.elifs or []:
            # Type check else-if condition
            cond_value = self.visit(cond)
            self.type_checker.check_if(node, cond_value.type, "elif")

            if self.unwrap(cond_value):
                # Save outer scope and create else-if scope
                old = self.v_table
                self.v_table = {"__parent__": old}
                old_fun = self.f_table
                self.f_table = {"__parent__": old_fun}

                try:
                    # Run each statement inside else-if body
                    for stmt in body:
                        self.visit(stmt)
                finally:
                    # Restore outer scope after else-if body
                    self.v_table = old
                    self.f_table = old_fun
                return

        # Run else branch if no previous condition matched
        if node.elses:
            # Save outer scope and create else scope
            old = self.v_table
            self.v_table = {"__parent__": old}
            old_fun = self.f_table
            self.f_table = {"__parent__": old_fun}
            try:
                # Run each statement inside else body
                for stmt in node.elses:
                    self.visit(stmt)
            finally:
                # Restore outer scope after else body
                self.v_table = old
                self.f_table = old_fun

    def visit_while(self, node):
        # Save outer scope
        old = self.v_table
        old_fun = self.f_table
        try:
            while True:
                # Type check condition only
                self.check_expression_type(node.cond)

                if not self.unwrap(self.visit(node.cond)):
                    break

                # Create fresh scope for this iteration
                self.v_table = {"__parent__": old}
                self.f_table = {"__parent__": old_fun}

                try:
                    # Run each statement inside while body
                    for stmt in node.body:
                        self.visit(stmt)

                except BreakException:
                    # Stop loop if break is used
                    break

                finally:
                    # Remove loop body scope before next iteration
                    self.v_table = old
                    self.f_table = old_fun

        finally:
            # Restore outer scope after while is done
            self.v_table = old
            self.f_table = old_fun
                
    def visit_dowhile(self, node):
        old = self.v_table
        old_fun = self.f_table
        try:
            while True:
                # Create fresh body scope for this iteration
                self.v_table = {"__parent__": old}
                self.f_table = {"__parent__": old_fun}

                try:
                    # Run each statement inside do-while body
                    for stmt in node.body:
                        self.visit(stmt)

                except BreakException:
                    # Stop loop if break is used
                    break

                finally:
                    # Remove body scope before checking condition / next iteration
                    self.v_table = old
                    self.f_table = old_fun

                # Type check condition only
                self.check_expression_type(node.cond)

                # Check condition after body has run
                if not self.unwrap(self.visit(node.cond)):
                    break

        finally:
            # Restore outer scope after do-while is done
            self.v_table = old
            self.f_table = old_fun
            
    def visit_forrange(self, node):
        self.check_expression_type(node)

        start = self.unwrap(self.visit(node.start))
        end = self.unwrap(self.visit(node.end))

        reverse = False
        if end < start:
            end, start = start, end
            reverse = True

        # Save outer scope and create for-range scope
        old = self.v_table
        self.v_table = {"__parent__": old}
        old_fun = self.f_table
        self.f_table = {"__parent__": old_fun}

        try:
            start_stop_range = range(start, end + 1) if not reverse else reversed(range(start, end + 1))

            for i in start_stop_range:
                # Save loop scope before this iteration
                old_table = self.v_table.copy()
                old_f_table = self.f_table.copy()
                # Set current loop variable as int RuntimeValue
                self.v_table[node.name] = RuntimeValue("int", i)

                try:
                    # Run each statement inside for-range body
                    for stmt in node.body:
                        self.visit(stmt)

                except BreakException:
                    # Stop loop if break is used
                    break

                finally:
                    # Restore loop scope before next iteration
                    self.v_table = old_table
                    self.f_table = old_f_table

        finally:
            # Restore outer scope after for-range is done
            self.v_table = old
            self.f_table = old_fun
    
    def visit_foreach(self, node):
        self.check_expression_type(node)

        # Find the list we want to loop over
        collection = self.lookup_var(node.collection)
        if collection is False:
            raise InterpreterError(
                self.code,
                node,
                f"The list: '{node.collection}' does not exist"
            )

        # Save outer scope and create foreach scope
        old = self.v_table
        self.v_table = {"__parent__": old}
        old_fun = self.f_table
        self.f_table = {"__parent__": old_fun}

        try:
            # Go through each item in the list
            for item in collection:
                # Save loop scope before this iteration
                old_table = self.v_table.copy()
                old_f_table = self.f_table.copy()

                # Set current loop variable
                self.v_table[node.name] = item

                try:
                    # Run each statement inside foreach body
                    for stmt in node.body:
                        self.visit(stmt)

                except BreakException:
                    # Stop loop if break is used
                    break

                finally:
                    # Restore loop scope before next iteration
                    self.v_table = old_table
                    self.f_table = old_f_table

        finally:
            # Restore outer scope after foreach is done
            self.v_table = old
            self.f_table = old_fun
    
    def visit_define(self, node):
        result_type = self.check_expression_type(node)
        self.f_table[node.name] = {
            "params" : node.params,
            "body" : node.body
        }
    
    def visit_return(self, node):
        result_type = self.check_expression_type(node)
        value = self.visit(node.value)
        raise ReturnException(value)

    def visit_break(self, node):
        result_type = self.check_expression_type(node)
        raise BreakException()

    def visit_expression(self, node):
        return self.visit(node.value)

    def visit_input(self, node):
        value = RuntimeValue("str", input())
        indexing = node.indexing
        name = node.name
        base = node.base
        scope = self.v_table
        
        self.type_checker.check_assign(
            node,
            name in self.v_table,
            self.lookup_var(base)
        )

        # Find the scope whith the variable we want to change
        if base:
            while base not in scope:
                scope = scope.get("__parent__")
            scope = scope[base]
        else:
            while name not in scope:
                scope = scope.get("__parent__")
                
        if indexing: # Handle if the variable is a list
            scope = scope[name] # can safely enter variable as we know its a list
            indices = [self.unwrap(self.visit(i)) for i in indexing][::-1] # reverse list because of our syntax
            for index in indices[:-1]:
                if index < 0 or index >= len(scope):
                    raise InterpreterError(
                            self.code,
                            node,
                            f"Index {index} outside of list: '{scope}'"
                        )
                if not isinstance(scope[index],list):
                    raise InterpreterError(
                            self.code,
                            node,
                            f"Index {index} of the list {scope} is not a list"
                        )
                scope = scope[index]
            if indices[-1] < 0 or indices[-1] >= len(scope):
                raise InterpreterError(
                    self.code,
                    node,
                    f"Index {indices[-1]} outside of list: '{scope}'"
                )
            if not isinstance(scope,list):
                    raise InterpreterError(
                            self.code,
                            node,
                            f"Index {indices[-1]} of the list {scope} is not a list"
                        )
            scope[indices[-1]] = value
        else: # standard case if variable is not a list
            scope[name] = value
    
    def visit_output(self, node):
        values = [self.visit(v) for v in node.value]
        processed = [] # storage for processed strings
        for v in values:
            v = self.unwrap(v)
            
            # Unwrap each element in a list
            if isinstance(v, list):
                v = self.unwrap_list(v)
            
            if isinstance(v, str):
                v = v.replace("\\n", "\n")  # convert \n into actual NEWLINE

            processed.append(v)

        print(*processed)



    # EXPRESSIONS
    def visit_or_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_bool_ops_expr(node, "OR", left.type, right.type)

        return RuntimeValue(
            result_type,
            self.unwrap(left) or self.unwrap(right)
        )

    def visit_and_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_bool_ops_expr(node, "AND", left.type, right.type)

        return RuntimeValue(
            result_type,
            self.unwrap(left) and self.unwrap(right)
        )

    def visit_xor_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_bool_ops_expr(node, "XOR", left.type, right.type)

        return RuntimeValue(
            result_type,
            self.unwrap(left) ^ self.unwrap(right)
        )

    def visit_not_expr(self, node):
        value = self.visit(node.cond)

        result_type = self.type_checker.check_bool_ops_expr(node, "AND", value.type, "bool")

        return RuntimeValue(
            result_type,
            not self.unwrap(value)
        )

    def visit_equal_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_comp_ops_expr(node, "==", left.type, right.type)

        return RuntimeValue(
            result_type,
            self.unwrap(left) == self.unwrap(right)
        )

    def visit_not_equal_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_comp_ops_expr(node, "!=", left.type, right.type)

        return RuntimeValue(
            result_type,
            self.unwrap(left) != self.unwrap(right)
        )

    def visit_greater_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_comp_ops_expr(node, ">", left.type, right.type)

        return RuntimeValue(
            result_type,
            self.unwrap(left) > self.unwrap(right)
        )

    def visit_less_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_comp_ops_expr(node, "<", left.type, right.type)

        return RuntimeValue(
            result_type,
            self.unwrap(left) < self.unwrap(right)
        )

    def visit_greater_equal_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_comp_ops_expr(node, ">=", left.type, right.type)

        return RuntimeValue(
            result_type,
            self.unwrap(left) >= self.unwrap(right)
        )

    def visit_less_equal_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_comp_ops_expr(node, "<=", left.type, right.type)

        return RuntimeValue(
            result_type,
            self.unwrap(left) <= self.unwrap(right)
        )
    
    def visit_add(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_add(
            node,
            left.type,
            right.type
        )

        return RuntimeValue(
            result_type,
            self.unwrap(left) + self.unwrap(right)
        )
    

    def visit_mul(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_mul(
            node,
            left.type,
            right.type
        )

        return RuntimeValue(
            result_type,
            self.unwrap(left) * self.unwrap(right)
        )

    def visit_div(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_div(
            node,
            left.type,
            right.type
        )

        if self.unwrap(right) == 0:
            raise InterpreterError(
                self.code,
                node,
                "division by 0"
            )

        return RuntimeValue(
            result_type,
            self.unwrap(left) / self.unwrap(right)
        )
    
    def visit_pow(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_pow(
            node,
            left.type,
            right.type
        )

        return RuntimeValue(
            result_type,
            self.unwrap(left) ** self.unwrap(right)
        )

    def visit_neg(self, node):
        value = self.visit(node.value)

        result_type = self.type_checker.check_neg(node, value.type)

        return RuntimeValue(
            result_type,
            -self.unwrap(value)
        )

    def visit_between(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_between(
            node,
            left.type,
            right.type
        )

        left_value = self.unwrap(left)
        right_value = self.unwrap(right)

        result_value = left_value
        if left_value < right_value:
            result_value = random.randrange(left_value, right_value + 1)
        elif left_value > right_value:
            result_value = random.randrange(right_value, left_value + 1)

        return RuntimeValue(result_type, result_value)
    
    def visit_chance(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_chance(
            node,
            left.type,
            right.type
        )

        return RuntimeValue(
            result_type,
            random.randrange(0, self.unwrap(right)) < self.unwrap(left)
        )
    
    def visit_var(self, node):
        if node.base:
            struct = self.lookup_var(node.base)
            self.type_checker.check_var(node, struct)

            return struct[node.name]

        value = self.lookup_var(node.name)
        self.type_checker.check_var(node, value)

        return value
    
    def visit_call(self, node):
        self.check_expression_type(node) # Sync current runtime types without checking the whole function body
        function = self.lookup_fun(node.name)
        params = function["params"] or []
        body = function["body"]
        args = node.args or []
        
        local_vars = {}
        for param, arg in zip(params, args):
            local_vars[param] = self.visit(arg)

        old = self.v_table # Save current scope
        self.v_table = {
            "__parent__": old,
            **local_vars
        }
        old_fun = self.f_table
        self.f_table = {"__parent__": old_fun}
        try:
            for stmt in body:
                self.visit(stmt)

        except ReturnException as r:
            return r.value # Return the actual runtime value from the function

        finally:
            self.v_table = old # Always restore scope after the function call
            self.f_table = old_fun

        return None
    
    def visit_index_access(self, node):
        if node.base: # If not from parent, look up value
            lst_base = self.lookup_var(node.base)
            lst = lst_base[node.target]
        else: # If has a parent, look up parent, and then find the target value
            lst = self.lookup_var(node.target)

        # Check if list exist
        self.type_checker.check_assign(
            node,
            lst
        )
        return self.iterate_through_list(node, lst, node.indexing[::-1])

    def iterate_through_list(self, node, lst, index):
        for index in index:
            index = self.visit(index)
                
            # Make sure it's a list
            if not isinstance(lst, list):
                raise TypeError(
                    self.code,
                    node,
                    f"Trying to index into something that isn't a list"
                )

            self.type_checker.check_index_access(
                node,
                index.type
            )
            
            index = self.unwrap(index)
            # Check if the index are out of bound
            if index < 0 and index > len(lst) - 1:
                raise InterpreterError(
                    self.code,
                    node,
                    f"The index: '{index}' does not exist in '{node.target}'"
                )
            lst = lst[index]
        return lst