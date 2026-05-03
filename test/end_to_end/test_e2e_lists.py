import pytest

from test.end_to_end.setup_e2e import run_program
from src.errors import TypeError as TypeCheckError
from src.errors import InterpreterError


def test_e2e_list_index_output(monkeypatch, capsys):
    code = '''create Items is listing: "sword", "shield", "potion"

define Play:
    output index 0 of Items
    output index 2 of Items
'''

    output = run_program(code, monkeypatch, capsys, slot=990)

    assert output == ["sword", "potion"]


def test_e2e_list_index_assignment(monkeypatch, capsys):
    code = '''create Items is listing: "sword", "shield", "potion"

define Play:
    index 1 of Items is "axe"
    output index 1 of Items
'''

    output = run_program(code, monkeypatch, capsys, slot=989)

    assert output == ["axe"]


def test_e2e_list_index_assignment_can_change_type(monkeypatch, capsys):
    code = '''create Items is listing: "sword", "shield"

define Play:
    index 0 of Items is 10
    output index 0 of Items
'''

    output = run_program(code, monkeypatch, capsys, slot=965)

    assert output == ["10"]


def test_e2e_type_error_for_non_int_index(monkeypatch, capsys):
    code = '''create Items is listing: "sword", "shield"

define Play:
    output index "zero" of Items
'''

    with pytest.raises(TypeCheckError):
        run_program(code, monkeypatch, capsys, slot=982)

