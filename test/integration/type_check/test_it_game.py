import pytest
from src.errors import TypeError
from setup_type_checker import type_check_test
    
def test_game_struct_valid():
    code = """
create Game with:
    Healt is 10
    Gold is 0
"""
    result = type_check_test(code)
    assert result == []


def test_game_struct_empty_valid():
    code = """
create Game with:
    
"""
    result = type_check_test(code)
    assert result == []


def test_game_as_variable_invalid():
    code = """
create Game is 10
"""
    with pytest.raises(TypeError, match="The identifier 'Game' is reserved and can only be used as a struct name."):
        type_check_test(code)
        
def test_game_as_list_invalid():
    code = """
create Game is listing: 10, 2, 3
"""
    with pytest.raises(TypeError, match="The identifier 'Game' is reserved and can only be used as a struct name."):
        type_check_test(code)
        
def test_game_as_function_invalid():
    code = """
define Game:
    return 5\n
"""
    with pytest.raises(TypeError, match="The identifier 'Game' is reserved and can only be used as a struct name."):
        type_check_test(code)

def test_multiple_game_structs_invalid():
    code = """
create Game with:
    Hp is 10

create Game with:
    Gold is 0
"""
    with pytest.raises(TypeError, match="The struct: 'Game' already exists"):
        type_check_test(code)

def test_game_error_message():
    code = """
create Game is 10
"""
    with pytest.raises(TypeError, match="The identifier 'Game' is reserved and can only be used as a struct name."):
        type_check_test(code)