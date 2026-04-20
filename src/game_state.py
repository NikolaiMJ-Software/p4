import json
from pathlib import Path

class GameStateManager:
    def __init__(self, slot=1):
        self.path = Path(f"save_slot_{slot}.json")

    def load(self):
        if not self.path.exists():
            return None
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None

    def save(self, game_state):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(game_state, f, indent=2)