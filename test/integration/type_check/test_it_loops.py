import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *
from setup_type_checker import type_check_test

'''
-----------------
Passing integration tests for loops
-----------------
'''

def test_it_pass_forrange_valid():
    result = type_check_test(forrange_valid_code)
    assert [None] == result
forrange_valid_code = """for each I from 1 to 10 do:
    create X is 2
"""


def test_it_pass_forrange_with_expression_bounds():
    result = type_check_test(forrange_expression_bounds_code)
    assert [None] == result
forrange_expression_bounds_code = """for each I from 1 + 1 to 5 * 2 do:
    create X is I + 1
"""


def test_it_pass_foreach_valid():
    result = type_check_test(foreach_valid_code)
    assert [['int', 'int', 'int'], None] == result
foreach_valid_code = """create Xs is listing: 1, 2, 3
for each Item in Xs do:
    create Y is Item + 1
"""


def test_it_pass_foreach_generic_list():
    result = type_check_test(foreach_generic_list_code)
    assert [[], None] == result
foreach_generic_list_code = """create Xs is listing:
for each Item in Xs do:
    create Y
"""


def test_it_pass_foreach_with_indexed_list_element_use():
    result = type_check_test(foreach_with_math_code)
    assert [['int', 'int', 'int'], None] == result
foreach_with_math_code = """create Xs is listing: 1, 2, 3
for each Item in Xs do:
    create Y is Item * 2
"""

def test_it_pass_foreach_use_and_change_global_var_in_body():
    result = type_check_test(foreach_golbal_var_code)
    print(result)
    assert ['int', ['int', 'int', 'int'], None, 'float'] == result
foreach_golbal_var_code = """create X is 5
create Xs is listing: 1, 2, 3
for each Item in Xs do:
    create Y is 0.5
    X is X - Y
create Z is X
"""

def test_it_pass_forrange_use_and_change_global_var_in_body():
    result = type_check_test(forrange_global_var_code)
    print(result)
    assert ['float', None, 'str'] == result
forrange_global_var_code = """create Y is 0.5
for each I from 1 to 5 do:
    create X is I + 1
    if X greater than 2 do:
        Y is "h"
create Z is Y
"""


'''
-----------------
Failing integration tests for loops
-----------------
'''

def test_it_fail_forrange_invalid_bounds():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(forrange_invalid_bounds_code)
    assert "for-range bounds must be numeric" in str(exc_info.value)
forrange_invalid_bounds_code = '''for each I from "a" to 10 do:
    create X is 2
'''


def test_it_fail_foreach_missing_collection():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(foreach_missing_collection_code)
    assert "does not exist" in str(exc_info.value)
foreach_missing_collection_code = """for each Item in Xs do:
    create Y is 2
"""


def test_it_fail_foreach_non_list():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(foreach_non_list_code)
    assert "Cannot iterate over non-list type" in str(exc_info.value)
foreach_non_list_code = """create Xs is 5
for each Item in Xs do:
    create Y is 2
"""


def test_it_fail_foreach_invalid_body_operation():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(foreach_invalid_body_operation_code)
    assert "Expected numeric types" in str(exc_info.value)
foreach_invalid_body_operation_code = '''create Xs is listing: 1, 2, 3
for each Item in Xs do:
    create Y is Item + "a"
'''