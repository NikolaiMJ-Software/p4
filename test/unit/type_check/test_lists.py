import pytest
from src.visitors.type_checker import TypeChecker
from src.ast.nodes import *
from src.errors import TypeError


'''
-----------------
Passing unit test for the type checker
-----------------
'''

def test_create_int_list():
    node = CreateList("xs", [IntLiteral(1), IntLiteral(2), IntLiteral(3)])

    result = TypeChecker().check_create_list(node, False)

    assert result is None


def test_create_list_mixed_types_pass():
    node = CreateList("xs", [IntLiteral(1), StringLiteral("a")])

    result = TypeChecker().check_create_list(node, False)

    assert result is None


def test_index_access_with_int_index_passes():
    node = IndexAccess([IntLiteral(0)], "xs", None)

    result = TypeChecker().check_index_access(node, "int")

    assert result is None


def test_foreach_existing_list_passes():
    node = Foreach("Item", "xs", [])

    result = TypeChecker().check_foreach(node, ["int", "str"])

    assert result is None


'''
-----------------
Failing unit test for the type checker
-----------------
'''

def test_create_two_lists_with_same_name():
    node = CreateList("X", [IntLiteral(1)])

    with pytest.raises(TypeError, match="already exists"):
        TypeChecker().check_create_list(node, True)


def test_index_access_with_string_index_fails():
    node = IndexAccess([StringLiteral("0")], "xs", None)

    with pytest.raises(TypeError, match="List index must be 'int', got a 'str'"):
        TypeChecker().check_index_access(node, "str")


def test_foreach_missing_list_fails():
    node = Foreach("Item", "xs", [])

    with pytest.raises(TypeError, match="The list: 'xs' does not exist"):
        TypeChecker().check_foreach(node, False)


def test_foreach_non_list_fails():
    node = Foreach("Item", "xs", [])

    with pytest.raises(TypeError, match="Cannot iterate over non-list type 'int'"):
        TypeChecker().check_foreach(node, "int")