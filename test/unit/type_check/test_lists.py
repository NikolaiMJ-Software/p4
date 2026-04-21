import pytest
from src.ast.nodes import Return, Var
from src.visitors.type_checker import *
from src.ast.nodes import *

def make_checker():
    return TypeCheckerVisitor()


def test_create_empty_list():
    checker = make_checker()

    assert checker.visit(CreateList("xs", None)) == "list"
    assert checker.v_table["xs"] == "list"


def test_create_typed_list():
    checker = make_checker()

    node = CreateList("xs", [IntLiteral(1), IntLiteral(2), IntLiteral(3)])
    assert checker.visit(node) == "list[int]"
    assert checker.v_table["xs"] == "list[int]"


def test_create_list_mixed_types_fails():
    checker = make_checker()

    node = CreateList("xs", [IntLiteral(1), StringLiteral("a")])

    with pytest.raises(TypeError, match="mixed types"):
        checker.visit(node)


def test_index_access_typed_list():
    checker = make_checker()
    checker.v_table["xs"] = "list[int]"

    node = IndexAccess([IntLiteral(0)], "xs", None)
    assert checker.visit(node) == "int"


def test_index_access_generic_list_returns_none():
    checker = make_checker()
    checker.v_table["xs"] = "list"

    node = IndexAccess([IntLiteral(0)], "xs", None)
    assert checker.visit(node) is None


def test_index_access_non_int_index_fails():
    checker = make_checker()
    checker.v_table["xs"] = "list[int]"

    node = IndexAccess([StringLiteral("0")], "xs", None)

    with pytest.raises(TypeError, match="List index must be int"):
        checker.visit(node)


def test_index_access_non_list_fails():
    checker = make_checker()
    checker.v_table["x"] = "int"

    node = IndexAccess([IntLiteral(0)], "x", None)

    with pytest.raises(TypeError, match="Cannot index non-list type"):
        checker.visit(node)


def test_assign_to_list_index_valid():
    checker = make_checker()
    checker.v_table["xs"] = "list[int]"

    node = Assign(
        IndexAccess([IntLiteral(0)], "xs", None),
        None,
        IntLiteral(99)
    )

    assert checker.visit(node) == "int"


def test_assign_to_list_index_wrong_value_type_fails():
    checker = make_checker()
    checker.v_table["xs"] = "list[int]"

    node = Assign(
        IndexAccess([IntLiteral(0)], "xs", None),
        None,
        StringLiteral("oops")
    )

    with pytest.raises(TypeError, match="Cannot assign value of type"):
        checker.visit(node)