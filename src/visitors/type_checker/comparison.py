from src.errors import TypeError


class Comparison:
    def check_comp_ops_expr(self, node, symbol, left_type, right_type):
        if not (left_type == right_type or self.is_numeric(left_type) and self.is_numeric(right_type)):
            raise TypeError(
                self.code,
                node,
                f"Can't compare: '{left_type}' {symbol} '{right_type}'"
            )

        return "bool"
