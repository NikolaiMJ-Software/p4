import pytest
from src.visitors.type_checker import *
from src.ast.nodes import *
from setup_type_checker import type_check_test

'''
-----------------
Passing integration tests for functions
-----------------
'''

def test_it_pass_define_function():
    result = type_check_test(define_function_code)
    assert [None] == result
define_function_code = """define Fun1 with A, B:
    return A + B
"""


def test_it_pass_call_function_returns_float():
    result = type_check_test(call_function_returns_float_code)
    assert [None, "float"] == result
call_function_returns_float_code = """define Fun1 with A, B:
    return A + B
call Fun1 with 1, 2.0
"""


def test_it_pass_call_function_returns_int():
    result = type_check_test(call_function_returns_int_code)
    assert [None, "int"] == result
call_function_returns_int_code = """define Fun1 with A, B:
    return A + B
call Fun1 with 1, 2
"""


def test_it_pass_define_function_without_params():
    result = type_check_test(define_function_without_params_code)
    assert [None] == result
define_function_without_params_code = """define Fun0:
    return 1
"""


def test_it_pass_call_zero_arg_function_returns_int():
    result = type_check_test(call_zero_arg_function_code)
    assert [None, "int"] == result
call_zero_arg_function_code = """define Fun0:
    return 1
call Fun0
"""


def test_it_pass_function_without_return():
    result = type_check_test(function_without_return_code)
    assert [None, None] == result
function_without_return_code = """define Fun1 with A:
    create X is A
call Fun1 with 1
"""


def test_it_pass_function_call_in_variable_creation():
    result = type_check_test(function_call_in_variable_creation_code)
    assert [None, "float"] == result
function_call_in_variable_creation_code = """define Fun1 with A, B:
    return A + B
create X is call Fun1 with 1, 2.0
"""


def test_it_pass_function_call_in_if_condition():
    result = type_check_test(function_call_in_if_condition_code)
    assert [None, None] == result
function_call_in_if_condition_code = """define IsSame with A, B:
    return A equal B
if call IsSame with 1, 1 do:
    create X is 5
"""


def test_it_pass_nested_function_usage():
    result = type_check_test(nested_function_usage_code)
    assert [None, None, "int"] == result
nested_function_usage_code = """define AddOne with A:
    return A + 1
define Double with A:
    return A * 2
call Double with call AddOne with 2
"""

def test_it_pass_get_global_var():
    result = type_check_test(function_gets_global_var)
    assert ['int', None, 'float'] == result
function_gets_global_var = """create X is 5
define Fun1:
    X is X - 0.5
    return X
call Fun1
"""


'''
-----------------
Failing integration tests for functions
-----------------
'''

def test_it_fail_define_duplicate_function():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(duplicate_function_code)
    assert "already exist" in str(exc_info.value)
duplicate_function_code = """define Fun1:
    return 1
define Fun1:
    return 2
"""


def test_it_fail_call_missing_function():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(missing_function_code)
    assert "does not exist" in str(exc_info.value)
missing_function_code = """call Fun1
"""


def test_it_fail_call_too_few_args():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(too_few_args_code)
    assert "expects 2 args, got 1" in str(exc_info.value)
too_few_args_code = """define Fun with A, B:
    return A
call Fun with 1
"""


def test_it_fail_call_too_many_args():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(too_many_args_code)
    assert "expects 1 args, got 2" in str(exc_info.value)
too_many_args_code = """define Fun with A:
    return A
call Fun with 1, 2
"""


def test_it_fail_function_body_uses_missing_param_type():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(function_body_invalid_op_code)
    assert "Expected numeric types" in str(exc_info.value)
function_body_invalid_op_code = """define Fun with A:
    return A + "x"
call Fun with 1
"""


def test_it_fail_function_call_used_with_wrong_result_type():
    with pytest.raises(TypeError) as exc_info:
        type_check_test(function_call_wrong_result_use_code)
    assert "Expected numeric types" in str(exc_info.value)
function_call_wrong_result_use_code = """define Fun:
    return "hello"
create X is call Fun + 1
"""