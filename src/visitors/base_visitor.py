class Visitor:
    def visit(self, node):
        if isinstance(node, str):
            return self.v_table.get(node)
        return node.accept(self)