from .runtime_value import RuntimeValue


class Boolean:
    def visit_or_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_bool_ops_expr(node, "OR", left.type, right.type)

        return RuntimeValue(
            result_type,
            self.unwrap(left) or self.unwrap(right)
        )

    def visit_and_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_bool_ops_expr(node, "AND", left.type, right.type)

        return RuntimeValue(
            result_type,
            self.unwrap(left) and self.unwrap(right)
        )

    def visit_xor_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_bool_ops_expr(node, "XOR", left.type, right.type)

        return RuntimeValue(
            result_type,
            self.unwrap(left) ^ self.unwrap(right)
        )

    def visit_not_expr(self, node):
        value = self.visit(node.cond)

        result_type = self.type_checker.check_bool_ops_expr(node, "NOT", value.type)

        return RuntimeValue(
            result_type,
            not self.unwrap(value)
        )