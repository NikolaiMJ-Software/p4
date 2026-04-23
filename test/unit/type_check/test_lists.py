import pytest
from src.ast.nodes import Return, Var
from src.visitors.type_checker import *
from src.ast.nodes import *

def make_checker():
    return TypeCheckerVisitor()


'''
-----------------
Passing unit test for the type checker
-----------------
'''
def test_create_int_list():
    checker = make_checker()

    node = CreateList("xs", [IntLiteral(1), IntLiteral(2), IntLiteral(3)])
    assert checker.visit(node) == ['int', 'int', 'int']
    assert checker.v_table["xs"] == ['int', 'int', 'int']


def test_create_list_mixed_types_pass():
    checker = make_checker()
    node = CreateList("xs", [IntLiteral(1), StringLiteral("a")])
    assert checker.visit(node) == ['int', 'str']
    assert checker.v_table["xs"] == ['int', 'str']


def test_index_access_typed_list():
    checker = make_checker()
    checker.v_table["xs"] = ['int']

    node = IndexAccess([IntLiteral(0)], "xs", None)
    assert checker.visit(node) == "int"


def test_assign_to_list_index():
    checker = make_checker()
    checker.v_table["xs"] = ['int']

    node = AssignIndex(
        IndexAccess([IntLiteral(0)], "xs", None),
        IntLiteral(99)
    )

    assert checker.visit(node) == "int"


'''
-----------------
Failing unit test for the type checker
-----------------
'''
def test_create_two_lists_with_same_name():
    checker = make_checker()
    checker.v_table["X"] = ['int']

    node = IndexAccess([IntLiteral(1)], "X", None)

    with pytest.raises(TypeError, match="does not exist"):
        checker.visit(node)

def test_index_access_not_initilized_list_fails():
    checker = make_checker()
    checker.v_table["xs"] = ['int']

    node = IndexAccess([StringLiteral("0")], "notalist", None)

    with pytest.raises(TypeError, match="List index must be int"):
        checker.visit(node)

def test_index_access_out_of_bound_negative():
    checker = make_checker()
    checker.v_table["xs"] = ['int', 'float', 'str']
    
    node = IndexAccess([Neg(IntLiteral(1))], "xs", None)
    with pytest.raises(TypeError, match="The index: '-1' does not exist in 'xs'"):
        checker.visit(node)

def test_index_access_out_of_bound_max():
    checker = make_checker()
    checker.v_table["xs"] = ['int', 'float', 'str']
    
    node = IndexAccess([IntLiteral(4)], "xs", None)
    with pytest.raises(TypeError, match="The index: '4' does not exist in 'xs'"):
        checker.visit(node)