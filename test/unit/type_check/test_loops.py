import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *


def test_forrange_valid_int_bounds():
    node = Forrange("i", IntLiteral(1), IntLiteral(10), [])

    result = TypeChecker().check_forrange(node, "int", "int")

    assert result is None


def test_forrange_valid_float_bounds():
    node = Forrange("i", FloatLiteral(1.5), FloatLiteral(10.5), [])

    result = TypeChecker().check_forrange(node, "float", "float")

    assert result is None


def test_forrange_valid_mixed_numeric_bounds():
    node = Forrange("i", IntLiteral(1), FloatLiteral(10.5), [])

    result = TypeChecker().check_forrange(node, "int", "float")

    assert result is None


def test_foreach_valid():
    node = Foreach("item", "xs", [])

    result = TypeChecker().check_foreach(node, ["int", "int", "float"])

    assert result is None


def test_forrange_invalid_start_bound():
    node = Forrange("i", StringLiteral("a"), IntLiteral(10), [])

    with pytest.raises(TypeError, match="for-range bounds must be numeric"):
        TypeChecker().check_forrange(node, "str", "int")


def test_forrange_invalid_end_bound():
    node = Forrange("i", IntLiteral(1), StringLiteral("a"), [])

    with pytest.raises(TypeError, match="for-range bounds must be numeric"):
        TypeChecker().check_forrange(node, "int", "str")


def test_foreach_missing_collection_fails():
    node = Foreach("item", "xs", [])

    with pytest.raises(TypeError, match="The list: 'xs' does not exist"):
        TypeChecker().check_foreach(node, False)


def test_foreach_non_list_fails():
    node = Foreach("item", "xs", [])

    with pytest.raises(TypeError, match="Cannot iterate over non-list type 'int'"):
        TypeChecker().check_foreach(node, "int")