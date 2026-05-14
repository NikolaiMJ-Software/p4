import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *

def test_create_variable():
    v_table = {}
    node = CreateVariable("x", IntLiteral(5))

    result = TypeChecker().check_create_variable(node, node.name in v_table)

    assert result is None


def test_create_variable_without_value():
    v_table = {}
    node = CreateVariable("x", None)

    result = TypeChecker().check_create_variable(node, node.name in v_table)
    
    assert result is None


def test_create_variable_duplicate_fails():
    v_table = {"x": "int(5)"}
    node = CreateVariable("x", IntLiteral(10))

    with pytest.raises(TypeError, match="already exist"):
        TypeChecker().check_create_variable(node, node.name in v_table)


def test_visit_var_existing_variable():
    v_table = {"v": "int(1)"}
    node = Var("v", None)

    result = TypeChecker().check_var(node, node.name in v_table)

    assert result is None


def test_visit_var_missing_variable_fails():
    v_table = {}
    node = Var("x", None)

    with pytest.raises(TypeError, match="does not exist"):
        TypeChecker().check_var(node, node.name in v_table)


def test_assign_existing_variable():
    v_table = {"v": "int(1)"}
    node = Assign("v", None, IntLiteral(54))

    result = TypeChecker().check_assign(node, node.name in v_table)

    assert result is None


def test_assign_missing_variable_fails():
    v_table = {}
    node = Assign("v", None, StringLiteral("hello"))

    with pytest.raises(TypeError, match="does not exist"):
        TypeChecker().check_assign(node, node.name in v_table)


def test_assign_existing_variable_updates_type():
    v_table = {"v": "int(1)"}
    node = Assign("v", None, StringLiteral("hello"))

    result = TypeChecker().check_assign(node, node.name in v_table)

    assert result is None


def test_assign_list_variable_updates_type():
    v_table = {"xs": "[int(1)]"}
    node = Assign("xs", None, StringLiteral("hello"))

    result = TypeChecker().check_assign(node, node.name in v_table)

    assert result is None