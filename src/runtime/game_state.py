import json
from pathlib import Path

# Function to save "Game" struct in json files
class GameStateManager:
    def __init__(self, slot=1): #Define what save "slot" a file should be saved in, default 1
        base_dir = Path(__file__).parent # Defines starting path from the runtime folder
        self.path = base_dir / "save_states" / f"save_slot_{slot}.json" #Creates path to the file, using selected save slot
        self.path.parent.mkdir(parents=True, exist_ok=True) #makes sure file exists, if not create file

    # Load function
    def load(self):
        if not self.path.exists(): # checks if file exists
            return None
        try: # if file exists read data and return it
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None

    # save game state function
    def save(self, game_state):
        with open(self.path, "w", encoding="utf-8") as f: # write in save file
            json.dump(game_state, f, indent=2)