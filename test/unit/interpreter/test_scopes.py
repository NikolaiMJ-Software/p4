import pytest
from src.visitors.interpreter import *
from src.ast.nodes import *

def make_checker():
    return InterpreterVisitor()

def test_lookup():
    checker = make_checker()
    
    checker.v_table = {"X":int(1)}
    
    assert checker.unwrap(checker.lookup_var("X")) == 1

def test_lookup_multiscope():
    checker = make_checker()
    
    checker.v_table = {"Z":int(3),"__parent__":{"Y":int(2),"__parent__":{"X":int(1)}}}
    
    assert checker.unwrap(checker.lookup_var("X")) == 1

def test_lookup_shadowing():
    checker = make_checker()
    
    checker.v_table = {"X":2,"__parent__":{"X":1}}
    
    assert checker.unwrap(checker.lookup_var("X")) == 2
