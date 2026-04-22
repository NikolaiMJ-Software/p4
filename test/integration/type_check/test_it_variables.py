import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *
from setup_type_checker import type_check_test

'''
-----------------
Passing integration tests for variables
-----------------
'''

def test_it_pass_create_variable():
    result = type_check_test(create_variable_code)
    assert ["int"] == result
create_variable_code = """create X is 5
"""


def test_it_pass_create_variable_without_value():
    result = type_check_test(create_variable_without_value_code)
    assert [None] == result
create_variable_without_value_code = """create X
"""


def test_it_pass_visit_existing_variable():
    result = type_check_test(existing_variable_code)
    assert ["int", "int"] == result
existing_variable_code = """create X is 5
X
"""


def test_it_pass_assign_existing_variable():
    result = type_check_test(assign_existing_variable_code)
    assert ["int", "int"] == result
assign_existing_variable_code = """create X is 5
X is 10
"""


def test_it_pass_assign_existing_variable_updates_type():
    result = type_check_test(assign_existing_variable_updates_type_code)
    assert ["int", "str"] == result
assign_existing_variable_updates_type_code = '''create X is 5
X is "hello"
'''


def test_it_pass_assign_list_variable_updates_type():
    result = type_check_test(assign_list_variable_updates_type_code)
    assert ["list[int]", "str"] == result
assign_list_variable_updates_type_code = '''create Xs is listing: 1, 2, 3
Xs is "hello"
'''


'''
-----------------
Failing integration tests for variables
-----------------
'''

def test_it_fail_create_variable_duplicate():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(create_variable_duplicate_code)
    assert "already exists" in str(exc_info.value)
create_variable_duplicate_code = """create X is 5
create X is 10
"""


def test_it_fail_visit_missing_variable():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(missing_variable_code)
    assert "does not exist" in str(exc_info.value)
missing_variable_code = """X
"""


def test_it_fail_assign_missing_variable():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(assign_missing_variable_code)
    assert "does not exist" in str(exc_info.value)
assign_missing_variable_code = """X is 10
"""