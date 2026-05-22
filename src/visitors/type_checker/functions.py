from src.errors import TypeError


class Functions:
    def check_define(self, node, already_exists):
        self.validate_game_name(node, "function")

        # Check if the function are already defined
        if already_exists:
            raise TypeError(
                self.code,
                node,
                f"Function: '{node.name}' already exists"
            )

    def check_call(self, node, function):
        # Check if the function are already defined
        if function is False:
            raise TypeError(
                self.code,
                node,
                f"The function: '{node.name}' does not exist"
            )
