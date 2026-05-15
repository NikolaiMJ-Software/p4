import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *
from src.errors import TypeError

def test_while_valid():
    node = While(Var("cond", None), [])

    assert TypeChecker().check_while(node, "bool") == "bool"


def test_while_invalid_condition():
    node = While(Var("cond", None), [])

    with pytest.raises(TypeError, match="while condition must be bool, got int"):
        TypeChecker().check_while(node, "int")


def test_dowhile_valid():
    node = Dowhile([], Var("cond", None))

    assert TypeChecker().check_dowhile(node, "bool") == "bool"


def test_dowhile_invalid_condition():
    node = Dowhile([], Var("cond", None))

    with pytest.raises(TypeError, match="dowhile condition must be bool, got int"):
        TypeChecker().check_dowhile(node, "int")