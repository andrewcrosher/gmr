import json
from .models import GameTime, GameState
from .data import drivers

SAVE_FILE = "savegame.json"

def save_game(state, time, filename=SAVE_FILE):
    data = {
        "time": time.to_dict(),
        "state": state.to_dict()
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def load_game(filename=SAVE_FILE):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        time = GameTime.from_dict(data["time"])
        state = GameState.from_dict(data["state"])
        
        # Restore driver references and sync data
        if state.player_driver:
            for d in drivers:
                if d["name"] == state.player_driver["name"]:
                    d.update(state.player_driver)
                    state.player_driver = d
                    break
        
        return state, time
    except FileNotFoundError:
        return None, None
    except Exception as e:
        print(f"Error loading save: {e}")
        return None, None
