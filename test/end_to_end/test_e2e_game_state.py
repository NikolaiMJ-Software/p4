import pytest, json, os

from setup_e2e import *
from src.errors import TypeError as TypeCheckError
from src.errors import InterpreterError


def test_e2e_save_game_state_writes_json(monkeypatch, capsys):
    code = '''create Game with:
    Game_status is 0
    Name

define Play:
    Game_status from Game is 1
    Name from Game is "Bob"
    output "saved"
'''

    output = run_program(code, monkeypatch, capsys)

    assert output == ["saved"]

    with open("p4/src/runtime/save_states/save_slot_999.json", "r") as file:
        data = json.load(file)

    assert data == {
        "Game_status": 1,
        "Name": "Bob"
    }


def test_e2e_load_game_state_from_json(monkeypatch, capsys):
    os.makedirs("src/runtime/save_states", exist_ok=True)

    with open("p4/src/runtime/save_states/save_slot_999.json", "w") as file:
        json.dump({
            "Game_status": 1,
            "Name": "Bob"
        }, file)

    code = '''create Game with:
    Game_status is 0
    Name

define Play:
    output Game_status from Game
    output Name from Game
'''

    output = run_program(code, monkeypatch, capsys)

    assert output == ["1", "Bob"]


def test_e2e_type_error_does_not_save_broken_game_state(monkeypatch, capsys):
    first_code = '''create Game with:
    Name

define Play:
    Name from Game is "Bob"
    output "saved"
'''

    output = run_program(first_code, monkeypatch, capsys)
    assert output == ["saved"]

    broken_code = '''create Game with:
    Name

define Play:
    Name from Game is "Alice"
    output MissingVariable
'''

    with pytest.raises(TypeCheckError, match="The variable: 'MissingVariable' does not exist"):
        run_program(broken_code, monkeypatch, capsys)

    third_code = '''create Game with:
    Name

define Play:
    output Name from Game
'''

    output = run_program(third_code, monkeypatch, capsys)
    assert output == ["Bob"]


def test_e2e_simple_game_flow(monkeypatch, capsys):
    code = '''create Game with:
    Class
    Weapon
    Weapon_damage

create Class

define Play:
    output "Choose class"
    input in Class
    if Class equal "warrior" do:
        Class from Game is "Warrior"
        Weapon from Game is "sword"
        Weapon_damage from Game is 10
        output "Your class is:", Class from Game
        output "Your weapon is:", Weapon from Game
    else do:
        output "Invalid class"
'''
    output = run_program(code, monkeypatch, capsys, inputs=["warrior"])

    assert output == [
        "Choose class",
        "Your class is: Warrior",
        "Your weapon is: sword"
    ]

def test_e2e_stop_game_while_running(monkeypatch, capsys):
    # Stop the program with 'Ctrl+c'
    force_break_code = '''create Game with:
    Animal

define Play:
    Animal from Game is "Raccoon"
    create X
    input in X
    Animal from Game is "Panda"
'''

    output = run_program(force_break_code, monkeypatch, capsys, inputs=[KeyboardInterrupt])
    assert output == ["Program interrupted. Saving game state..."]
    
    # Check the Animal in Game is still 'Raccoon'
    code2 = '''create Game with:
    Animal

define Play:
    output Animal from Game
'''
    output = run_program(code2, monkeypatch, capsys)
    assert output == ["Raccoon"]