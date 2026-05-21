from .runtime_value import RuntimeValue


class Comparison:
    def visit_equal_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        return RuntimeValue(
            "bool",
            self.unwrap(left) == self.unwrap(right)
        )

    def visit_not_equal_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        return RuntimeValue(
            "bool",
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