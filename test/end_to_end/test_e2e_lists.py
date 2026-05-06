import pytest

from setup_e2e import *
from src.errors import TypeError as TypeCheckError
from src.errors import InterpreterError


def test_e2e_list_index_output(monkeypatch, capsys):
    code = '''create Items is listing: "sword", "shield", "potion"

define Play:
    output index 0 of Items
    output index 2 of Items
'''

    output = run_program(code, monkeypatch, capsys)

    assert output == ["sword", "potion"]


def test_e2e_list_index_assignment(monkeypatch, capsys):
    code = '''create Items is listing: "sword", "shield", "potion"

define Play:
    index 1 of Items is "axe"
    output index 1 of Items
'''

    output = run_program(code, monkeypatch, capsys)

    assert output == ["axe"]


def test_e2e_list_index_assignment_can_change_type(monkeypatch, capsys):
    code = '''create Items is listing: "sword", "shield"

define Play:
    index 0 of Items is 10
    output index 0 of Items
'''

    output = run_program(code, monkeypatch, capsys)

    assert output == ["10"]


def test_e2e_type_error_for_non_int_index(monkeypatch, capsys):
    code = '''create Items is listing: "sword", "shield"

define Play:
    output index "zero" of Items
'''

    with pytest.raises(TypeCheckError, match="List index must be int, got str"):
        run_program(code, monkeypatch, capsys)


def test_e2e_nested_list_index_access(monkeypatch, capsys):
    code = '''create X is listing: 1, 2, 3
index 2 of X is listing: 4, 5
index 1 of X is listing: 2.1, 2.3, 2.5
index 0 of index 2 of X is listing: 4, "he he", 9.2
output X

create Y is 0
create Z is 2
output index 2 of index Y of index Z of X       # 9.2
output index 2 of index Y of index Z + 1 of X   # <----- Error
'''
    with pytest.raises(TypeCheckError, match="The index: '3' does not exist in 'X'"):
        output = run_program(code, monkeypatch, capsys)
        assert output == ["[1, [2.1, 2.3, 2.5], [[4, 'he he', 9.2], 5]]", "9.2"]