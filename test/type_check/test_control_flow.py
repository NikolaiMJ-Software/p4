import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *

def make_checker():
    return TypeCheckerVisitor()


def test_if_valid():
    checker = make_checker()

    node = If(
        BoolLiteral(True),
        [CreateVariable("x", IntLiteral(1))],
        [(BoolLiteral(False), [CreateVariable("y", IntLiteral(2))])],
        [CreateVariable("z", IntLiteral(3))]
    )

    assert checker.visit(node) is None


def test_if_invalid_condition():
    checker = make_checker()

    node = If(
        IntLiteral(1),
        [CreateVariable("x", IntLiteral(1))],
        [],
        []
    )

    with pytest.raises(TypeError, match="if leftition must be bool"):
        checker.visit(node)


def test_if_invalid_elif_condition():
    checker = make_checker()

    node = If(
        BoolLiteral(True),
        [],
        [(IntLiteral(1), [CreateVariable("x", IntLiteral(1))])],
        []
    )

    with pytest.raises(TypeError, match="elif leftition must be bool"):
        checker.visit(node)


def test_if_creates_variable():
    checker = make_checker()

    node = If(
        BoolLiteral(True),
        [CreateVariable("x", IntLiteral(1))],
        [],
        []
    )

    checker.visit(node)

    assert "x" in checker.v_table
    assert checker.v_table["x"] == "int"


def test_if_else_creates_variable():
    checker = make_checker()

    node = If(
        BoolLiteral(False),
        [],
        [],
        [CreateVariable("y", IntLiteral(2))]
    )

    checker.visit(node)

    assert "y" in checker.v_table
    assert checker.v_table["y"] == "int"


def test_if_none_condition_skips_body():
    checker = make_checker()
    checker.v_table["cond"] = None

    node = If(
        Var("cond", None),
        [CreateVariable("x", IntLiteral(1))],
        [],
        []
    )

    assert checker.visit(node) is None
    assert "x" not in checker.v_table


def test_while_valid_and_scope_restored():
    checker = make_checker()
    checker.v_table["cond"] = "bool"

    node = While(
        Var("cond", None),
        [CreateVariable("x", IntLiteral(1))]
    )

    assert checker.visit(node) is None
    assert "x" not in checker.v_table


def test_while_invalid_condition():
    checker = make_checker()
    checker.v_table["cond"] = "int"

    node = While(
        Var("cond", None),
        []
    )

    with pytest.raises(TypeError, match="while leftition must be bool"):
        checker.visit(node)


def test_dowhile_valid_and_scope_restored():
    checker = make_checker()
    checker.v_table["cond"] = "bool"

    node = Dowhile(
        [CreateVariable("x", IntLiteral(1))],
        Var("cond", None)
    )

    assert checker.visit(node) is None
    assert "x" not in checker.v_table


def test_dowhile_invalid_condition():
    checker = make_checker()
    checker.v_table["cond"] = "int"

    node = Dowhile(
        [CreateVariable("x", IntLiteral(1))],
        Var("cond", None)
    )

    with pytest.raises(TypeError, match="dowhile leftition must be bool"):
        checker.visit(node)