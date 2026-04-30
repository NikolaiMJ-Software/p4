import pytest
from src.visitors.interpreter import *
from src.ast.nodes import *

def make_checker():
    return InterpreterVisitor()

def test_runtimetype_empty():
    checker = make_checker()
    
    val = None
    
    assert checker.runtime_to_type(val) == None

def test_runtimetype_runtimevalue():
    checker = make_checker()
    
    val = RuntimeValue("int", 1)
    
    assert checker.runtime_to_type(val) == "int"

def test_runtimetype_list():
    checker = make_checker()
    
    val = [RuntimeValue("bool",1),RuntimeValue("int",2),RuntimeValue("str","3")]
    
    assert checker.runtime_to_type(val) == ["bool","int","str"]

def test_runtimetype_dict():
    checker = make_checker()
    
    val = {"X":RuntimeValue("int",1)}
    
    assert checker.runtime_to_type(val) == {"X":"int"}

def test_sync_typechecker():
    checker = make_checker()
    
    checker.v_table = {"X":RuntimeValue("bool",1),"Y":RuntimeValue("int",2),"__parent__":{"X":RuntimeValue("int",0),"Z":RuntimeValue("str","3")}}
    checker.sync_type_checker()
    
    assert checker.type_checker.v_table == {"X":"bool","Y":"int","Z":"str"}

def test_unwrap():
    checker = make_checker()
    
    val = RuntimeValue("int",1)
    
    assert checker.unwrap(val) == 1

def test_checkexpressiontype():
    checker = make_checker()
    
    checker.v_table = {"X":RuntimeValue("bool",0)}
    node = Var("X")
    
    assert checker.check_expression_type(node) == "bool"