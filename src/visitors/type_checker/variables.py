from src.errors import TypeError


class Variables:
    def check_create_variable(self, node, already_exists):
        self.validate_game_name(node, "variable")

        # Make sure no duplicate of variabels
        if already_exists:
            raise TypeError(
                self.code,
                node,
                f"The variable: '{node.name}' already exists"
            )

    def check_assign(self, node, target):
        # Check if it got inheritance
        if node.base:
            # Check if the parent exist
            if target is False:
                raise TypeError(
                    self.code,
                    node,
                    f"The struct: '{node.base}' does not exist"
                )

            # Check if the name exist
            name = node.target if hasattr(node, "target") else node.name
            if not isinstance(target, dict) or name not in target:
                raise TypeError(
                    self.code,
                    node,
                    f"The variable: '{name}' does not exist in the struct: '{node.base}'"
                )

            return

        # Check if the name exist
        if target is False:
            if hasattr(node, "target"):
                msg = f"The list: '{node.target}' does not exist"
            else:
                msg = f"The variable: '{node.name}' does not exist"

            raise TypeError(
                self.code,
                node,
                msg
            )

    def check_var(self, node, value):
        if node.base is None:
            if value is False:
                raise TypeError(
                    self.code,
                    node,
                    f"The variable: '{node.name}' does not exist"
                )
            return

        # Error, if the parent (base) is not defined
        if value is False:
            raise TypeError(
                self.code,
                node,
                f"The struct: '{node.base}' is not defined"
            )

        # Error, if the variable 'name' are not inside of the struct (base)
        if not isinstance(value, dict) or node.name not in value:
            raise TypeError(
                self.code,
                node,
                f"The variable: '{node.name}' is not defined in the struct: '{node.base}'"
            )
