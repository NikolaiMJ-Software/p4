from src.errors import TypeError


class Boolean:
    def check_bool_ops_expr(self, node, ops, left_type, right_type="bool"):
        include_right = f" and '{right_type}'"
        if ops == "NOT":
            include_right = ""
        if left_type != "bool" or right_type != "bool":
            raise TypeError(
                self.code,
                node,
                f"{ops} requires bool, got '{left_type}'{include_right}"
            )
        return "bool"
