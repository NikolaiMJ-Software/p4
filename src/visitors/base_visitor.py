class Visitor:
    def visit(self, node):
        if isinstance(node, list):
            return [self.visit(n) for n in node]
        return node.accept(self)