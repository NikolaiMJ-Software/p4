from .runtime_value import RuntimeValue
from src.errors import InterpreterError
import random


class Arithmetic:
    def visit_add(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_add(
            node,
            left.type,
            right.type
        )

        return RuntimeValue(
            result_type,
            self.unwrap(left) + self.unwrap(right)
        )

    def visit_mul(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_mul(
            node,
            left.type,
            right.type
        )

        return RuntimeValue(
            result_type,
            self.unwrap(left) * self.unwrap(right)
        )

    def visit_div(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_div(
            node,
            left.type,
            right.type
        )

        if self.unwrap(right) == 0:
            raise InterpreterError(
                self.code,
                node,
                "division by 0"
            )

        return RuntimeValue(
            result_type,
            self.unwrap(left) / self.unwrap(right)
        )

    def visit_pow(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_pow(
            node,
            left.type,
            right.type
        )

        return RuntimeValue(
            result_type,
            self.unwrap(left) ** self.unwrap(right)
        )

    def visit_neg(self, node):
        value = self.visit(node.value)

        result_type = self.type_checker.check_neg(node, value.type)

        return RuntimeValue(
            result_type,
            -self.unwrap(value)
        )

    def visit_between(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_between(
            node,
            left.type,
            right.type
        )

        left_value = self.unwrap(left)
        right_value = self.unwrap(right)

        low = min(left_value, right_value)
        high = max(left_value, right_value)

        if result_type == "float":
            result_value = random.uniform(low, high)
        else:
            result_value = random.randrange(low, high + 1)

        return RuntimeValue(result_type, result_value)

    def visit_chance(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        result_type = self.type_checker.check_chance(
            node,
            left.type,
            right.type
        )

        return RuntimeValue(
            result_type,
            random.uniform(0, self.unwrap(right)) < self.unwrap(left)
        )