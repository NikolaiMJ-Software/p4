import pytest

from setup_e2e import run_program
from src.errors import TypeError as TypeCheckError
from src.errors import InterpreterError

def test_e2e_function_call_typechecks_dynamically(monkeypatch, capsys):
    code = '''create Answer

define Play:
    call Ask

define Ask:
    input in Answer
    if Answer equal "yes" do:
        output "accepted"
''' 

    output = run_program(code, monkeypatch, capsys, inputs=["yes"])

    assert output == ["accepted"]


def test_e2e_function_arguments_keep_runtime_types(monkeypatch, capsys):
    code = '''define AddNumbers with Y, V:
    return Y + V

create Number1 is 10
create Number2 is 25

define Play:
    output Number1 + Number2
    output call AddNumbers with Number1, Number2
'''

    output = run_program(code, monkeypatch, capsys)

    assert output == ["35", "35"]


def test_e2e_function_return_value(monkeypatch, capsys):
    code = '''define AddNumbers with A, B:
    return A + B

define Play:
    output call AddNumbers with 10, 25
'''

    output = run_program(code, monkeypatch, capsys)

    assert output == ["35"]


def test_e2e_function_return_wrong_type_raises(monkeypatch, capsys):
    code = '''define BadAdd with A:
    return A + "text"

define Play:
    output call BadAdd with 10
'''

    with pytest.raises(TypeCheckError, match="Expected numeric types, got int and str"):
        run_program(code, monkeypatch, capsys)


def test_e2e_function_parameter_does_not_leak(monkeypatch, capsys):
    code = '''define Show with X:
    output X

define Play:
    call Show with 10
    output X
'''

    with pytest.raises(TypeCheckError, match="The variable: 'X' does not exist"):
        run_program(code, monkeypatch, capsys)