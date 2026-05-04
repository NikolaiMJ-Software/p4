import pytest

from setup_e2e import run_program
from src.errors import TypeError as TypeCheckError
from src.errors import InterpreterError


def test_e2e_save_and_load_game_state(monkeypatch, capsys):
    slot = 996

    first_code = '''create Game with:
    Game_status is 0
    Name

define Play:
    Game_status from Game is 1
    Name from Game is "Bob"
    output "saved"
'''
    output = run_program(first_code, monkeypatch, capsys, slot=slot)

    assert output == ["saved"]

    second_code = '''create Game with:
    Game_status is 0
    Name

define Play:
    output Game_status from Game
    output Name from Game
'''

    output = run_program(second_code, monkeypatch, capsys, slot=slot)

    assert output == ["1", "Bob"]


def test_e2e_type_error_does_not_save_broken_game_state(monkeypatch, capsys):
    slot = 991

    first_code = '''create Game with:
    Name

define Play:
    Name from Game is "Bob"
    output "saved"
'''

    output = run_program(first_code, monkeypatch, capsys, slot=slot)
    assert output == ["saved"]

    broken_code = '''create Game with:
    Name

define Play:
    Name from Game is "Alice"
    output MissingVariable
'''

    with pytest.raises(TypeCheckError):
        run_program(broken_code, monkeypatch, capsys, slot=slot)

    third_code = '''create Game with:
    Name

define Play:
    output Name from Game
'''

    output = run_program(third_code, monkeypatch, capsys, slot=slot)
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

    output = run_program(code, monkeypatch, capsys, inputs=["warrior"], slot=993)

    assert output == [
        "Choose class",
        "Your class is: Warrior",
        "Your weapon is: sword"
    ]
