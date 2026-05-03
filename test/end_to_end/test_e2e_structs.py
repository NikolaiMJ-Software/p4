import pytest

from test.end_to_end.setup_e2e import run_program
from src.errors import TypeError as TypeCheckError
from src.errors import InterpreterError


def test_e2e_output_struct_field(monkeypatch, capsys):
    code = '''create Game with:
    Weapon
    Weapon_damage

define Play:
    Weapon from Game is "sword"
    Weapon_damage from Game is 10
    output "Weapon:", Weapon from Game, "Damage:", Weapon_damage from Game
'''

    output = run_program(code, monkeypatch, capsys, slot=997)

    assert output == ["Weapon: sword Damage: 10"]


def test_e2e_struct_inheritance(monkeypatch, capsys):
    code ='''create Character with:
    Health is 100
    Name
    
create Enemy from Character with:
    Name is "Jeff"

define Play:
    output Name from Enemy
    output Health from Enemy
'''

    output = run_program(code, monkeypatch, capsys, slot=995)

    assert output == ["Jeff", "100"]


def test_e2e_nested_struct_list_access(monkeypatch, capsys):
    code = '''create Player with:
    Items is listing: "sword", "shield"

define Play:
    output index 0 of Items from Player
'''

    output = run_program(code, monkeypatch, capsys, slot=975)

    assert output == ["sword"]


def test_e2e_struct_missing_field_raises(monkeypatch, capsys):
    code = '''create Player with:
    Name

define Play:
    output Health from Player
'''

    with pytest.raises(TypeCheckError):
        run_program(code, monkeypatch, capsys, slot=971)
