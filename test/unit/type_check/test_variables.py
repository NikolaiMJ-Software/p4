import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *

def make_checker():
    return TypeCheckerVisitor()


def test_create_variable():
    checker = make_checker()

    assert checker.visit(CreateVariable("x", IntLiteral(5))) == "int"
    assert checker.v_table["x"] == "int"


def test_create_variable_without_value():
    checker = make_checker()

    assert checker.visit(CreateVariable("x", None)) is None
    assert "x" in checker.v_table
    assert checker.v_table["x"] is None


def test_create_variable_duplicate_fails():
    checker = make_checker()
    checker.visit(CreateVariable("x", IntLiteral(5)))

    with pytest.raises(TypeError, match="already exist"):
        checker.visit(CreateVariable("x", IntLiteral(10)))


def test_visit_var_existing_variable():
    checker = make_checker()
    checker.v_table["x"] = "int"

    assert checker.visit(Var("x", None)) == "int"


def test_visit_var_missing_variable_fails():
    checker = make_checker()

    with pytest.raises(TypeError, match="does not exist"):
        checker.visit(Var("x", None))


def test_assign_existing_variable():
    checker = make_checker()
    checker.v_table["x"] = "int"

    assert checker.visit(Assign("x", None, IntLiteral(10))) == "int"
    assert checker.v_table["x"] == "int"


def test_assign_missing_variable_fails():
    checker = make_checker()

    with pytest.raises(TypeError, match="does not exist"):
        checker.visit(Assign("x", None, IntLiteral(10)))

def test_assign_existing_variable_updates_type():
    checker = make_checker()
    checker.v_table["x"] = "int"

    result = checker.visit(Assign("x", None, StringLiteral("hello")))

    assert result == "str"
    assert checker.v_table["x"] == "str"


def test_assign_list_variable_updates_type():
    checker = make_checker()
    checker.v_table["xs"] = "list[int]"

    result = checker.visit(Assign("xs", None, StringLiteral("hello")))

    assert result == "str"
    assert checker.v_table["xs"] == "str"