import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

import pytest
from src.parser import parse, ParseError

#############
# Functions #
#############

def test_define_function():
    code = """define X:
    return V
    
    """

    tree = parse(code)
    
    assert tree.children[0].data == "func_def"
    
def test_define_func_param():
    code = """define Y with A, B, C:
    X is A+B+C
    return X
    """
    tree = parse(code)
    
    assert tree.children[0].data == "func_def"


def test_call():
    tree = parse("call Function\n")
    assert tree.children[0].data == "expr_stmt"

def test_call_param():
    tree = parse("call Function with 1, 2\n")
    assert tree.children[0].data == "expr_stmt"

def test_call_inside_assignment():
    tree = parse("X is call Damage with 1, 2\n")
    node = tree.children[0]

    assert node.data == "assign_stmt"


def test_call_inside_output():
    tree = parse("output call GetHealth\n")
    node = tree.children[0]

    assert node.data == "output_stmt"


def test_call_inside_create():
    tree = parse("create X is call Roll with 1, 2\n")
    node = tree.children[0]

    assert node.data == "create_v"

