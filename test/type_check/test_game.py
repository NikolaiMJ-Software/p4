import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

import pytest
from parser import parse
from src.ast.builder import ASTBuilder
from src.visitors.type_checker import TypeCheckerVisitor


def type_check(code):
    tree = parse(code)
    ast = ASTBuilder().transform(tree)
    checker = TypeCheckerVisitor()

    for stmt in ast:
        checker.visit(stmt)
    
    
def test_game_struct_valid():
    code = """
create Game with:
    Healt is 10
    Gold is 0
"""
    type_check(code)
    
def test_game_struct_empty_valid():
    code = """
create Game with:
    
"""
    type_check(code)
    
def test_game_as_variable_invalid():
    code = """
create Game is 10
"""
    with pytest.raises(TypeError):
        type_check(code)
        
def test_game_as_list_invalid():
    code = """
create Game listing: 10, 2, 3
"""
    with pytest.raises(TypeError):
        type_check(code)
        
def test_game_as_function_invalid():
    code = """
define Game:
    return 5\n
"""
    with pytest.raises(TypeError):
        type_check(code)

def test_multiple_game_structs_invalid():
    code = """
create Game with:
    Hp is 10

create Game with:
    Gold is 0
"""
    with pytest.raises(TypeError):
        type_check(code)

def test_game_error_message():
    code = """
create Game is 10
"""
    with pytest.raises(TypeError, match="Game"):
        type_check(code)