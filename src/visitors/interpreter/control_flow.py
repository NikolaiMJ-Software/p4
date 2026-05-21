from .runtime_value import RuntimeValue
from .interpreter import BreakException

class ControlFlow:
    def visit_if(self, node):
        cond = self.unwrap(self.visit(node.cond))
        cond = None if cond == "UNINITIALIZED" else cond
        if cond:
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
            cond_value = self.unwrap(self.visit(cond))
            cond_value = None if cond_value == "UNINITIALIZED" else cond_value
            if cond_value:
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

    def visit_break(self, node):
        raise BreakException()