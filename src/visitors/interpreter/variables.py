from .runtime_value import RuntimeValue


class Variables:
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

    def visit_assign(self, node):
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
        table = False if len(self.v_table) == 0 else self.v_table
        while table and node.name not in table:
            table = table.get("__parent__")

        # Check if the name exist
        self.type_checker.check_assign(node, table)

        # Save in v_table
        table[node.name] = value

    def visit_var(self, node):
        if node.base:
            struct = self.lookup_var(node.base)
            self.type_checker.check_var(node, struct)

            return struct[node.name]

        value = self.lookup_var(node.name)
        self.type_checker.check_var(node, value)

        return value

    def visit_input(self, node):
        value = RuntimeValue("str", input())
        indexing = node.indexing
        name = node.name
        base = node.base

        target = self.lookup_var(base) if base else self.lookup_var(name)
        self.type_checker.check_assign(
            node,
            target
        )

        # Find the scope whith the variable we want to change
        scope = self.v_table
        if base:
            while base not in scope:
                scope = scope.get("__parent__")
            scope = scope[base]
        else:
            while name not in scope:
                scope = scope.get("__parent__")

        if indexing: # Handle if the variable is a list
            indexes = indexing[::-1]

            # Find the last target list
            scope = scope[name]
            for i in indexes[:-1]:
                scope = self.iterate_through_list(node, scope, i)

            # Assign to last index
            self.iterate_through_list(node, scope, indexes[-1])
            final_index = self.unwrap(self.visit(indexes[-1]))
            scope[final_index] = value

        else: # standard case if variable is not a list
            scope[name] = value