from .runtime_value import RuntimeValue
from .interpreter import BreakException

class Loops:
    def visit_while(self, node):
        # Save outer scope
        old = self.v_table
        old_fun = self.f_table

        try:
            while True:
                # Type check condition
                cond = self.visit(node.cond)
                self.type_checker.check_while(node, cond.type)

                if not self.unwrap(cond):
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

                # Type check condition
                cond = self.visit(node.cond)
                self.type_checker.check_dowhile(node, cond.type)

                # Check condition after body has run
                if not self.unwrap(cond):
                    break

        finally:
            # Restore outer scope after do-while is done
            self.v_table = old
            self.f_table = old_fun

    def visit_forrange(self, node):
        # Evaluate range start and end
        start_value = self.visit(node.start)
        end_value = self.visit(node.end)

        # Range start and end must be numeric
        self.type_checker.check_forrange(
            node,
            start_value.type,
            end_value.type
        )

        start = self.unwrap(start_value)
        end = self.unwrap(end_value)

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
        # Find the list we want to loop over
        collection = self.lookup_var(node.collection)

        # Check if the collection exists and is a list
        self.type_checker.check_foreach(node, collection)

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