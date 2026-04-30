import pytest
from src.visitors.interpreter import *
from src.ast.nodes import *

def make_checker():
    return InterpreterVisitor()

def test_lookup():
    checker = make_checker()
    
    checker.v_tables = [{"X":1}]
    
    assert checker.lookup("X") == 1

def test_lookup_multiscope():
    checker = make_checker()
    
    checker.v_tables = [{"X":1},{"Y":2},{"Z":3}]
    
    assert checker.lookup("X") == 1

def test_lookup_shadowing():
    checker = make_checker()
    
    checker.v_tables = [{"X":1},{"X":2}]
    
    assert checker.lookup("X") == 2

def test_findscope():
    checker = make_checker()
    
    checker.v_tables = [{"X":1,"A":2},{"Y":2,"B":3},{"Z":3,"C":4}]
    
    assert checker.find_scope("X") == {"X":1,"A":2}

def test_findscope_shadowing():
    checker = make_checker()
    
    checker.v_tables = [{"X":1,"A":2},{"X":2,"B":3},{"Z":3,"C":4}]
    
    assert checker.find_scope("X") == {"X":2,"B":3}