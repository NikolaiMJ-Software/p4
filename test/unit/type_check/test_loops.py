import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *

def make_checker():
    return TypeCheckerVisitor()


def test_forrange_valid():
    checker = make_checker()

    node = Forrange(
        "i",
        IntLiteral(1),
        IntLiteral(10),
        [CreateVariable("x", IntLiteral(2))]
    )

    assert checker.visit(node) is None
    assert "i" not in checker.v_table
    assert "x" not in checker.v_table


def test_forrange_invalid_bounds():
    checker = make_checker()

    node = Forrange(
        "i",
        StringLiteral("a"),
        IntLiteral(10),
        []
    )

    with pytest.raises(TypeError, match="for-range bounds must be numeric"):
        checker.visit(node)


def test_foreach_valid():
    checker = make_checker()
    checker.v_table["xs"] = "list[int]"

    node = Foreach(
        "item",
        "xs",
        [CreateVariable("y", Add(Var("item", None), IntLiteral(1)))]
    )

    assert checker.visit(node) is None
    assert "item" not in checker.v_table
    assert "y" not in checker.v_table


def test_foreach_missing_collection_fails():
    checker = make_checker()

    node = Foreach("item", "xs", [])

    with pytest.raises(TypeError, match="does not exist"):
        checker.visit(node)


def test_foreach_non_list_fails():
    checker = make_checker()
    checker.v_table["xs"] = "int"

    node = Foreach("item", "xs", [])

    with pytest.raises(TypeError, match="Cannot iterate over non-list type"):
        checker.visit(node)