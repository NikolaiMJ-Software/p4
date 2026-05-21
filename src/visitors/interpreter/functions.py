from .runtime_value import RuntimeValue
from .interpreter import ReturnException
from src.errors import InterpreterError


class Functions:
    def visit_define(self, node):
        # Check if the function are already defined
        self.type_checker.check_define(
            node,
            node.name in self.f_table
        )

        # Save data as 'params' and 'body' in functions
        self.f_table[node.name] = {
            "params": node.params if node.name != "Play" else node,
            "body": node.body
        }

    def visit_return(self, node):
        # Evaluate return value
        value = self.visit(node.value)
        # Stop function call and send value back
        raise ReturnException(value)

    def visit_call(self, node):
        function = self.lookup_fun(node.name)

        # Check if function exists and argument count matches
        self.type_checker.check_call(node, function)

        params = [] if node.name == "Play" else function["params"] or []
        body = function["body"]
        args = node.args or []

        # validate argument counts
        if len(params) != len(args):
            raise InterpreterError(
                self.code,
                node if node.name != "Play" else self.f_table["Play"]["params"],
                f"Function '{node.name}' expects {len(params)} args, got {len(args)}"
            )

        local_vars = {}

        # Evaluate arguments and bind them to parameters
        for param, arg in zip(params, args):
            local_vars[param] = self.visit(arg)

        old = self.v_table
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
            return r.value

        finally:
            self.v_table = old
            self.f_table = old_fun

        return None