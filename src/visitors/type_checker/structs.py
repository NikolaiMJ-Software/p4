from src.errors import TypeError


class Structs:
    def check_create_struct(self, node, already_exists, parent_exists):
        self.validate_game_name(node, "struct")

        # Error, if the 'name' already exist
        if already_exists:
            raise TypeError(
                self.code,
                node,
                f"The struct: '{node.name}' already exists"
            )

        elif node.base and parent_exists is False:
            # Error, for no parent
            raise TypeError(
                self.code,
                node,
                f"The parent struct: '{node.base}' does not exist"
            )
