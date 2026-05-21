from .runtime_value import RuntimeValue
from src.errors import InterpreterError
from src.errors import TypeError


class Lists:
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

    def visit_assign_index(self, node):
        value = self.visit(node.value)
        lst = self.lookup_var(node.target.base) if node.target.base else self.lookup_var(node.target.target)

        # Check if list exist
        self.type_checker.check_assign(node.target, lst)
        if node.target.base:
            lst = lst[node.target.target]

        # Find the last target list
        indexes = node.target.indexing[::-1]
        for i in indexes[:-1]:
            lst = self.iterate_through_list(node, lst, i)

        # Assign to last index
        self.iterate_through_list(node, lst, indexes[-1])
        final_index = self.unwrap(self.visit(indexes[-1]))
        lst[final_index] = value

    def visit_index_access(self, node):
        lst = self.lookup_var(node.base) if node.base else self.lookup_var(node.target)

        # Check if list exist
        self.type_checker.check_assign(node, lst)
        if node.base:
            lst = lst[node.target]
        for i in node.indexing[::-1]:
            lst = self.iterate_through_list(node, lst, i)
        return lst

    def iterate_through_list(self, node, lst, index):
        index = self.visit(index)

        # Make sure it's a list
        if not isinstance(lst, list):
            raise TypeError(
                self.code,
                node,
                f"Trying to index into something that isn't a list"
            )

        # Check type
        self.type_checker.check_index_access(
            node,
            index.type
        )

        index = self.unwrap(index)
        # Check if the index are out of bound
        if index < 0 or index > len(lst) - 1:
            raise InterpreterError(
                self.code,
                node,
                f"The index: '{index}' does not exist in '{node.target}'"
            )
        return lst[index]