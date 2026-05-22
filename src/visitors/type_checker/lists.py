from src.errors import TypeError


class Lists:
    def check_create_list(self, node, already_exists):
        self.validate_game_name(node, "list")

        if already_exists:
            raise TypeError(
                self.code,
                node,
                f"The list: '{node.name}' already exists"
            )

    def check_index_access(self, node, index_type):
        # Make sure the index is a 'int'
        if index_type != "int":
            raise TypeError(
                self.code,
                node,
                f"List index must be 'int', got a '{index_type}'"
            )
