
class Structs:
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