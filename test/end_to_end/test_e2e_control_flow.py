import pytest

from setup_e2e import *
from src.errors import TypeError as TypeCheckError
from src.errors import InterpreterError


def test_e2e_loop_with_stop(monkeypatch, capsys):
    code = '''create Answer

define Play:
    while true do:
        input in Answer
        if Answer equal "stop" do:
            output "stopped"
            stop
        else do:
            output "again"
'''

    output = run_program(code, monkeypatch, capsys, inputs=["hello", "stop"])

    assert output == ["again", "stopped"]


def test_e2e_for_range_loop(monkeypatch, capsys):
    code = '''define Play:
    for each I from 1 to 3 do:
        output I
'''

    output = run_program(code, monkeypatch, capsys)

    assert output == ["1", "2", "3"]


def test_e2e_foreach_loop(monkeypatch, capsys):
    code = '''create Items is listing: "sword", "shield", "potion"

define Play:
    for each Item in Items do:
        output Item
'''

    output = run_program(code, monkeypatch, capsys)

    assert output == ["sword", "shield", "potion"]


def test_e2e_else_if_branch(monkeypatch, capsys):
    code = '''create Answer

define Play:
    input in Answer
    if Answer equal "yes" do:
        output "yes branch"
    else if Answer equal "maybe" do:
        output "maybe branch"
    else do:
        output "else branch"
'''

    output = run_program(code, monkeypatch, capsys, inputs=["maybe"])

    assert output == ["maybe branch"]


def test_e2e_do_while_runs_before_condition(monkeypatch, capsys):
    code = '''create X is 0

define Play:
    do:
        output "ran"
    while false
'''

    output = run_program(code, monkeypatch, capsys,)

    assert output == ["ran"]