import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *
from test.type_check.integration.struct_it_test import typecheck_test

'''
-----------------
Passing integration test for the type checker
-----------------
'''
def test_it_pass_struct_get_parrent():
    get_parrent = typecheck_test(get_parrent_code)
    assert [None, None] == get_parrent
get_parrent_code = """create Character with:
    Health is 100
    Attack is 5
    Defense
    Name
create Warrior from Character with:
    
"""

def test_it_pass_struct_overwrite():
    overwrite = typecheck_test(overwrite_parrent_var_code)
    assert [None, None, None, None, None] == overwrite
overwrite_parrent_var_code = """create Character with:
    Health is 100
    Attack is 5
    Defense
    Name
create Warrior from Character with:
    Attack is 3
    Defense is 2
create Knight from Warrior with:
    Defense is 5
    Speed is -2
create Me from Knight with:
    
create Enemy from Knight with:
    
"""

def test_it_pass_struct_get_var():
    get_var = typecheck_test(get_var_code)
    assert [None, None, None, None, None, "int"] == get_var
get_var_code = """create Character with:
    Health is 100
    Attack is 5
    Defense
    Name
create Warrior from Character with:
    Attack is 3
    Defense is 2
create Knight from Warrior with:
    Defense is 5
    Speed is -2
create Me from Knight with:
    
create Enemy from Knight with:
    
Health from Enemy
"""    

def test_it_pass_struct_change_var():
    change_var = typecheck_test(change_var_code)
    assert [None, None, None, None, None, "int"] == change_var
change_var_code = """create Character with:
    Health is 100
    Attack is 5
    Defense
    Name
create Warrior from Character with:
    Attack is 3
    Defense is 2
create Knight from Warrior with:
    Defense is 5
    Speed is -2
create Me from Knight with:
    
create Enemy from Knight with:
    
Health from Enemy is Health from Enemy - Attack from Me
"""

def test_it_pass_struct_get_and_change_var():
    change_name_res = typecheck_test(change_name_code)
    assert [None, None, None, None, None, None, None, "str", "str", None] == change_name_res
change_name_code = """create Character with:
    Health is 100
    Attack is 5
    Defense
    Name
create Warrior from Character with:
    Attack is 3
    Defense is 2
create Knight from Warrior with:
    Defense is 5
    Speed is -2
create Me from Knight with:
    
create Enemy from Knight with:
    
Name from Enemy
Name from Me
Name from Enemy is "Bob"
Name from Enemy
Name from Me
"""

'''
-----------------
Failing integration test for the type checker
-----------------
'''
def test_it_fail_struct_duplicate_name():
    with pytest.raises(TypeError) as exc_info:
        typecheck_test(duplicate_struct_name_code)
    assert str(exc_info.value) == "The struct: 'Character' already exist"
duplicate_struct_name_code = """create Character with:
    Health is 100
    Attack is 5
    Defense
    Name
create Character with:
    Speed
"""    

def test_it_fail_struct_undefined_parrent():
    with pytest.raises(TypeError) as exc_info:
        typecheck_test(wrong_parrent_code)
    assert str(exc_info.value) == "The parrent struct: 'Person' don't exist"
wrong_parrent_code = """create Character with:
    Health is 100
    Attack is 5
    Defense
    Name
create Warrior from Person with:
    Attack is 3
    Defense is 2
"""    

def test_it_fail_struct_undefined_struct():
    with pytest.raises(TypeError) as exc_info:
        typecheck_test(accing_undefined_struct_code)
    assert str(exc_info.value) == "The struct: 'Enemy' are not defined"
accing_undefined_struct_code = """Health from Enemy
"""    

def test_it_fail_struct_undefined_var():
    with pytest.raises(TypeError) as exc_info:
        typecheck_test(undefined_var_code)
    assert str(exc_info.value) == "The variable: 'Speed' are not defined in the struct: 'Character'"
undefined_var_code = """create Character with:
    Health is 100
    Attack is 5
    Defense
    Name
Speed from Character
"""