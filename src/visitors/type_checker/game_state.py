from src.errors import TypeError


class GameState:
    # VALIDATION FOR RESERVED GAME STRUCT
    def validate_game_name(self, node, type_type):
        # check if we are dealing with and ID game
        if node.name != "Game":
            return
        # if game is not a struct sent back an error
        if type_type != "struct":
            raise TypeError(
                self.code,
                node,
                "The identifier 'Game' is reserved and can only be used as a struct name."
            )
