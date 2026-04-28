import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *
from setup_type_checker import type_check_test

'''
-----------------
Passing integration tests for lists
-----------------
'''

def test_it_pass_create_empty_list():
    result = type_check_test(create_empty_list_code)
    assert [[]] == result
create_empty_list_code = """create X is listing:
"""


def test_it_pass_create_typed_int_list():
    result = type_check_test(create_typed_int_list_code)
    assert [['int', 'int', 'int']] == result
create_typed_int_list_code = """create X is listing: 1, 2, 3
"""


def test_it_pass_create_typed_string_list():
    result = type_check_test(create_typed_string_list_code)
    assert [['str', 'str']] == result
create_typed_string_list_code = '''create X is listing: "A", "B"
'''


def test_it_pass_index_access_typed_list():
    result = type_check_test(index_access_typed_list_code)
    assert [['int', 'int', 'int'], 'int'] == result
index_access_typed_list_code = """create X is listing: 1, 2, 3
index 0 of X
"""


def test_it_pass_assign_to_list_index_valid():
    result = type_check_test(assign_to_list_index_valid_code)
    assert [['int', 'int', 'int'], 'int'] == result
assign_to_list_index_valid_code = """create X is listing: 1, 2, 3
index 0 of X is 99
"""


def test_it_pass_list_index_used_in_variable_creation():
    result = type_check_test(list_index_used_in_variable_creation_code)
    assert [['int', 'int', 'int'], 'int'] == result
list_index_used_in_variable_creation_code = """create X is listing: 1, 2, 3
create Y is index 0 of X
"""


def test_it_pass_index_access_in_expression():
    result = type_check_test(index_access_in_expression_code)
    assert [['int', 'int', 'int'], 'int'] == result
index_access_in_expression_code = """create X is listing: 1, 2, 3
create Y is index 0 of X + 1
"""

def test_it_pass_create_list_mixed_types():
    result = type_check_test(create_list_mixed_types_code)
    assert [['int', 'str']] == result
create_list_mixed_types_code = '''create X is listing: 1, "A"
'''

def test_it_fail_assign_to_list_index_new_value_type():
    result = type_check_test(assign_to_list_index_wrong_value_type_code)
    assert [['str', 'int', 'int'], 'str'] == result
assign_to_list_index_wrong_value_type_code = '''create X is listing: 1, 2, 3
index 0 of X is "oops"
'''

'''
-----------------
Failing integration tests for lists
-----------------
'''
def test_it_fail_index_access_non_int_index():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(index_access_non_int_index_code)
    assert "List index must be int" in str(exc_info.value)
index_access_non_int_index_code = '''create X is listing: 1, 2, 3
index "0" of X
'''


def test_it_fail_index_access_non_list():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(index_access_non_list_code)
    assert "not a list" in str(exc_info.value)
index_access_non_list_code = """create X is 5
index 1 of X is 5
"""

def test_it_fail_index_access_none_exisiting_list():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(index_access_none_init_list_code)
    assert "The list: 'X' does not exist" in str(exc_info.value)
index_access_none_init_list_code = """index 1 of X is 5
"""