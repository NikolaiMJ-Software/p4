import pytest
from src.visitors.interpreter import *
from src.ast.nodes import *

def make_checker():
    return InterpreterVisitor()

def test_unwrap():
    checker = make_checker()
    
    val = RuntimeValue("int",1)
    
    assert checker.unwrap(val) == 1

def test_unwrap_list():
    checker = make_checker()
    
    val = [RuntimeValue("float",4.4), [RuntimeValue("int",1), RuntimeValue("bool",True), [RuntimeValue("str","Bob"), RuntimeValue("int",32)]], RuntimeValue("str","Hell"), [RuntimeValue("float",7.6), RuntimeValue("str","69")]]
    
    assert checker.unwrap_list(val) == [4.4, [1, True, ['Bob', 32]], 'Hell', [7.6, '69']]