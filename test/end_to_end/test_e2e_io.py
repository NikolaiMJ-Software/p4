import pytest

from setup_e2e import *
from src.errors import TypeError as TypeCheckError
from src.errors import InterpreterError

def test_e2e_input_then_string_comparison(monkeypatch, capsys):
    code = '''create Answer

define Play:
    input in Answer
    if Answer equal "yes" do:
        output "worked"
    else do:
        output "failed"
'''

    output = run_program(code, monkeypatch, capsys, inputs=["yes"])

    assert output == ["worked"]


def test_e2e_input_else_branch(monkeypatch, capsys):
    code = '''create Answer

define Play:
    input in Answer
    if Answer equal "yes" do:
        output "worked"
    else do:
        output "failed"
'''

    output = run_program(code, monkeypatch, capsys, inputs=["no"])

    assert output == ["failed"]