import pytest

from setup_e2e import *
from src.errors import TypeError as TypeCheckError
from src.errors import InterpreterError


def test_e2e_type_error_is_raised(monkeypatch, capsys):
    code = '''create Number is 10

define Play:
    output Number + "text"
'''

    with pytest.raises(TypeCheckError, match="Expected numeric types on operation: \\+, got 'int' and 'str'") as info:
        run_program(code, monkeypatch, capsys)
        
    error = info.value
    
    assert error.line == 4
    assert error.column == 12

    expected_context = '''    output Number + "text"
           ^'''
    assert error.context == expected_context


def test_e2e_type_error_for_bad_arithmetic(monkeypatch, capsys):
    code = '''create Number is 10
create Text is "hello"

define Play:
    output Number + Text
'''

    with pytest.raises(TypeCheckError, match="Expected numeric types on operation: \\+, got 'int' and 'str'") as info:
        run_program(code, monkeypatch, capsys)

    error = info.value
    
    assert error.line == 5
    assert error.column == 12

    expected_context = '''    output Number + Text
           ^'''
    assert error.context == expected_context


def test_e2e_type_error_for_wrong_function_arg_count(monkeypatch, capsys):
    code = '''define AddNumbers with A, B:
    return A + B

define Play:
    call AddNumbers with 10
'''

    with pytest.raises(InterpreterError, match="Function 'AddNumbers' expects 2 args, got 1") as info:
        run_program(code, monkeypatch, capsys)
    
    error = info.value
    
    assert error.line == 5
    assert error.column == 5

    expected_context = '''    call AddNumbers with 10
    ^'''
    assert error.context == expected_context




def test_e2e_chance_rejects_string(monkeypatch, capsys):
    code = '''create CriticalHit

define Play:
    CriticalHit is chance "yes" in 100
'''

    with pytest.raises(TypeCheckError, match="chance requires numeric types, got 'str' and 'int'") as info:
        run_program(code, monkeypatch, capsys)
        
    error = info.value
    
    assert error.line == 4
    assert error.column == 20

    expected_context = '''    CriticalHit is chance "yes" in 100
                   ^'''
    assert error.context == expected_context



def test_e2e_between_rejects_string(monkeypatch, capsys):
    code = '''create Health

define Play:
    Health is between "low" and 100
'''

    with pytest.raises(TypeCheckError, match="between requires numeric types, got 'str' and 'int'") as info:
        run_program(code, monkeypatch, capsys)

    error = info.value
    
    assert error.line == 4
    assert error.column == 15

    expected_context = '''    Health is between "low" and 100
              ^'''
    assert error.context == expected_context

def test_e2e_division_by_zero_raises(monkeypatch, capsys):
    code = '''define Play:
    output 10 / 0
'''

    with pytest.raises(InterpreterError, match="division by 0") as info:
        run_program(code, monkeypatch, capsys)
    
    error = info.value
    
    assert error.line == 2
    assert error.column == 17

    expected_context = (
        "    output 10 / 0\n"
        + " " * (error.column - 1)
        + "^"
    )

    assert error.context == expected_context