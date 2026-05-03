import pytest

from test.end_to_end.setup_e2e import run_program
from src.errors import TypeError as TypeCheckError
from src.errors import InterpreterError


def test_e2e_type_error_is_raised(monkeypatch, capsys):
    code = '''create Number is 10

define Play:
    output Number + "text"
'''

    with pytest.raises(TypeCheckError):
        run_program(code, monkeypatch, capsys, slot=992)


def test_e2e_type_error_for_bad_arithmetic(monkeypatch, capsys):
    code = '''create Number is 10
create Text is "hello"

define Play:
    output Number + Text
'''

    with pytest.raises(TypeCheckError):
        run_program(code, monkeypatch, capsys, slot=983)


def test_e2e_type_error_for_wrong_function_arg_count(monkeypatch, capsys):
    code = '''define AddNumbers with A, B:
    return A + B

define Play:
    call AddNumbers with 10
'''

    with pytest.raises(TypeCheckError):
        run_program(code, monkeypatch, capsys, slot=981)


def test_e2e_if_condition_must_be_bool(monkeypatch, capsys):
    code = '''create X is 10

define Play:
    if X do:
        output "bad"
'''

    with pytest.raises(TypeCheckError):
        run_program(code, monkeypatch, capsys, slot=970)


def test_e2e_chance_rejects_string(monkeypatch, capsys):
    code = '''create CriticalHit

define Play:
    CriticalHit is chance "yes" in 100
'''

    with pytest.raises(TypeCheckError):
        run_program(code, monkeypatch, capsys, slot=968)


def test_e2e_between_rejects_string(monkeypatch, capsys):
    code = '''create Health

define Play:
    Health is between "low" and 100
'''

    with pytest.raises(TypeCheckError):
        run_program(code, monkeypatch, capsys, slot=967)


def test_e2e_division_by_zero_raises(monkeypatch, capsys):
    code = '''define Play:
    output 10 / 0
'''

    with pytest.raises(InterpreterError):
        run_program(code, monkeypatch, capsys, slot=966)