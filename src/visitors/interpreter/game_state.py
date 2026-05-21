from .runtime_value import RuntimeValue


class GameState:
    def load_game_state(self):
        loaded_game = self.game_state_manager.load()
        if loaded_game is not None and "Game" in self.v_table:
            self.v_table["Game"] = self.from_json_value(loaded_game) # Load converted JSON save-file into v_table under "Game" key

    def save_game_state(self):
        game = self.v_table.get("Game")
        if game is not None:
            self.game_state_manager.save(self.to_json_value(game)) # Convert runtime values into JSON and save to save-file

    def to_json_value(self, value): # Convert runtime values before saving them as JSON
        if isinstance(value, RuntimeValue): # Save only the actual value, not the runtime wrapper
            return self.to_json_value(value.value)

        if isinstance(value, list): # Convert all values inside lists
            return [self.to_json_value(item) for item in value]

        if isinstance(value, dict): # Convert struct fields and skip parent since they are only used during interpretation and arent a part of the actual saved game state
            return {
                key: self.to_json_value(val)
                for key, val in value.items()
                if key != "__parent__"
            }

        if value == "UNINITIALIZED":
            return None

        return value

    def from_json_value(self, value): # Convert saved JSON values back into runtime values

        if value is None:
            return "UNINITIALIZED"

        if isinstance(value, bool):
            return RuntimeValue("bool", value)

        if isinstance(value, int):
            return RuntimeValue("int", value)

        if isinstance(value, float):
            return RuntimeValue("float", value)

        if isinstance(value, str):
            return RuntimeValue("str", value)

        if isinstance(value, list):
            return [self.from_json_value(item) for item in value]

        if isinstance(value, dict):
            return {
                key: self.from_json_value(val)
                for key, val in value.items()
            }

        return value