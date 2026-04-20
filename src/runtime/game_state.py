import json
from pathlib import Path

class GameStateManager:
    def __init__(self, slot=1):
        base_dir = Path(__file__).parent
        self.path = base_dir / "save_states" / f"save_slot_{slot}.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)

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