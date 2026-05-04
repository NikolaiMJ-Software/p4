import pytest

from setup_e2e import run_program
from src.errors import TypeError as TypeCheckError
from src.errors import InterpreterError


def test_e2e_string_concatenation(monkeypatch, capsys):
    code = '''create First is "Hello "
create Second is "World"

define Play:
    output First + Second
'''

    output = run_program(code, monkeypatch, capsys)

    assert output == ["Hello World"]


def test_e2e_between_can_assign_numeric_value(monkeypatch, capsys):
    code = '''create Health

define Play:
    Health is between 1 and 1
    output Health
'''

    output = run_program(code, monkeypatch, capsys)

    assert output == ["1"]


def test_e2e_chance_returns_bool(monkeypatch, capsys):
    code = '''create CriticalHit

define Play:
    CriticalHit is chance 1 in 1
    if CriticalHit do:
        output "critical"
    else do:
        output "normal"
'''

    output = run_program(code, monkeypatch, capsys)

    assert output == ["critical"]


def test_e2e_unary_negative_number(monkeypatch, capsys):
    code = '''create X is -5

define Play:
    output X
'''

    output = run_program(code, monkeypatch, capsys)

    assert output == ["-5"]