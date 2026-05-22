import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

import pytest
from src.parser import parse, ParseError


################
# Control Flow #
################

def test_if_stmt():
    code = """if true do:
    X is 5
    create Y
    output Y, X, "cake"
    """
    
    tree = parse(code)
    
    assert tree.children[0].data == "if_stmt"

def test_if_else_stmt():
    code = """if true do:
    X is 5
    create Y
    output Y
else do:
    output 0
    """
    
    tree = parse(code)
    
    assert tree.children[0].data == "if_stmt"

def test_if_elif_else():
    code = """if true do:
    output 1
else if false do:
    output 2
else do:
    output 3
"""
    tree = parse(code)
    assert tree.children[0].data == "if_stmt"


def test_while_loop():
    code ="""while true do:
    X is X+1
    """
    tree = parse(code)

    assert tree.children[0].data == "while_stmt"

def test_do_while():
    code = """do:
    Y is Y-1
while true

"""
    
    tree = parse(code)
    
    assert tree.children[0].data == "dowhile_stmt"
def test_stop_inside_while():
    code = """while true do:
    stop
"""
    tree = parse(code)

    assert tree.children[0].data == "while_stmt"


def test_return_inside_if_function():
    code = """define X:
    if true do:
        return 1
"""
    tree = parse(code)

    assert tree.children[0].data == "func_def"
    
