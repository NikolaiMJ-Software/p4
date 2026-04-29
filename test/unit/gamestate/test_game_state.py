import json
from src.runtime.game_state import GameStateManager


def test_load_returns_none_when_save_file_does_not_exist(tmp_path):
    manager = GameStateManager(slot=1, base_dir=tmp_path)

    result = manager.load()

    assert result is None


def test_save_creates_save_file(tmp_path):
    manager = GameStateManager(slot=1, base_dir=tmp_path)

    game_state = {
        "Class": "Warrior",
        "Health": 100,
        "Weapon": "Sword"
    }

    manager.save(game_state)

    assert manager.path.exists()


def test_save_and_load_game_state(tmp_path):
    manager = GameStateManager(slot=1, base_dir=tmp_path)

    game_state = {
        "Class": "Mage",
        "Health": 75,
        "Weapon": "Staff"
    }

    manager.save(game_state)
    loaded = manager.load()

    assert loaded == game_state


def test_different_slots_create_different_files(tmp_path):
    slot_1 = GameStateManager(slot=1, base_dir=tmp_path)
    slot_2 = GameStateManager(slot=2, base_dir=tmp_path)

    slot_1.save({"Health": 100})
    slot_2.save({"Health": 50})

    assert slot_1.load() == {"Health": 100}
    assert slot_2.load() == {"Health": 50}
    assert slot_1.path != slot_2.path


def test_load_returns_none_if_json_is_invalid(tmp_path):
    manager = GameStateManager(slot=1, base_dir=tmp_path)

    manager.path.write_text("{ invalid json", encoding="utf-8")

    result = manager.load()

    assert result is None