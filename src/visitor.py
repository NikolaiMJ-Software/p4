class Visitor:
    def visit(self, node):
        return node.accept(self)