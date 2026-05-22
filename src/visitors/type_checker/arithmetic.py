from src.errors import TypeError


class Arithmetic:
    # NUMERIC CHECKS FOR EXPRESSIONS
    def is_numeric(self, t):
        return t in ["int", "float"]

    def numeric_result_type(self, node, symbol, left_type, right_type):
        # Makes sure both sides are numeric
        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(
                self.code,
                node,
                f"Expected numeric types on operation: {symbol}, got '{left_type}' and '{right_type}'"
            )
        if "float" in (left_type, right_type):
            return "float"
        return "int"

    def check_add(self, node, left_type, right_type):
        # Allow string concatenation
        if left_type == "str" and right_type == "str":
            return "str"

        # Otherwise, both sides must be numeric
        return self.numeric_result_type(node, "+", left_type, right_type)

    def check_mul(self, node, left_type, right_type):
        return self.numeric_result_type(node, "*", left_type, right_type)

    def check_div(self, node, left_type, right_type):
        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(
                self.code,
                node,
                f"Expected numeric types on operation: /, got '{left_type}' and '{right_type}'"
            )
        return "float"  # division always returns float

    def check_pow(self, node, left_type, right_type):
        return self.numeric_result_type(node, "^", left_type, right_type)

    def check_neg(self, node, value_type):
        if not self.is_numeric(value_type):
            raise TypeError(
                self.code,
                node,
                f"NEG requires numeric type, got '{value_type}'"
            )
        return value_type

    def check_between(self, node, left_type, right_type):
        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(
                self.code,
                node,
                f"between requires numeric types, got '{left_type}' and '{right_type}'"
            )

        if "float" in (left_type, right_type):
            return "float"

        return "int"

    def check_chance(self, node, left_type, right_type):
        if not self.is_numeric(left_type) or not self.is_numeric(right_type):
            raise TypeError(
                self.code,
                node,
                f"chance requires numeric types, got '{left_type}' and '{right_type}'"
            )

        return "bool"
