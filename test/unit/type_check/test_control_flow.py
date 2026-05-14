import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *
from src.errors import TypeError


def test_if_valid():
    node = If(BoolLiteral(True), [], [], [])

    assert TypeChecker().check_if(node, "bool", "if") == "bool"


def test_if_invalid_condition():
    node = If(IntLiteral(1), [], [], [])

    with pytest.raises(TypeError, match="if condition must be bool, got int"):
        TypeChecker().check_if(node, "int", "if")


def test_if_invalid_elif_condition():
    node = If(BoolLiteral(True), [], [], [])

    with pytest.raises(TypeError, match="elif condition must be bool, got int"):
        TypeChecker().check_if(node, "int", "elif")


def test_if_none_condition_skips_body():
    node = If(Var("cond", None), [], [], [])

    assert TypeChecker().check_if(node, None, "if") is None


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