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
    assert ["list"] == result
create_empty_list_code = """create X is listing:
"""


def test_it_pass_create_typed_int_list():
    result = type_check_test(create_typed_int_list_code)
    assert ["list[int]"] == result
create_typed_int_list_code = """create X is listing: 1, 2, 3
"""


def test_it_pass_create_typed_string_list():
    result = type_check_test(create_typed_string_list_code)
    assert ["list[str]"] == result
create_typed_string_list_code = '''create X is listing: "A", "B"
'''


def test_it_pass_index_access_typed_list():
    result = type_check_test(index_access_typed_list_code)
    assert ["list[int]", "int"] == result
index_access_typed_list_code = """create X is listing: 1, 2, 3
index 0 of X
"""


def test_it_pass_index_access_generic_list():
    result = type_check_test(index_access_generic_list_code)
    assert ["list", None] == result
index_access_generic_list_code = """create X is listing:
index 0 of X
"""


def test_it_pass_assign_to_list_index_valid():
    result = type_check_test(assign_to_list_index_valid_code)
    assert ["list[int]", "int"] == result
assign_to_list_index_valid_code = """create X is listing: 1, 2, 3
index 0 of X is 99
"""


def test_it_pass_list_index_used_in_variable_creation():
    result = type_check_test(list_index_used_in_variable_creation_code)
    assert ["list[int]", "int"] == result
list_index_used_in_variable_creation_code = """create X is listing: 1, 2, 3
create Y is index 0 of X
"""


def test_it_pass_index_access_in_expression():
    result = type_check_test(index_access_in_expression_code)
    assert ["list[int]", "int"] == result
index_access_in_expression_code = """create X is listing: 1, 2, 3
create Y is index 0 of X + 1
"""

def test_it_pass_create_list_mixed_types():
    result = type_check_test(create_list_mixed_types_code)
    assert ["list[int]"] == result
create_list_mixed_types_code = '''create X is listing: 1, "A"
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
    assert "Cannot index non-list type" in str(exc_info.value)
index_access_non_list_code = """create X is 5
index 0 of X
"""


def test_it_fail_assign_to_list_index_wrong_value_type():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(assign_to_list_index_wrong_value_type_code)
    assert "Cannot assign value of type" in str(exc_info.value)
assign_to_list_index_wrong_value_type_code = '''create X is listing: 1, 2, 3
index 0 of X is "oops"
'''