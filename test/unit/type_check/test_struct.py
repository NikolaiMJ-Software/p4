import pytest
from src.visitors.type_checker.type_checker import *
from src.ast.nodes import *

'''
-----------------
Passing unit test for the type checker
-----------------
'''
def test_struct_get_parent():
    v_table = {"Character":{"Health": "int(100)"}}
    node = CreateStruct("Warrior", ("Character", []))
    
    result = TypeChecker().check_create_struct(node, node.name in v_table, v_table["Character"])
    assert result is None

def test_struct_get_var():
    v_table = {"Warrior":{"Health": "int(100)", "Defense": "float(4.7)"}}
    node = Var("Defense", "Warrior")

    result = TypeChecker().check_var(node, v_table["Warrior"])
    assert result is None

def test_struct_change_var():
    v_table = {"Warrior":{"Health": "int(100)", "Defense": "float(4.7)"}}
    node = Assign("Health", "Warrior", IntLiteral(120))

    result = TypeChecker().check_assign(node, v_table["Warrior"])
    assert result is None


'''
-----------------
Failing unit test for the type checker
-----------------
'''
def test_struct_duplicate_name():
    v_table = {"Character": {"Health": "int(100)"}, "Warrior":{"Health": "int(100)"}}
    node = CreateStruct("Warrior", ("Character", []))

    with pytest.raises(TypeError, match="The struct: 'Warrior' already exists"):
        TypeChecker().check_create_struct(node, node.name in v_table, node.base in v_table)

def test_struct_undefined_parent():
    v_table = {"Character": {"Health": "int(100)"}}
    node = CreateStruct("Knight", ("Warrior", []))

    with pytest.raises(TypeError, match="The parent struct: 'Warrior' does not exist"):
        TypeChecker().check_create_struct(node, node.name in v_table, node.base in v_table)
   
def test_struct_undefined_struct():
    v_table = {"Character": {"Health": "int(100)"}}
    node = Var("Health", "Warrior")

    with pytest.raises(TypeError, match="The struct: 'Warrior' is not defined"):
        TypeChecker().check_var(node, node.base in v_table)

def test_struct_undefined_var():
    v_table = {"Character": {"Health": "int(100)"}}
    node = Var("Defense", "Character")

    with pytest.raises(TypeError, match="The variable: 'Defense' is not defined in the struct: 'Character'"):
        TypeChecker().check_var(node, node.base in v_table)
